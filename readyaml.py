import yaml
import sys
from pprint import pprint


def readyaml(yamlfile):
    stream = open(yamlfile, 'r')
    try:
        metadata = yaml.load(stream)
        return metadata
    except Exception as e:
        print(e)
        print("Error: Missformated YAML")


def TOC_populate(parent_dir, metadata_dict):
    '''
    Function updates metadata_dict['TOC'] with full path of dirs:
    docx, html, icml
    '''
    for text_entry in metadata_dict['TOC']:
        try:
            docx = parent_dir + '/docx/' + text_entry['docx']
            html = docx.replace('/docx/', '/html/').replace('.docx', '.html')
            icml = docx.replace('/docx/', '/icml/').replace('.docx', '.icml')
            txt = docx.replace('/docx/', '/txt/').replace('.docx', '.txt')
            # for text entry in TOC
            # add full path of html, icml, docx files
            text_entry['html'] = html
            text_entry['docx'] = docx
            text_entry['icml'] = icml
            text_entry['txt'] = txt
        except Exception as e:
            print('Error with {} in {}'.format(e, text_entry))
            sys.exit(1)
    return metadata_dict


if __name__ == '__main__':
    metadata = readyaml('publication_metadata.yaml')
    pprint(metadata)
