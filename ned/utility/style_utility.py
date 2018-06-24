def bold(text):
    return '*' + text + '*'

def italics(text):
    return '_' + text + '_'

def quoted(text):
    return '>' + text

def indent(text, num_indents=1):
    return '\t'*num_indents + text