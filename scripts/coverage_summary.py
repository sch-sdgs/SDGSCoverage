import logging
import os
import argparse
from Coverage.CoveragePy import Coverage

__author__ = 'mparker'


def main():
    parser = argparse.ArgumentParser(description='Genome coverage summaries')
    parser.add_argument('--genome_n', metavar='Ns_in_genome', type=str, default="/accelrys/apps/gel/genomeref/data/human/human_g1k_v37_NonN_Regions.CHR.bed",
                        help='a bed file of the non-N regions in genome')
    parser.add_argument('--bw', metavar='bw', default=False,
                        help='bw file')
    parser.add_argument('--bed', metavar='bed', default=False,
                        help='provide a bed file for analysis')
    parser.add_argument('--output', metavar='output', default=False,
                        help='output file')
    parser.add_argument('--xlim', metavar='xlim', default=False,
                        help='xlimit for plotting, GL is better at 101, Tumor at 201')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='If it is present then debugging is turned on')

    #todo: if bed is provided don't do exome and wholegenome - just do bed


    args = parser.parse_args()

    logger = logging.getLogger(__name__)

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG


    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    c = Coverage()
    bed = c.make_exons_bed()

    well_id = os.path.basename(args.output)

    print "making exon cov means with gc..."

    gc_output_file = args.output+".exon.coverage.means.with.GC.txt"
    output = open(gc_output_file,"w")
    result = c.exon_gc_coverage(args.bw,bed)
    result.to_csv(output, sep='\t',index=False)
    output.close()

    print "making exon cov summary..."

    exon_output_file = args.output+".exon.coverage.counts.txt"
    output = open(exon_output_file, 'w')
    result = c.coverage_counts_exon(args.bw,bed)
    result.to_csv(output, sep='\t')
    output.close()

    print "making wgs cov summary..."

    wg_output_file = args.output+".wg.coverage.counts.txt"
    output = open(wg_output_file, 'w')
    result = c.coverage_counts_wg(args.genome_n,args.bw)
    result.to_csv(output, sep='\t')
    output.close()

    print "all files made now plotting..."

    Rcommand = "make_plots_summaries.R -w " +  wg_output_file + " -e " + exon_output_file + " -g " + gc_output_file + " -l " + well_id +" -c " + args.xlim
    print Rcommand
    temp = os.system(Rcommand)


if __name__ == '__main__':
    main()
