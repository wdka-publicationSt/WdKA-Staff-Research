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
                    choices=['website', 'html', 'icml'],
                    default='website',
                    help="output formats: website, html, icml")

args = parser.parse_args()

dir_parent = os.path.dirname((os.path.abspath(__file__)))
dir_parent_ls = os.listdir(dir_parent)

# metadata of publication from YAML file
metadata = readyaml(dir_parent + '/' + 'publication_metadata.yaml')
metadata = TOC_populate(dir_parent, metadata)  # add full path dirs to TOC
pprint(metadata)

if args.output == 'website':
    print('Making {}'.format(args.output))
    env = jinja_env(dir_parent + '/website-templates')
    # create website's text_entries
    for text_entry in metadata['TOC']:
        # pprint(text_entry)
        print("{} >> {}".format(text_entry['docx'], text_entry['html']), "\n")

        text_entry_content = pandoc_convert(inputfile=text_entry['docx'],
                                            _from='docx',
                                            _to='html')
        webpage = jinja_render_template(
            env=env,
            tmpl_file='contentpage.html',
            title=text_entry['title'],
            TOC=metadata['TOC'],  # used in menu
            content=text_entry_content
            # TODO: add authors
        )
        filename = (text_entry['html'].replace('/html/', '/website/'))
        with open(filename, 'w') as webpagefile:
            webpagefile.write(webpage)
        # print(webpage)
    # create index
    webpage_idex = jinja_render_template(
        env=env,
        tmpl_file='contentpage.html',
        title=metadata['Title'],
        TOC=metadata['TOC'],  # used in menu
        content=''
        # TODO: add authors
    )

elif args.output == 'html':
    print('Making {}'.format(args.output))
    for text_entry in metadata['TOC']:
        print("{} >> {}".format(text_entry['docx'], text_entry['html']), "\n")
        text_entry_content = pandoc_convert(inputfile=text_entry['docx'],
                                            _from='docx',
                                            _to='html')
        with open(text_entry['html'], 'w') as htmlfile:
            htmlfile.write(text_entry_content)

elif args.output == 'icml':
    print('Making {}'.format(args.output))
    for text_entry in metadata['TOC']:
        print("{} >> {}".format(text_entry['docx'], text_entry['icml']), "\n")
        text_entry_content = pandoc_convert(inputfile=text_entry['docx'],
                                            _from='docx',
                                            _to='icml')
        with open(text_entry['icml'], 'w') as htmlfile:
            htmlfile.write(text_entry_content)
