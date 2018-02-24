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


Directory Structure:

```.
├── folder-1
│   ├── template.yml.tpl
│   └── values.yml <- "defaulty" variables for resources in this folder
├── folder-2
│   ├── template.yml.tpl
│   └── values.yml <- "defaulty" variables for resources in this folder
├── values.yml <--- global variables used in all resources
├── folder-2.yml <--- values that get added only for resources in folder-2
├── folder-2-customer-b.yml <--- a second set of values, that will get appied to resources in folder-2
├── folder-1.yml <---values that get added only for resources in folder-1
└── values.yml.secret <--- global variables, that will be merged with values.yml. good for using `git-crypt` to encrypt only secret portions of your variables
```

Variable precidence:

- {{folder_name}}.yml

- values.yml

- {{folder_name}}/values.yml

Examples:

`ktpl`  # will template all resources from `folder-1` and `folder-2`. `folder-2` will be applied twice, the templated resources will be passed to `kubectl apply`

`ktpl folder-1` # will template only resources from `folder-1`, and the templated resources will be passed to `kubectl apply`

`ktpl --template` # will do as example 1, but instead of passing to `kubectl apply` the results will be printed to screen




