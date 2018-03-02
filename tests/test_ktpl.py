from __future__ import absolute_import
import sys
from docopt import docopt
from .context import ktpl

doc = ktpl.cli.__doc__

args = docopt(doc)
args['--template'] = True
print(args)

ktpl.cli.main(args)


def test_template():
    args = docopt(doc)
    args['--template'] = True
    ktpl.cli.main(args)

