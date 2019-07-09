#!/usr/bin/env python3
import sys
import os
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
from pprint import pprint
import pkg_resources
installed_packages = pkg_resources.working_set
installed_packages_list = sorted([i.key for i in installed_packages])
if 'nltk' in installed_packages_list:
    import nltk



parser = ArgumentParser(prog=sys.argv[0],
                        usage='%(prog)s  output',
                        description="Script to convert \
                        docx files to other format: icml, html, website")
parser.add_argument("output",
                    choices=['website', 'html', 'icml', 'pdf', 'wordfrequency'],
                    default='website',
                    help="output formats: website, html, icml, pdf")

args = parser.parse_args()

dir_parent = os.path.dirname((os.path.abspath(__file__)))
dir_parent_ls = os.listdir(dir_parent)

# templates enviroment
env = jinja_env(dir_parent + '/website-templates')

# metadata of publication from YAML file
metadata = readyaml(dir_parent + '/' + 'publication_metadata.yaml')
metadata = TOC_populate(dir_parent, metadata)  # add full path dirs to TOC
pprint(metadata)

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


def word_frequency(word_amount=20):
    '''
    Returns word frequency of the entire publication
    REQUIRES NLTK
    '''
    print('Making {}'.format(args.output))
    convert_loop(TOC=metadata['TOC'],
                 _from='docx',
                 _to='txt')
    txt_all = ''
    for text_entry in metadata['TOC']:
        print(text_entry['txt'])
        with open(text_entry['txt'], 'r') as txt_file:
            txt = txt_file.read()
            # assemble all HTML files content
            # onto a single variable html_all
            txt_all += txt
    allWords = nltk.tokenize.word_tokenize(txt_all)
    stopwords = nltk.corpus.stopwords.words('english')
    allWordExceptStopDist = nltk.FreqDist(w.lower() for w in allWords
                                          if w.lower() not in stopwords and
                                          len(w) > 2)
    mostCommon = allWordExceptStopDist.most_common(word_amount)
    mostCommon_filename = dir_parent + '/commonWords.txt'
    with open(mostCommon_filename, 'w') as mostCommon_file:
        mostCommon_list_strings = [(': ').join([pair[0], str(pair[1])]) for pair in mostCommon]
        mostCommon_file.write(('\n').join(mostCommon_list_strings))
    pprint(mostCommon)
    return mostCommon


def keywords_to_html(words_freqs, html):
    '''
    Tags the html content with keyword from word_freq
    inputs:
        - word_freq: a list of tupples, containing:
        most common words (keywords) and their frequency
        - html: the html content to be tagged
    '''
    html_span = '<span class="keyword {}">{}</span>'
    for word_freq in words_freqs:
        word = word_freq[0]
        # freq = word_freq[1]
        # TODO: include Capitalized, uppercase words
        html = html.replace(word, html_span.format(word, word))
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
                                            _to=_to.replace('txt','plain'))
        text_entry_content = img_ref2figure(text_entry_content)
        with open(text_entry[_to], 'w') as outfile:
            outfile.write(text_entry_content)


if args.output == 'wordfrequency':
    word_frequency(word_amount=30)

if args.output == 'pdf':
    print('Making {}'.format(args.output))
    pdfdir = dir_parent + '/pdf/'
    pdfcss = pdfdir + 'style.pdf.css'
    tmp_html_pdf = pdfdir + 'allcontent.html'
    pdffile = pdfdir + 'publication.pdf'

    convert_loop(TOC=metadata['TOC'],
                 _from='docx',
                 _to='html')

    html_all = ''

    for text_entry in metadata['TOC']:
        print(text_entry['html'])
        with open(text_entry['html'], 'r') as html_file:
            html_text = html_file.read()
            # assemble all HTML files content
            # onto a single variable html_all
            html_all += html_text

    # place html_all to HTML template
    htlm_head_body = jinja_render_template(
        env=env,
        tmpl_file='contentpage.html',
        title=metadata['Title'],
        content=html_all,
    )

    # write content of html_all into tmp file
    with open(tmp_html_pdf, 'w') as html_tmp:
        html_tmp.write(htlm_head_body)

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
    if 'nltk' in installed_packages_list:
        words_freqs = word_frequency(word_amount=30)
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
            # if nltk module is installed
            # tag most frequent words:
            if 'nltk' in installed_packages_list:
                html_text = keywords_to_html(words_freqs=words_freqs,
                                             html=html_text)
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
