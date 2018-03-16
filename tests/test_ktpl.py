from __future__ import absolute_import
import sys
from docopt import docopt
from .context import ktpl

doc = ktpl.cli.__doc__

# args = docopt(doc)

def test_template():
    args = docopt(doc, ['--template', 'tests'])
    foo = ktpl.cli.main(args)
    assert foo is None

