#!/usr/bin/env python3
import os
import sys
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
# from jinja2 import Template
from pprint import pprint


# ### Script generates webpages:
# * texts entries present in publication_metadata.yaml
# 
# ### templates in website-templates/ #####
# * base.html
# * contentpage.html
# * menu.html


def jinja_env(tmpl_dir):
    env = Environment()  # loads templates from the file system
    # Loads templates from the current directory
    env.loader = FileSystemLoader(tmpl_dir)
    return env


def jinja_render_template(env, tmpl_file, title, content, TOC='', publication_title='', css=False):
    tmpl = env.get_template(tmpl_file)
    tmpl_render = tmpl.render(publication_title=publication_title,
                              mytitle=title,
                              TOC=TOC,
                              content=content,
                              css=css)
    return(tmpl_render)







