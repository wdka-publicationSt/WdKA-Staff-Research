#!/usr/bin/env python3
import sys
import os
from argparse import ArgumentParser
from pprint import pprint
from convert import pandoc_convert
from readyaml import readyaml
from readyaml import TOC_populate
from createwebsite import jinja_env
from createwebsite import jinja_render_template


parser = ArgumentParser(prog=sys.argv[0],
                        usage='%(prog)s  output',
                        description="Script to convert \
                        docx files to other format: icml, html, website")
parser.add_argument("output",
                    choices=['website', 'html', 'icml', 'pdf'],
                    default='website',
                    help="output formats: website, html, icml, pdf")

args = parser.parse_args()

dir_parent = os.path.dirname((os.path.abspath(__file__)))
dir_parent_ls = os.listdir(dir_parent)

# metadata of publication from YAML file
metadata = readyaml(dir_parent + '/' + 'publication_metadata.yaml')
metadata = TOC_populate(dir_parent, metadata)  # add full path dirs to TOC
pprint(metadata)


def convert_loop(TOC, _from, _to):
    '''
    Loop through all files TOC
    Converting them from _from to _to format
    '''
    for text_entry in TOC:
        print("{} >> {}".format(text_entry[_from],
              text_entry[_to]), "\n")
        text_entry_content = pandoc_convert(inputfile=text_entry['docx'],
                                            _from=_from,
                                            _to=_to)
        with open(text_entry[_to], 'w') as outfile:
            outfile.write(text_entry_content)


if args.output == 'website':
    print('Making {}'.format(args.output))
    env = jinja_env(dir_parent + '/website-templates')
    # create website's text_entries
    convert_loop(TOC=metadata['TOC'],
                 _from='docx',
                 _to='html')
    for text_entry in metadata['TOC']:
        print(text_entry['html'])
        with open(text_entry['html'], 'r') as html_file:
            html_text = html_file.read()
            # print(html_text)
        webpage = jinja_render_template(
            env=env,
            tmpl_file='contentpage.html',
            title=text_entry['title'],
            TOC=metadata['TOC'],  # used in menu
            content=html_text
            # TODO: add authors
        )
        filename = (text_entry['html'].replace('/html/', '/website/'))
        with open(filename, 'w') as webpagefile:
            webpagefile.write(webpage)

elif args.output == 'html':
    convert_loop(TOC=metadata['TOC'], _from='docx', _to='html')
elif args.output == 'icml':
    convert_loop(TOC=metadata['TOC'], _from='docx', _to='icml')
elif args.output == 'pdf':
    convert_loop(TOC=metadata['TOC'], _from='docx', _to='html')
    # ICML STUFF
