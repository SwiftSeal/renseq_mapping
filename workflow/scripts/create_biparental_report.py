#! /usr/bin/env python3

# This script takes information from the biparental mapping pipeline to produce
# a convenient report

import argparse
from collections import defaultdict

# Prepare function to parse CLI arguments


def parse_args():
    parser = argparse.ArgumentParser(description='Prepare a report')
    parser.add_argument('--output', required=True, type=str,
                        help='Output report text file')
    parser.add_argument('--read_counts', required=True, nargs='+',
                        type=str, help='space separated list of read count files')
    parser.add_argument('--experiment_name', required=True,
                        type=str, help='Name of the experiment')
    parser.add_argument('--R_parent_name', required=True,
                        type=str, help='Name of R parent used')
    parser.add_argument('--S_parent_name', required=True,
                        type=str, help='Name of S parent used')
    parser.add_argument('--R_bulk_path', required=True,
                        type=str, help='Path of R bulk used')
    parser.add_argument('--S_bulk_path', required=True,
                        type=str, help='Path of S bulk used')
    parser.add_argument('--reference_name', required=True,
                        type=str, help='Name of accession used for HiFi assembly')
    parser.add_argument('--snp_counts', required=True, nargs='+',
                        type=str, help='space separated list of snp count files')
    parser.add_argument('--parent_S_min', required=True, type=float,
                        help='Minimum allele frequency used for suspectible parent')
    parser.add_argument('--parent_S_max', required=True, type=float,
                        help='Maximum allele frequency used for suspectible parent')
    parser.add_argument('--parent_R_min', required=True, type=float,
                        help='Minimum allele frequency used for resistant parent')
    parser.add_argument('--parent_R_max', required=True, type=float,
                        help='Maximum allele frequency used for resistant parent')
    parser.add_argument('--bulk_S_min', required=True, type=float,
                        help='Minimum allele frequency used for suspectible bulk')
    parser.add_argument('--bulk_S_max', required=True, type=float,
                        help='Maximum allele frequency used for suspectible bulk')
    parser.add_argument('--bulk_R_min', required=True, type=float,
                        help='Minimum allele frequency used for resistant bulk')
    parser.add_argument('--bulk_R_max', required=True, type=float,
                        help='Maximum allele frequency used for resistant bulk')
    parser.add_argument('--interesting_snps', required=True,
                        type=str, help='Path to interesting snps file')
    parser.add_argument('--blast_results', required=True, type=str,
                        help='Path to file of blast results of contigs against reference')
    return parser.parse_args()

# Prepare function to get necessary data


def get_data(R_bulk_path: str, S_bulk_path: str, read_counts: list, snp_counts: list, blast_results: str):
    # Get R bulk name
    R_bulk_filename = R_bulk_path.split('/')[-1]
    R_bulk_name = R_bulk_filename.split('.')[0]

    # Get S bulk name
    S_bulk_filename = S_bulk_path.split('/')[-1]
    S_bulk_name = S_bulk_filename.split('.')[0]

    # Get read counts
    read_count_dict = defaultdict(list)
    for read_count_file in read_counts:
        read_count_filename = read_count_file.split('/')[-1]
        read_count_source = read_count_filename.split('.')[0]
        read_count_phenotype = read_count_filename.split('.')[1]
        with open(read_count_file) as read_count_results:
            read_count_lines = read_count_results.readlines()
            R1 = read_count_lines[0].rstrip().split()[1]
            R2 = read_count_lines[1].rstrip().split()[1]
        read_count_ID = read_count_source + "_" + read_count_phenotype
        read_count_dict[read_count_ID] = [R1, R2]

    # Get SNP counts
    snp_count_dict = defaultdict(float)
    for snp_count_file in snp_counts:
        snp_count_filename = snp_count_file.split('/')[-1]
        snp_count_source = snp_count_filename.split('.')[0]
        snp_count_filtering = snp_count_filename.split('.')[1]
        with open(snp_count_file) as snp_count_results:
            snp_count_lines = snp_count_results.readlines()
            snp_count = snp_count_lines[0].rstrip()
        snp_count_ID = snp_count_source + "_" + snp_count_filtering
        snp_count_dict[snp_count_ID] = snp_count

    # Get BLAST results
    blast_result_dict = defaultdict(str)
    with open(blast_results) as blast_hits:
        blast_lines = blast_hits.readlines()
        for blast_line in blast_lines:
            blast_line = blast_line.rstrip()
            contig = blast_line[0]
            chromosome = blast_line[1]
            blast_result_dict[contig] = chromosome

    # Return data structures out of function
    return R_bulk_name, S_bulk_name, read_count_dict, snp_count_dict, blast_result_dict

# Prepare function to write out report file


def write_output(R_bulk_path: str, S_bulk_path: str, read_counts: list, snp_counts: list, blast_results: str, output: str, experiment_name: str, R_parent_name: str, S_parent_name: str, parent_R_min: float, parent_R_max: float, parent_S_min: float, parent_S_max: float, bulk_R_min: float, bulk_R_max: float, bulk_S_min: float, bulk_S_max: float, interesting_snps: str):
    R_bulk_name, S_bulk_name, read_count_dict, snp_count_dict, blast_result_dict = get_data(
        R_bulk_path, S_bulk_path, read_counts, snp_counts, blast_results)
    with open(output, 'w') as outfile:
        # Write out experiment name
        outfile.write(experiment_name)
        outfile.write('\n')
        outfile.write('\n')

        # Write out samples used
        outfile.write("Resistant Parent: ")
        outfile.write(R_parent_name)
        outfile.write('\n')
        outfile.write("Susceptible Parent: ")
        outfile.write(S_parent_name)
        outfile.write('\n')
        outfile.write("Resistant Bulk: ")
        outfile.write(R_bulk_name)
        outfile.write('\n')
        outfile.write("Susceptible Bulk: ")
        outfile.write(S_bulk_name)
        outfile.write('\n')
        outfile.write('\n')

        # Write out read counts
        outfile.write("Resistant Parent Reads:")
        outfile.write('\n')
        outfile.write("R1: ")
        outfile.write(str(read_count_dict["parent_resistant"][0]))
        outfile.write('\n')
        outfile.write("R2: ")
        outfile.write(str(read_count_dict["parent_resistant"][1]))
        outfile.write('\n')
        outfile.write("Susceptible Parent Reads:")
        outfile.write('\n')
        outfile.write("R1: ")
        outfile.write(str(read_count_dict["parent_susceptible"][0]))
        outfile.write('\n')
        outfile.write("R2: ")
        outfile.write(str(read_count_dict["parent_susceptible"][1]))
        outfile.write('\n')
        outfile.write("Resistant Bulk Reads:")
        outfile.write('\n')
        outfile.write("R1: ")
        outfile.write(str(read_count_dict["bulk_resistant"][0]))
        outfile.write('\n')
        outfile.write("R2: ")
        outfile.write(str(read_count_dict["bulk_resistant"][1]))
        outfile.write('\n')
        outfile.write("Susceptible Bulk Reads:")
        outfile.write('\n')
        outfile.write("R1: ")
        outfile.write(str(read_count_dict["bulk_susceptible"][0]))
        outfile.write('\n')
        outfile.write("R2: ")
        outfile.write(str(read_count_dict["bulk_susceptible"][1]))
        outfile.write('\n')
        outfile.write('\n')

        # Write out filtering conditions
        outfile.write("Filtering parameters used:")
        outfile.write('\n')
        outfile.write("Resistant Parent:")
        outfile.write('\n')
        outfile.write("Minimum Frequency: ")
        outfile.write(str(parent_R_min))
        outfile.write('\n')
        outfile.write("Maximum Frequency: ")
        outfile.write(str(parent_R_max))
        outfile.write('\n')
        outfile.write("Susceptible Parent:")
        outfile.write('\n')
        outfile.write("Minimum Frequency: ")
        outfile.write(str(parent_S_min))
        outfile.write('\n')
        outfile.write("Maximum Frequency: ")
        outfile.write(str(parent_S_max))
        outfile.write('\n')
        outfile.write("Resistant Bulk:")
        outfile.write('\n')
        outfile.write("Minimum Frequency: ")
        outfile.write(str(bulk_R_min))
        outfile.write('\n')
        outfile.write("Maximum Frequency: ")
        outfile.write(str(bulk_R_max))
        outfile.write('\n')
        outfile.write("Susceptible Bulk:")
        outfile.write('\n')
        outfile.write("Minimum Frequency: ")
        outfile.write(str(bulk_S_min))
        outfile.write('\n')
        outfile.write("Maximum Frequency: ")
        outfile.write(str(bulk_S_max))
        outfile.write('\n')
        outfile.write('\n')

        # Write out SNP counts
        outfile.write("Number of SNPs identified before filtering:")
        outfile.write('\n')
        outfile.write("Parent: ")
        outfile.write(str(snp_count_dict["parent_unfiltered"]))
        outfile.write('\n')
        outfile.write("Bulk: ")
        outfile.write(str(snp_count_dict["bulk_unfiltered"]))
        outfile.write('\n')
        outfile.write('\n')
        outfile.write("Number of SNPs identified after filtering:")
        outfile.write('\n')
        outfile.write("Parent: ")
        outfile.write(str(snp_count_dict["parent_filtered"]))
        outfile.write('\n')
        outfile.write("Bulk: ")
        outfile.write(str(snp_count_dict["bulk_filtered"]))
        outfile.write('\n')
        outfile.write('\n')

        # Write out interesting SNPs
        with open(interesting_snps) as snps_of_interest:
            snp_lines = snps_of_interest.readlines()
            for snp_line in snp_lines:
                snp_line = snp_line.rstrip()
                outfile.write(snp_line)
                outfile.write('\n')
            snps_of_interest.close()
        outfile.write('\n')

        # Write out BLAST locations in DM
        outfile.write("Locations of contigs in DM:")
        for contig in blast_result_dict.keys():
            chromosome = blast_result_dict[contig]
            list_to_write = [contig, chromosome]
            string_to_write = '\t'.join(list_to_write)
            outfile.write(string_to_write)
            outfile.write('\n')

# Prepare main function


def main():
    args = parse_args()
    R_bulk_path = args.R_bulk_path
    S_bulk_path = args.S_bulk_path
    read_counts = args.read_counts
    snp_counts = args.snp_counts
    blast_results = args.blast_results
    output = args.output
    experiment_name = args.experiment_name
    R_parent_name = args.R_parent_name
    S_parent_name = args.S_parent_name
    parent_R_min = args.parent_R_min
    parent_R_max = args.parent_R_max
    parent_S_min = args.parent_S_min
    parent_S_max = args.parent_S_max
    bulk_R_min = args.bulk_R_min
    bulk_R_max = args.bulk_R_max
    bulk_S_min = args.bulk_S_min
    bulk_S_max = args.bulk_S_max
    interesting_snps = args.interesting_snps
    write_output(R_bulk_path, S_bulk_path, read_counts, snp_counts, blast_results, output, experiment_name, R_parent_name, S_parent_name,
                 parent_R_min, parent_R_max, parent_S_min, parent_S_max, bulk_R_min, bulk_R_max, bulk_S_min, bulk_S_max, interesting_snps)


if __name__ == '__main__':
    main()
