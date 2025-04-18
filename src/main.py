import argparse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from alignment import Alignment
from tree_builder import TreeBuilder
from benchmarks.neighbor_joining import neighbor_joining
from math import isqrt
import newick

def main():
    parser = argparse.ArgumentParser(description="FastTree implemented in Python")
    parser.add_argument("--algo",
                        type=str,
                        help="the algorithm used to construct the tree",
                        required=True,
                        choices=["nj", "slowtree"])
    parser.add_argument("input_file",
                        type=argparse.FileType("r"),
                        help="the aligned nucleotide sequences in fasta format")
    parser.add_argument("output_file",
                        type=argparse.FileType("w"),
                        help="the file to output the tree to")

    args = parser.parse_args()
    logger.info(f"Loading fasta file: {args.input_file.name}")
    fasta_data = args.input_file.read().strip().split('\n')

    alignment_dict = dict()
    for label_line, seq in zip(fasta_data[::2], fasta_data[1::2]):
        label = label_line[1:].split(' ', 1)[0]
        alignment_dict[label] = seq

    logger.info(f"Constructing profile matrices")
    alignment = Alignment(alignment_dict)
    logger.info(f"Profile matrices of {alignment.alignment_size} sequences "
        f"of length {alignment.alignment_length} successfully constructed")

    if args.algo == "nj":
        newick.dump(neighbor_joining(alignment), args.output_file)
    else:
        tree_builder = TreeBuilder(alignment,
                                   refresh_interval=isqrt(alignment.alignment_size))
        newick.dump(tree_builder.build(), args.output_file)

if __name__ == "__main__":
    main()
