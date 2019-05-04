#!/usr/bin/env python3
import os
import sys
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
# from jinja2 import Template
from pprint import pprint
from readyaml import readyaml


# ### Script generates webpages:
# * index.html
# * texts present in publication_metadata.yaml
# 
# ### templates in website-templates/ #####
# * base.html
# * contentpage.html
# * menu.html

"""
# #######TODO:####### 
* integrate css
# PAGES GENERATED
* one page per .docx
"""

thisfile_path = os.path.abspath(__file__)
thisfile_dir = os.path.dirname(thisfile_path) # parentdir
print(thisfile_path)

# metadata of publication from YAML file
metadata = readyaml(thisfile_dir + '/' + 'publication_metadata.yaml')
# pprint(metadata)
# TODO: populate dictionary with path to html files
for text in metadata['TOC']:
    try:
        docx = text['docx']
        html = thisfile_dir + '/html/' + docx.replace('.docx', '.html')
        print(html)
    except Exception as e:
        print('Error with {} in {}'.format(e, text))
        sys.exit(1)
    # TODO convert to HTML in convert.py script
    # print (html_file)
    
    print(text)
    

# env = Environment()  # loads templates from the file system
# # Loads templates from the current directory
# env.loader = FileSystemLoader(thisfile_dir + '/website-templates')

# tmpl = env.get_template('contentpage.html')
# tmpl_render = tmpl.render(mytitle=metadata['Title'],
#                           TOC=metadata['TOC'],
#                           content="testing",)
# # print(tmpl_render)


# # # save
# with open("website/index.html", "w") as index:
#   index.write(tmpl_render)









