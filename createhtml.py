#!/usr/bin/env python3
import os
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
# from jinja2 import Template
from pprint import pprint
from readyaml import readyaml

thisfile_path = os.path.abspath(__file__)
thisfile_dir = os.path.dirname(thisfile_path)
print(thisfile_path)

# metadata of publication from YAML file
metadata = readyaml('publication_metadata.yaml')
# pprint(metadata)
# TODO: populate dictionary with path to html files


# Template
# TODO: include CSS + JS script

env = Environment()  # loads templates from the file system
# Loads templates from the current directory
env.loader = FileSystemLoader('./website-templates')

tmpl = env.get_template('contentpage.html')
tmpl_render = tmpl.render(mytitle=metadata['Title'],
                          TOC=metadata['TOC'],
                          content="testing",)
print(tmpl_render)


# # save
with open("index.html", "w") as index:
	index.write(tmpl_render)




"""
TODO: 
# PAGES GENERATED
* index.html
* one page per .docx
# ELEMENTS GENERATED
* menu

#### templates in website-templates/ #####
base.html
contentpage.html
menu.html

"""





# # CONTROL STRUCTURES: loops and if conditions
# # http://jinja.pocoo.org/docs/2.10/templates/#list-of-control-structures
# users_html = Template('''<ul>
#   {% for user in users  %}
#     <li class="user" id="user_{{ user|lower }}">
#         {% if user[0] == "A" %}
#             <i>{{ user[0] }}</i>{{ user[1:] }}
#         {% else %}
#             <b>{{ user[0] }}</b>{{ user[1:] }}
#         {% endif %}
#     </li>
#   {% endfor %}
#   </ul>
# ''')

