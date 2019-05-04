#!/usr/bin/env python3
import os
import sys
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
# from jinja2 import Template
from pprint import pprint


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



def jinja_env(tmpl_dir):
    env = Environment()  # loads templates from the file system
    # Loads templates from the current directory
    env.loader = FileSystemLoader(tmpl_dir)
    return env

def jinja_render_template(env, tmpl_file):
    tmpl = env.get_template(tmpl_file)
    tmpl_render = tmpl.render(mytitle=metadata['Title'],
                              TOC=metadata['TOC'],
                              content="testing",)
    return(tmpl_render)
# print(tmpl_render)


# # # save
# with open("website/index.html", "w") as index:
#   index.write(tmpl_render)









