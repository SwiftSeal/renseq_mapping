#!/usr/bin/env python3

# This finds SNPs from the results of a biparental analysis and filters to find
# those within or near to NLR Annotator hits

import argparse
from collections import defaultdict

# Prepare function to parse CLI arguments


def parse_args():
    parser = argparse.ArgumentParser(description='Find interesting SNPs')
    parser.add_argument('--input_SNPs', required=True, type=str,
                        help='Input file of candidate SNPs')
    parser.add_argument('--input_NLRs', required=True, type=str,
                        help='Input sorted bed file from NLR Annotator')
    parser.add_argument('--output', required=True, type=str,
                        help='Output text file of interesting SNPs')
    parser.add_argument('--flanking', required=True, type=float,
                        help='Flanking region for identifying nearby SNPs')
    return parser.parse_args()

# Prepare function to load SNPs into dictionary


def load_SNPs(input_SNPs: str):
    SNP_dict = defaultdict(list)
    for line in input_SNPs:
        if line.startswith("chromosome"):
            continue
        line = line.rstrip()
        split_line = line.split('\t')
        contig = split_line[0]
        position = split_line[1]
        SNP_dict[contig].append(position)
    return SNP_dict

# Prepare function to load NLRs into dictionary


def load_NLRs(input_NLRs: str):
    NLR_dict = defaultdict(list)
    for line in input_NLRs:
        line = line.rstrip()
        split_line = line.split('\t')
        contig = split_line[0]
        start = float(split_line[1]) + 1
        stop = split_line[2]
        NLR_ID = split_line[3]
        NLR_dict[NLR_ID] = [start, stop, contig]
    return NLR_dict

# Find SNPs that are within or near to NLRs


def find_interesting_SNPs(flanking: float, input_SNPs: str, input_NLRs: str):
    SNP_dict = load_SNPs(input_SNPs)
    NLR_dict = load_NLRs(input_NLRs)
    containing_dict = defaultdict(list)
    near_dict = defaultdict(list)
    for SNP_contig in SNP_dict.keys():
        positions = SNP_dict[SNP_contig]
        for NLR in NLR_dict.keys():
            NLR_contig = NLR_dict[NLR][2]
            if NLR_contig == SNP_contig:
                NLR_start = float(NLR_dict[NLR][0])
                NLR_stop = float(NLR_dict[NLR][1])
                for position in positions:
                    if NLR_start <= float(position) <= NLR_stop:
                        containing_dict[NLR].append(position)
                    elif NLR_start - flanking <= float(position) <= NLR_stop + flanking:
                        near_dict[NLR].append(position)
    return containing_dict, near_dict

# Prepare function to write out results


def write_output(flanking: float, input_SNPs: str, input_NLRs: str, output):
    containing_dict, near_dict = find_interesting_SNPs(
        flanking, input_SNPs, input_NLRs)
    output.write("SNPs within NLRs")
    output.write('\n')
    for NLR in containing_dict.keys():
        positions = containing_dict[NLR]
        for position in positions:
            list_to_write = [NLR, position]
            string_to_write = '\t'.join(list_to_write)
            output.write(string_to_write)
            output.write('\n')
    list_to_write = ["SNPs within ", str(int(flanking)), "bp of NLRs"]
    string_to_write = ''.join(list_to_write)
    output.write(string_to_write)
    output.write('\n')
    for NLR in near_dict.keys():
        positions = containing_dict[NLR]
        for position in positions:
            list_to_write = [NLR, position]
            string_to_write = '\t'.join(list_to_write)
            output.write(string_to_write)
            output.write('\n')
    output.close()

# Prepare main function


def main():
    args = parse_args()
    input_SNPs = open(args.input_SNPs).readlines()
    input_NLRs = open(args.input_NLRs).readlines()
    output = open(args.output, 'w')
    write_output(args.flanking, input_SNPs, input_NLRs, output)


if __name__ == '__main__':
    main()
