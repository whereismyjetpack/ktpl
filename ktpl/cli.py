# -*- coding: utf-8 -*-
"""
Usage:
  ktpl [--template-file=<file>...] [--input-file=<file>...] ( [--template] | [--delete] ) [--environment] [<folder>...]
 
Options:
  --delete -d                         Delete, instead of apply templated manifests
  --template -t                       Template manifests, and print to screen
  --environment -e                    Consider environment when processing variables
  --input-file=<file>... -i           Path to input file(s) to process instead of the defaults
  --template-file=<file>...           Path to template file(s) to process instead of the defaults
"""
from __future__ import absolute_import
import re
import os
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from docopt import docopt
from ktpl import __version__
from .kube import run_kube_command
from .filters import b64dec, b64enc, slugify_string


def main(arguments):

    variables = {}
    extensions = ('.yaml', '.yml')
    template_extensions = ('.tpl')
    secret_extension = '.secret'
    folders = []

    def has_secret_file(filename):
        """
        Checks for a secret deployment file, returns True if found
        False if not found
        """
        secret_file = filename + secret_extension
        if os.path.isfile(secret_file):
            return True

        return False

    if arguments['--delete']:
        kube_method = 'delete'
    else:
        kube_method = 'apply'

    if arguments['--environment']:
        variables = merge_variables(variables, dict(os.environ.items()))

    # Update variables dictionary.
    # if input-file is specified, we don't read in values files.
    if arguments['--input-file']:
        for filename in arguments['--input-file']:
            variables = merge_variables(variables, process_variables(filename))
    else:
        values_files = find_values_files('.', extensions, "values")
        secret_values = find_values_files('.', secret_extension, "values")
        all_values = values_files + secret_values
        for filename in all_values:
            variables = merge_variables(variables, process_variables(filename))

    if arguments['<folder>']:
        folders = arguments['<folder>']
        for folder in folders:
            if not os.path.isdir(folder):
                print('Can not process %s, folder not found' % folder)
                folders.remove(folder)

    elif arguments['--template-file']:
        process_output(variables, arguments['--template-file'], arguments, kube_method)
    else:
        folders = [f for f in sorted(os.listdir(os.getcwd())) if os.path.isdir(f)]

    # TODO if no folders, maybe send a message to the user?
    for folder in folders:
        deployment_vars = find_values_files(folder, extensions, "values")
        for filename in deployment_vars:
            variables = merge_variables(process_variables(filename), variables)
        deployment_values = find_values_files('.', extensions, folder)
        secret_values = find_values_files('.', secret_extension, folder)
        template_files = [ os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(folder), followlinks=True) for f in fn if f.endswith(template_extensions) ]

        # TODO if passed a folder, and there are no template files we should display a message
        # if we are looking in all subdirs, maybe not? maybe part of debug?
        if not template_files:
            continue

        if deployment_values:
            for filename in deployment_values:
                this_vars = {}
                secret_vars = {}
                if has_secret_file(filename):
                    secret_vars = merge_variables(variables, process_variables(filename + secret_extension))
                    secret_values.remove(filename + secret_extension)
                this_vars = merge_variables(variables, process_variables(filename))
                this_vars = merge_variables(this_vars, secret_vars)
                process_output(this_vars, template_files, arguments, kube_method)
        elif secret_values:
            for filename in secret_values:
                this_vars = {}
                this_vars = merge_variables(variables, process_variables(filename))
                process_output(this_vars, template_files, arguments, kube_method)
        else:
            process_output(variables, template_files, arguments, kube_method)
    

def merge_variables(x, y):
    """
    Take two dictonaries, and merge them
    Second argument gets merged into the first.
    """
    z = x.copy()
    z.update(y)
    return z

def process_output(variables, template_files, arguments, kube_method):
    """
    Proccess template files, and either print to screen, or pass to kubectl
    """
    output = ""
    for file_path in template_files:
        output = output + "\n" + process_template(os.path.basename(os.path.abspath(file_path)),
                                  os.path.dirname(os.path.abspath(file_path)), variables)

    if arguments['--template']:
        print(output)
    else:
        run_kube_command(output, kube_method)

def find_values_files(folder, extensions, pattern):
    """
    Finds variables based off a folder, extension, and pattern match
    Returns a list of found files.
    """
    pattern = re.compile(pattern)
    return [ 
        os.path.join(folder, filename) 
        for filename in os.listdir(folder)
            if filename.endswith(extensions)
                and pattern.match(filename) ]


def process_variables(input_file):
    """
    Takes a variable file as an argument, returns a dictionary
    of variables for that file
    """

    with open(input_file, 'r') as f:
        current_file = f.read()

    yaml_load = yaml.safe_load(current_file)
    if isinstance(yaml_load, dict):
        return yaml_load
    else:
        return {}

def process_template(template_file, searchpath, variables):
    """
    Takes a template file, and variables and returns the templated version
    of that template
    """
    loader = FileSystemLoader(searchpath=searchpath)
    env = Environment(loader=loader, undefined=StrictUndefined, trim_blocks=False, lstrip_blocks=False)
    env.filters['b64dec'] = b64dec
    env.filters['b64enc'] = b64enc
    env.filters['slugify_string'] = slugify_string
    template = env.get_template(template_file)

    return template.render(variables)

def cli():
    arguments = docopt(__doc__, version=__version__)
    main(arguments)

if __name__ == '__main__':
    cli()
