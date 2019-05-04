#!/usr/bin/env python3
import sys
import os
from argparse import ArgumentParser
from convert import pandoc_convert

parser = ArgumentParser(prog=sys.argv[0],
                        usage='%(prog)s  output',
                        description="Script to convert \
                        docx files to other format: icml, html, website")
parser.add_argument("output",
                    choices=['website', 'html', 'icml'],
                    default='website',
                    help="output formats: website, html, icml")

args = parser.parse_args()

dir_parent = os.path.dirname((os.path.abspath(__file__)))
dir_parent_ls = os.listdir(dir_parent)

# dictionary strcuture and populate
formats = {f: {
    "format": f,
    "dir": dir_parent + "/" + f}
    for f in ["docx", "html", "icml"]}

# print(formats)


def ls_dir(d):
    visible_files = [f for f in os.listdir(d) if f[0] is not '.']
    return visible_files


def convert_files(input_format_dict, output_format_dict):
    in_dir = input_format_dict['dir']
    in_format = input_format_dict['format']
    out_dir = output_format_dict['dir']
    out_format = output_format_dict['format']
    for input_file in ls_dir(in_dir):
        output_file = "{}/{}".format(out_dir,
                                     input_file.replace(in_format, out_format))
        input_file = "{}/{}".format(in_dir, input_file)

        pandoc_output = pandoc_convert(_from=in_format,
                                       _to=out_format,
                                       inputfile=input_file,
                                       outputfile=output_file)
        print(pandoc_output)


if args.output == 'website':
    print('Making {}'.format(args.output))
    convert_files(input_format_dict=formats['docx'],
              output_format_dict=formats['html'])
elif args.output == 'html':
    print('Making {}'.format(args.output))
    convert_files(input_format_dict=formats['docx'],
                  output_format_dict=formats['html'])
elif args.output == 'icml':
    print('Making {}'.format(args.output))
    convert_files(input_format_dict=formats['docx'],
                  output_format_dict=formats['icml'])