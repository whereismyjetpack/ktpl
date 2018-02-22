"""
Usage:
  ktpl [options] [<folder>...]

Options:
  --delete -d                  Delete, instead of apply templated manifests
  --template -t                Template manifests, and print to screen 
"""
from __future__ import absolute_import
from .__version__ import __version__
from .kube import run_kube_command
from docopt import docopt
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined
from .filters import b64dec, b64enc, slugify_string
import yaml
import re
import os


def main(arguments):
    """
    main
    """
    variables = {}
    if arguments['--delete']:
        kube_method = 'delete'
    else:
        kube_method = 'apply'

    if arguments['<folder>']:
        folders = arguments['<folder>']
    else:
        folders = [f for f in sorted(os.listdir(os.getcwd())) if os.path.isdir(f)]
        # folders.append(os.getcwd())

    extensions = ('.yaml', 'yml')

    values_files = find_values_files('.', extensions, "values")
    secret_values = find_values_files('.', 'secret', "values")
    [ variables.update(process_variables(file)) for file in values_files ]
    [ variables.update(process_variables(file)) for file in secret_values ]
    
    def add_secret_files(filename):
        if os.path.isfile(filename + ".secret"):
            variables.update(process_variables(filename + ".secret"))
            return True
        else:
            return False

    for folder in folders:
        deployment_values = find_values_files('.', extensions, folder)
        secret_values = find_values_files('.', 'secret', folder)
        template_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(folder), followlinks=True) for f in fn if f.endswith('.tpl') ]

        if not template_files:
            continue

        if deployment_values:
            for filename in deployment_values:
                if add_secret_files(filename):
                    secret_values.remove(filename + ".secret")
                variables.update(process_variables(filename))
                process_output(variables, template_files, arguments, kube_method, folder, filename=filename)
        if secret_values:
            for filename in secret_values:
                variables.update(process_variables(filename))
                process_output(variables, template_files, arguments, kube_method, folder, filename=filename)
        else:
            process_output(variables, template_files, arguments, kube_method, folder)

def process_output(variables, template_files, arguments, kube_method, folder, filename=None):
    output = [ proceess_template(os.path.basename(os.path.abspath(file_path)), os.path.dirname(os.path.abspath(file_path)), variables) for file_path in template_files ] 
    output = '\n'.join(output)
    if arguments['--template']:
        print(output)
    else:
        if filename:
            print('\nSending Manifests from %s for %s to kubectl...') % (folder, filename)
        else:
            print('\nSending Manifests from %s to kubectl...') % (folder)
        run_kube_command(output, kube_method)

def find_values_files(folder, extensions, pattern):
    pattern = re.compile(pattern)
    return [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(extensions) and pattern.match(file)]


def process_variables(input_file):
    """
    Processes variables
    """

    with open(input_file, 'r') as f:
        current_file = f.read()
    
    yaml_load = yaml.safe_load(current_file)
    if isinstance(yaml_load, dict):
        return yaml_load
    else:
        # TODO fix this 
        return {}

def proceess_template(template_file, searchpath, variables):
    loader = FileSystemLoader(searchpath=searchpath)
    env = Environment(loader=loader, undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
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