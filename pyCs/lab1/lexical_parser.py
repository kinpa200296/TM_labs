import json
from token_parser import TokenParser
import os


class LexicalParser(object):

    def __init__(self):
        self.token_parsers = []
        self.special_chars = []
        cur_dir = os.path.dirname(__file__)
        self.__load_tokens(os.path.join(cur_dir, 'tokens.json'))
        self.__load_special_chars(os.path.join(cur_dir, 'special_chars.json'))
        self.__cur_token_str = u''
        self.__tokens = []
        self.__line_num = 0
        self.__column_num = 0

    def __load_tokens(self, filename):
        with open(filename, 'r') as tokens_file:
            tokens_info = json.load(tokens_file)
        for token_info in tokens_info:
            self.token_parsers.append(TokenParser(token_info.keys()[0],
                                                  token_info.values()[0]))

    def __load_special_chars(self, filename):
        with open(filename, 'r') as special_chars_file:
            self.special_chars = json.load(special_chars_file)

    def print_all_tokens(self):
        for token_parser in self.token_parsers:
            print token_parser

    def match_token(self, s):
        if not isinstance(s, unicode):
            raise ValueError('argument should be a unicode string')
        for token_parser in self.token_parsers:
            m = token_parser.match(s)
            if m is not None:
                return m

    def __create_token(self, next_char):
        if not isinstance(next_char, unicode):
            raise ValueError('argument should be a unicode string')
        if self.__cur_token_str != u'':
            token = self.match_token(self.__cur_token_str)
            token.line = self.__line_num
            token.column = self.__column_num
            self.__tokens.append(token)

        self.__cur_token_str = next_char

    def __can_connect_special_char(self, c):
        return c == u'<' or c == u'>' or c == u'='

    def parse(self, filename):
        self.__cur_token_str = u''
        self.__tokens = []
        self.__line_num = 0
        with open(filename, 'r') as f:
            for line in f:
                self.__line_num += 1
                self.__column_num = 0
                is_parsing_string = False
                prev_char = u''
                for char in line:
                    self.__column_num += 1
                    char = unicode(char)
                    if char == u'\n':
                        self.__create_token(u'')
                    elif char == u'\"':
                        if is_parsing_string:
                            self.__cur_token_str += char
                            self.__create_token(u'')
                            is_parsing_string = False
                        else:
                            self.__create_token(char)
                            is_parsing_string = True
                    elif is_parsing_string:
                        self.__cur_token_str += char
                    elif char == u' ' or char == u'\t':
                        self.__create_token(u'')
                    elif char in self.special_chars:
                        if prev_char in self.special_chars:
                            if self.__can_connect_special_char(prev_char) and self.__can_connect_special_char(char):
                                self.__cur_token_str += char
                            else:
                                self.__create_token(char)
                        else:
                            if self.__cur_token_str == u'':
                                self.__cur_token_str += char
                            else:
                                self.__create_token(char)
                    else:
                        if prev_char in self.special_chars:
                            self.__create_token(char)
                        else:
                            self.__cur_token_str += char
                    prev_char = char
                self.__create_token(u'')
        return self.__tokens


if __name__ == '__main__':
    lexer = LexicalParser()
    # lexer.print_all_tokens()
    # print lexer.special_chars
    # print lexer.match_token(u'12')
