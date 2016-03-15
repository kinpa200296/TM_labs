from lab1 import LexicalParser


if __name__ == '__main__':
    lexer = LexicalParser()
    tokens = lexer.parse('code.in')
    error_cnt = 0
    for token in tokens:
        if token.name == 'unknown':
            error_cnt += 1
    if error_cnt != 0:
        print 'Errors found. Total: {quantity}'.format(quantity=error_cnt)
        for token in tokens:
            if token.name == 'unknown':
                print token.show_as_invalid()
        with open('code.out', 'w') as f:
            f.writelines('Errors found. Total: {quantity}\n'.format(quantity=error_cnt))
            for token in tokens:
                if token.name == 'unknown':
                    f.writelines(token.show_as_invalid()+'\n')
    else:
        token_tables = {}
        for token in tokens:
            if token_tables.has_key(token.name):
                token_tables[token.name].add(token.value)
            else:
                token_tables[token.name] = set()
                token_tables[token.name].add(token.value)
        for token_name in token_tables:
           print token_name + 's table:\n\t'+'\n\t'.join(token_tables[token_name])
        with open('code.out', 'w') as f:
            # f.writelines([t.__str__()+'\n' for t in tokens])
            for token_name in token_tables:
                f.writelines(token_name + 's table:\n\t'+'\n\t'.join(token_tables[token_name])+'\n')
