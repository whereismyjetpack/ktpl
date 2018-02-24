# ktpl

Command line utility to template out Kubernetes Resource Definitions from jinja2 templates, and apply or delete them

## Getting Started
`pip install git+https://github.com/whereismyjetpack/ktpl.git@master`

### Prerequisites

`kubectl`

### Usage
```
Usage:
  ktpl [options] [<folder>...]
  ktpl [options] [--input-file=<file>]...
  ktpl [options] [--template-file=<file>]...

Options:
  --delete -d                      Delete, instead of apply templated manifests
  --template -t                    Template manifests, and print to screen
  --environment -e                 Consider environment when processing variables
  --input-file=<file> -i           Path to input file(s) to process instead of the defaults
  --template-file=<file> -t        Path to template file(s) to process instead of the defaults
```


