import base64
from slugify import slugify

def b64enc(input):
    return base64.b64encode(input)

def b64dec(input):
    return base64.b64decode(input)

def slugify_string(input):
    return slugify(input)