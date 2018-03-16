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

def test_b64enc():
    input = 'foo'
    r = ktpl.filters.b64enc(input)
    assert type(r) is str
    assert r == 'Zm9v'

def test_b64dec():
    input = 'Zm9v'
    r = ktpl.filters.b64dec(input)
    assert type(r) is str
    assert r == 'foo'
