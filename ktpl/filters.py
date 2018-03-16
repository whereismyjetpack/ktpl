import base64
from slugify import slugify

def b64enc(input):
    output = base64.b64encode(input.encode())
    return output.decode()

def b64dec(input):
    output = base64.b64decode(input.encode())
    return output.decode()

def slugify_string(input):
    return slugify(input)