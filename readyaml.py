import yaml
from pprint import pprint


def readyaml(yamlfile):
    stream = open(yamlfile, 'r')
    try:
        metadata = yaml.load(stream)
        pprint(metadata)
    except Exception as e:
        print(e)
        print("Error: Missformated YAML")


if __name__ == '__main__':
    readyaml('publication_metadata.yaml')

