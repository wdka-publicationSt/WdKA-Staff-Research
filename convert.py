#!/usr/bin/env python3
import sys
import os
import subprocess
import shlex
from argparse import ArgumentParser

def pandoc_convert(_from, _to, inputfile):
    tmpfile = os.path.abspath('./.content') # path of tempfile
    open(tmpfile, 'a').close() # write empty tempfile to disk
    pandoc_cmd = 'pandoc {input} -f {form} -t {to} -o {output}'.format(
        form=_from,
        to=_to,
        input=inputfile,
        output=tmpfile)
    pandoc_cmd_list = shlex.split(pandoc_cmd)
    try:
        subprocess.call(pandoc_cmd_list)
        with open(tmpfile, 'r') as tempfile_r:
            output = tempfile_r.read()
        return(output)
    except Exception as e:
        print('Error with {} while converting {}'.format(e, inputfile))
        sys.exit(1)


if __name__ == '__main__':

    parser = ArgumentParser(prog=sys.argv[0],
                            usage='%(prog)s  --to html OR icml',
                            description="Simple script, \
                            wrapper to pandoc, \
                            that converts docx files to other format")

    parser.add_argument("--to",
                        choices=['html', 'icml'],
                        default='html',
                        help="convert to format: html or icml")

    args = parser.parse_args()

    dir_parent = os.path.dirname((os.path.abspath(__file__)))
    dir_parent_ls = os.listdir(dir_parent)

    formats = {f: {
        "format": f,
        "dir": dir_parent + "/" + f}
        for f in ["docx", "html", "icml"]}

    def ls_dir(d):
        visible_files = [f for f in os.listdir(d) if f[0] is not '.']
        return visible_files


    for input_file in ls_dir(formats['docx']['dir']):
        output_file = "{}/{}".format(formats[args.to]['dir'],
                                     input_file.replace('docx', args.to))
        input_file = "{}/{}".format(formats['docx']['dir'], input_file)
        print(input_file, output_file)

        pandoc_cmd = 'pandoc {input} --from docx --to {to} \
            --output {output}'.format(input=input_file,
                                      to=args.to,
                                      output=output_file)

        pandoc_cmd_list = shlex.split(pandoc_cmd)
        subprocess.call(pandoc_cmd_list)