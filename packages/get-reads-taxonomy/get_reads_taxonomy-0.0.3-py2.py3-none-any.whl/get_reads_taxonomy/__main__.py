"""
 Copyright (c) 2022 Antonio Fernandez-Guerra

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """


import logging

from get_reads_taxonomy.utils import (
    get_arguments,
    create_output_files,
    splitkeep,
    fast_flatten,
)
from get_reads_taxonomy.defaults import valid_ranks
from get_reads_taxonomy.extract import get_read_by_taxa, index_bam_file
import pandas as pd
import os
import pysam
import numpy as np
from Bio import SeqIO, SeqRecord
import gzip
from mimetypes import guess_type
from functools import partial
import tqdm
from collections import defaultdict
import re


log = logging.getLogger("my_logger")


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s ::: %(asctime)s ::: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    args = get_arguments()
    logging.getLogger("my_logger").setLevel(
        logging.DEBUG if args.debug else logging.INFO
    )

    # Check that rank and taxonomy file are both present
    if args.rank and not args.taxonomy_file:
        log.error("--rank requires --taxonomy")
        exit(1)
    if args.taxonomy_file and not args.rank:
        log.error("Error: --taxonomy-file requires --rank")
        exit(1)

    discarded_refs = {}
    refs_tax = defaultdict()

    log.info("Loading taxonomy data...")
    taxonomy = pd.read_csv(
        args.taxonomy_file,
        sep="\t",
        header=None,
        names=["reference", "taxonomy"],
    )

    # get get_ranks
    ranks = {valid_ranks[x]: args.rank[x] for x in args.rank if x in valid_ranks}
    # get refs that belong to this taxonomy
    # loop over all rows
    for i, row in tqdm.tqdm(
        taxonomy.iterrows(),
        total=taxonomy.shape[0],
        desc="Taxa processed",
        leave=False,
    ):
        taxs = row[1].split(";")
        for r in taxs:
            r1 = splitkeep(r, "__")
            if r1[0] in ranks and any(r == x for x in ranks[r1[0]]):
                v = re.sub("[^0-9a-zA-Z]+", "_", r1[1])
                refs_tax[row[0]] = f"{r1[0]}{v}"
                # refs[row[0]] = f

    logging.info("Loading BAM file...")
    save = pysam.set_verbosity(0)
    bam = args.bam
    samfile = pysam.AlignmentFile(bam, "rb", threads=args.threads)
    chr_lengths = []
    for chrom in samfile.references:
        chr_lengths.append(samfile.get_reference_length(chrom))
    max_chr_length = np.max(chr_lengths)

    # Check if BAM files is not sorted by coordinates, sort it by coordinates
    if not samfile.header["HD"]["SO"] == "coordinate":
        log.info("BAM file is not sorted by coordinates, sorting it...")
        sorted_bam = bam.replace(".bam", ".grt-sorted.bam")
        pysam.sort(
            "-@", str(args.threads), "-m", str(args.sort_memory), "-o", sorted_bam, bam
        )
        bam = sorted_bam
        # Reindex the sorted BAM file
        index_bam_file(
            bam,
            suffix=".grt-sorted.bam",
            max_chr_length=max_chr_length,
            threads=args.threads,
        )
        samfile.close()
        samfile = pysam.AlignmentFile(bam, "rb", threads=args.threads)
    else:
        if not samfile.has_index():
            index_bam_file(
                bam=bam,
                suffix="bam",
                max_chr_length=max_chr_length,
                threads=args.threads,
            )
            samfile = pysam.AlignmentFile(bam, "rb", threads=args.threads)

    # rnames = defaultdict(int)
    # for aln in samfile.fetch(multiple_iterators=False, until_eof=True):
    #     rnames[aln.qname] += 1

    # samfile.close()
    # print(len(rnames))
    # exit()

    pysam.set_verbosity(save)

    refs_bam = [
        chrom.contig for chrom in samfile.get_index_statistics() if chrom.mapped > 0
    ]

    # for ref in refs_bam:
    #     if ref not in refs_tax:
    #         print(ref)
    #         discarded_refs[ref] = "not in taxonomy file"
    # print(len(discarded_refs))
    # exit()
    # If we have a taxonomy file, get the references that are in the BAM file
    # if not we just report all reads in the BAM file

    refs = [x for x in refs_bam if x in refs_tax]
    # check ir refs is empty, then exit
    if len(refs) == 0:
        log.error("No references to extract")
        exit(1)

    out_files = create_output_files(prefix=args.prefix, bam=args.bam, taxon=ranks)

    # for file in out_files:
    #     # file exists deleted
    #     if os.path.exists(out_files[file]):
    #         os.remove(out_files[file])

    log.info("Processing reads...")

    reads = get_read_by_taxa(
        bam=bam,
        refs=refs,
        refs_tax=refs_tax,
        threads=args.threads,
        chunksize=args.chunk_size,
    )
    # write reads

    count = defaultdict(int)
    if args.only_read_ids:
        logging.info("Saving only read ids...")
    else:
        logging.info("Saving reads...")

    if args.unique_reads:
        logging.info("Saving only unique reads...")

    if args.taxonomy_file:
        desc = "Taxa processed"
    else:
        desc = "References processed"

    reads_seen = defaultdict(int)
    tax_count = 0
    for tax in tqdm.tqdm(reads, ncols=80, desc=desc, leave=False, total=len(reads)):
        if args.combine_reads:
            r = splitkeep(tax, "__")
            r[1] = re.sub("[^0-9a-zA-Z]+", "_", r[1])
            fastq = os.devnull
            fastq_ids = os.devnull
            fastq_combined = (
                out_files["fastq_combined"]["fname"]
                if args.combine_reads and not args.only_read_ids
                else os.devnull
            )
            fastq_combined_ids = (
                out_files["fastq_combined_read_ids"]["fname"]
                if args.only_read_ids
                else os.devnull
            )
        else:
            fastq = out_files[tax]["fname"] if not args.only_read_ids else os.devnull
            fastq_ids = (
                out_files[f"{tax}_read_ids"]["fname"]
                if args.only_read_ids
                else os.devnull
            )
            fastq_combined = os.devnull
            fastq_combined_ids = os.devnull

        os.remove(fastq) if os.path.exists(fastq) and fastq != os.devnull else None

        os.remove(fastq_ids) if os.path.exists(
            fastq_ids
        ) and fastq_ids != os.devnull else None

        os.remove(fastq_combined) if os.path.exists(
            fastq_combined
        ) and fastq_combined != os.devnull and tax_count == 0 else None

        os.remove(fastq_combined_ids) if os.path.exists(
            fastq_combined_ids
        ) and fastq_combined_ids != os.devnull and tax_count == 0 else None

        tax_count += 1

        encoding = "gzip"
        # get
        _open = partial(gzip.open, mode="at") if encoding == "gzip" else open
        # TODO: clean this up
        if len(reads[tax]) > 3:
            disable_tqdm = False
        else:
            disable_tqdm = True

        with _open(fastq) as f, _open(fastq_combined) as f_combined, _open(
            fastq_ids
        ) as f_ids, _open(fastq_combined_ids) as f_combined_ids:
            for read in tqdm.tqdm(
                reads[tax],
                ncols=80,
                desc="Reads written",
                leave=False,
                total=len(reads[tax]),
                ascii="░▒█",
                disable=disable_tqdm,
            ):
                if args.only_read_ids:
                    rec = read
                else:
                    rec = SeqRecord.SeqRecord(reads[tax][read]["seq"], read, "", "")
                    rec.letter_annotations["phred_quality"] = reads[tax][read]["qual"]
                if args.combine_reads:
                    if read not in reads_seen:
                        if args.only_read_ids:
                            f_combined_ids.write(f"{read}\n")
                            count[out_files["fastq_combined_read_ids"]["fname"]] += 1
                        else:
                            SeqIO.write(rec, f_combined, "fastq")
                            count[out_files["fastq_combined"]["fname"]] += 1
                        reads_seen[read] += 1
                else:
                    if args.unique_reads:
                        if reads[tax][read]["rclass"] == "unique":
                            if args.only_read_ids:
                                f_ids.write(f"{read}\n")
                                count[out_files[f"{tax}_read_ids"]["fname"]] += 1
                            else:
                                SeqIO.write(rec, f, "fastq")
                                count[out_files[f"{tax}"]["fname"]] += 1
                    else:
                        if args.only_read_ids:
                            f_ids.write(f"{read}\n")
                            count[out_files[f"{tax}_read_ids"]["fname"]] += 1
                        else:
                            SeqIO.write(rec, f, "fastq")
                            count[out_files[f"{tax}"]["fname"]] += 1

    for file in out_files:
        if count[out_files[file]["fname"]] and count[out_files[file]["fname"]] > 0:
            pass
        else:
            # check if file exists
            if (
                os.path.exists(out_files[file]["fname"])
                and out_files[file]["exists"] is not True
            ):
                os.remove(out_files[file]["fname"])

    logging.info("Done!")


if __name__ == "__main__":
    main()
