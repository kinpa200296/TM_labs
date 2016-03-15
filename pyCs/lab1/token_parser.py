import re
from token import Token


class TokenParser(object):

    def __init__(self, token_name, templates):
        if not isinstance(token_name, unicode):
            raise ValueError('token_name should be a unicode string')
        if not isinstance(templates, list):
            raise ValueError('templates should be a list')
        for template in templates:
            if not isinstance(template, unicode):
                raise ValueError('templates elements should all be unicode strings')
        self.token_name = token_name
        self.templates = templates

    def __repr__(self):
        return self.__str__().__repr__()

    def __str__(self):
        return '"{token_name}":\n\t{templates}'.format(token_name=self.token_name,
                                                       templates="\n\t".join(self.templates))

    def match(self, s):
        if not isinstance(s, unicode):
            raise ValueError('argument should be a unicode string')
        for template in self.templates:
            regexp = "^{template}$".format(template=template)
            m = re.match(regexp, s)
            if m is not None:
                return Token(self.token_name, s)
