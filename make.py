#!/usr/bin/env python3
import sys
import os, os.path
import logging
import re
from argparse import ArgumentParser
from pprint import pprint
from convert import pandoc_convert
from readyaml import readyaml
from readyaml import TOC_populate
from createwebsite import jinja_env
from createwebsite import jinja_render_template
from weasyprint import HTML, CSS


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

# templates enviroment
env = jinja_env(dir_parent + '/website-templates')
pdf_env = jinja_env(dir_parent + '/pdf-templates')

# metadata of publication from YAML file
metadata = readyaml(dir_parent + '/' + 'publication_metadata.yaml')
metadata = TOC_populate(dir_parent, metadata)  # add full path dirs to TOC
pprint(metadata)
id
def img_ref2figure(html):
    '''
    function replaces the reference to an image in the text i.e.:
    <p>![Lieke van der Maas working with Kombucha](images/AldjevanMeer/bluecitylab.png)</p> 
    to: 
    <figure>
        <img src="images/AldjevanMeer/bluecitylab.png">
        <figcaption>Lieke van der Maas working with Kombucha</figcaption>
    </figure>
    '''
    img_regex = "<p>!\[(?P<caption>.*?)\]\((?P<path>.*?)\)<\/p>"
    html = re.sub(img_regex,
                  '<figure>\
                  <img src="../\g<path>"/>\
                  <figcaption>\g<caption></figcaption>\
                  </figure>',
                  html)
    return html


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
        text_entry_content = img_ref2figure(text_entry_content)
        with open(text_entry[_to], 'w') as outfile:
            outfile.write(text_entry_content)


if args.output == 'pdf':
    print('Making {}'.format(args.output))
    pdfdir = os.path.join(dir_parent, 'pdf')
    pdfcss = os.path.join(pdfdir, 'style.pdf.css')
    tmp_html_pdf = os.path.join(pdfdir, 'allcontent.html')
    pdffile = os.path.join(pdfdir, 'publication.pdf')

    convert_loop(TOC=metadata['TOC'],
                 _from='docx',
                 _to='html')

    # Add the converted HTML to the TOC dictionary
    for text_entry in metadata['TOC']:
        print(text_entry['html'])
        with open(text_entry['html'], 'r') as html_file:
            text_entry['html_content'] = html_file.read()

    # Render template
    template = pdf_env.get_template('base.html')
    rendered = template.render(title=metadata['Title'], TOC=metadata['TOC'])

    # write content of rendered template into tmp file
    with open(tmp_html_pdf, 'w') as html_tmp:
        html_tmp.write(rendered)

    # LOG Weasyprint errors
    logger = logging.getLogger('weasyprint')
    logger.addHandler(logging.FileHandler(
        (dir_parent + '/pdf/' + 'weasyprint.log'), mode='w'
    ))

    # generate the PDF from the HTML content
    HTML(filename=tmp_html_pdf).write_pdf(pdffile,
                                          stylesheets=[CSS(filename=pdfcss)
                                                       ]
                                          )
elif args.output == 'website':
    print('Making {}'.format(args.output))
    env = jinja_env(dir_parent + '/website-templates')
    # create website's text_entries
    convert_loop(TOC=metadata['TOC'],
                 _from='docx',
                 _to='html')

    index_page = jinja_render_template(
        env=env,
        tmpl_file='index.html',
        title='',
        TOC=metadata['TOC'],  # used in menu
        content='',
        css=True,
        publication_title=metadata['Title'],
        # TODO: add authors
        # TODO rm contentpage.html
    )

    with open('website/index.html', 'w') as index_page_file:
        index_page_file.write(index_page)

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
            content=html_text,
            css=True,
            publication_title=metadata['Title'],
            # TODO: add authors
            # TODO rm contentpage.html
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
