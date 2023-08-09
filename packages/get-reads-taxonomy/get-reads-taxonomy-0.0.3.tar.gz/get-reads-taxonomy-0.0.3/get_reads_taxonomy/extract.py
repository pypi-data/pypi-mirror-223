import tqdm
import pysam
from Bio import Seq
import logging
from multiprocessing import Pool
from collections import defaultdict
from functools import partial
from get_reads_taxonomy.utils import is_debug, calc_chunksize, initializer
import os

# import cProfile as profile
# import pstats

log = logging.getLogger("my_logger")


def index_bam_file(bam, suffix, max_chr_length, threads=1):
    logging.info("Indexing BAM file...")
    samfile = pysam.AlignmentFile(bam, "rb", threads=threads)
    if samfile.has_index():
        sorted_bam_index_bai = bam.replace(suffix, f"{suffix}.bam.bai")
        sorted_bam_index_csi = bam.replace(suffix, f"{suffix}.bam.csi")
        if os.path.exists(sorted_bam_index_bai):
            os.remove(sorted_bam_index_bai)
        elif os.path.exists(sorted_bam_index_csi):
            os.remove(sorted_bam_index_csi)

    if max_chr_length > 536870912:
        logging.info("A reference is longer than 2^29, indexing with csi")
        pysam.index("-c", "-@", str(threads), bam)
    else:
        pysam.index(
            "-@", str(threads), bam
        )  # Need to reload the samfile after creating index
    samfile.close()


def get_alns(params, refs_tax, threads=1):
    reads = defaultdict(lambda: defaultdict(dict))
    bam, references = params
    samfile = pysam.AlignmentFile(bam, "rb", threads=threads)
    for reference in references:
        for aln in samfile.fetch(
            contig=reference, multiple_iterators=False, until_eof=True
        ):
            # create read

            #

            # Check if reference is damaged
            aln_reference_name = reference
            aln_qname = aln.qname

            if aln_reference_name in refs_tax:
                name = refs_tax[aln_reference_name]
                if reads[name][aln_qname]:
                    log.debug("Read already exists")
                else:
                    seq = Seq.Seq(aln.seq)
                    qual = aln.query_qualities
                    if aln.is_reverse:
                        seq = seq.reverse_complement()
                        qual = qual[::-1]
                    reads[name][aln_qname] = {
                        "seq": seq,
                        "qual": qual,
                        "rtax": name,
                    }
    samfile.close()
    return dict(reads)


def merge_dicts(dicts):
    reads = defaultdict(lambda: defaultdict(dict))
    read_seen = defaultdict(int)
    for d in dicts:
        for tax, tax_reads in d.items():
            for read, read_info in tax_reads.items():
                if read in read_seen:
                    read_info["rclass"] = "duplicate"
                    reads[tax][read] = read_info
                    read_seen[read] += 1
                else:
                    read_info["rclass"] = "unique"
                    reads[tax][read] = read_info
                    read_seen[read] += 1

    return dict(reads)


def get_read_by_taxa(
    bam,
    refs,
    refs_tax,
    chunksize=None,
    threads=1,
):
    # prof = profile.Profile()
    # prof.enable()

    if (chunksize is not None) and ((len(refs) // chunksize) > threads):
        c_size = chunksize
    else:
        c_size = calc_chunksize(n_workers=threads, len_iterable=len(refs), factor=4)

    ref_chunks = [refs[i : i + c_size] for i in range(0, len(refs), c_size)]

    params = zip([bam] * len(ref_chunks), ref_chunks)

    if is_debug():
        data = list(
            map(
                partial(
                    get_alns,
                    refs_tax=refs_tax,
                    threads=threads,
                ),
                params,
            )
        )
    else:
        logging.info(
            f"Processing {len(ref_chunks):,} chunks of {c_size:,} references each..."
        )
        p = Pool(
            threads,
            initializer=initializer,
            initargs=([params, refs_tax],),
        )

        data = list(
            tqdm.tqdm(
                p.imap_unordered(
                    partial(
                        get_alns,
                        refs_tax=refs_tax,
                        threads=threads,
                    ),
                    params,
                    chunksize=1,
                ),
                total=len(ref_chunks),
                leave=False,
                ncols=80,
                desc="References processed",
            )
        )

        p.close()
        p.join()
    # prof.disable()
    # # print profiling output
    # stats = pstats.Stats(prof).sort_stats("tottime")
    # stats.print_stats(10)
    log.info(f"Merging {len(ref_chunks)} chunks...")
    data = merge_dicts(data)  # top 10 rows
    return data
