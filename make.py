#!/usr/bin/env python3
import sys
import os
from argparse import ArgumentParser
from pprint import pprint
from convert import pandoc_convert
from readyaml import readyaml
from createwebsite import jinja_env
from createwebsite import jinja_render_template

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

# metadata of publication from YAML file
metadata = readyaml(dir_parent + '/' + 'publication_metadata.yaml')
pprint(metadata)


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


def TOC_populate(metadata_dict):
    for text_entry in metadata_dict['TOC']:
        try:
            docx = dir_parent + '/docx/' + text_entry['docx']
            html = dir_parent + '/html/' + docx.replace('.docx', '.html')
            # for text entry in TOC
            # add full path of html and docx files
            text_entry['html'] = html
            text_entry['docx'] = docx
            print(text_entry)

        except Exception as e:
            print('Error with {} in {}'.format(e, text_entry))
            sys.exit(1)
        print(text_entry)


if args.output == 'website':
    print('Making {}'.format(args.output))
    convert_files(input_format_dict=metadata['Formats']['docx'],
                  output_format_dict=metadata['Formats']['html'])
    TOC_populate(metadata)
    env = jinja_env(dir_parent + '/website-templates')

    # TODO: include template vars mytitle=metadata['Title'], TOC=metadata['TOC'], content="testing",

    # use metadata['TOC'] to order publication

    page=jinja_render_template(env=env,
                          tmpl_file='contentpage.html')
    print(env, page)



elif args.output == 'html':
    print('Making {}'.format(args.output))
    convert_files(input_format_dict=metadata['Formats']['docx'],
                  output_format_dict=metadata['Formats']['html'])
elif args.output == 'icml':
    print('Making {}'.format(args.output))
    convert_files(input_format_dict=metadata['Formats']['docx'],
                  output_format_dict=metadata['Formats']['icml'])
