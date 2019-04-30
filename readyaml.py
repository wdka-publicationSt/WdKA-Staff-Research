import yaml
from pprint import pprint


def readyaml(yamlfile):
    stream = open(yamlfile, 'r')
    try:
        metadata = yaml.load(stream)
        return metadata
    except Exception as e:
        print(e)
        print("Error: Missformated YAML")


if __name__ == '__main__':
    metadata = readyaml('publication_metadata.yaml')
    pprint(metadata)
