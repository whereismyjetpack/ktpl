# ktpl

Utility to template Kubernetes Resource Definitions using the jinja2 templating engine, then apply or delete the templated resources

[![Build Status](https://travis-ci.org/whereismyjetpack/ktpl.svg?branch=master)](https://travis-ci.org/whereismyjetpack/ktpl)

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


### Directory Structure:

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

### Variable precidence:
{{folder_name}}.yml  
values.yml  
{{folder_name}}/values.yml  

### Examples:
```
1.) ktpl
- processes folder-1/template.yml.tpl, and folder-2/template.yml.tpl. processes folder-2/template.yml.tpl twice. once with values from folder-2.yml, and once with values from folder-2-customer-b.yml. 
2.) ktpl folder-1
- processes folder-1/template.yml.tpl with values from values.yml, values.yml.secret, and folder-1.yml. variables from folder-1.yml will override defaulty variables set in values.yml
3.) ktpl --template
- processes the same as example 1, but prints the template to screen instead of sending to kubectl
```




