import re
import os

class Lexer:
    def __init__(self, code,file="core/out.txt"):
        self.__code = code
        self.output_file = file
        self.keywords = r'\b(subprogram|pentru|daca|atunci|altfel|executa|cat_timp|returneaza|sf_daca|sf_subprogram|adevarat|fals|scrie|repeta|pana_cand|sf_pentru|sf_cat_timp|citeste|div|mod)\b'
        self.operators = r'(\+|-|\*|/|<--|div|mod|\[|\]|\(|\))'
        self.identifiers = r'([a-zA-Z_][a-zA-Z0-9_]*)'
        self.integers = r'-?\b\d+\b'  
        self.reals = r'-?\b\d+\.\d+\b'
        self.whitespaces = r'\s+'  
        self.token_pattern = f'{self.operators}'

    def __tokenize(self):
        try:
            with open(self.output_file, 'w') as g:
                for line in self.__code.split("\n"):
                    line = line.strip()  
                    tokens = re.split(self.token_pattern, line)
                    tokens = [token for token in tokens if token.strip()]
                    for token in tokens:
                        g.write(f"{token}\n")
        except Exception as e:
            print(f"An error occurred: {e}")

    def __analyze(self):
        with open(self.output_file) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if re.match(self.keywords, line):
                    pass
                elif re.match(self.identifiers, line):
                    pass
                elif re.match(self.reals, line):
                    pass
                elif re.match(self.integers, line):
                    pass
                elif re.match(self.operators, line):
                    pass
                else:
                        indexing = dict(enumerate(self.__code.split("\n"), start=1))
                        for nr, val in indexing.items():
                            if line in val:
                                return f"Error at line {nr}: {val}"
        return ""
    def f(self):
        self.__tokenize()
        return self.__analyze()