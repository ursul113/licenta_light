import ply.lex as lex
import ply.yacc as yacc
import os
class Parser:
    def __init__(self, code, keyboard_input,file="core/translated.php"):
        self.lexer = None
        self.parser = None
        self.result = None
        self.translated_code = []
        self._build_lexer()
        self._build_parser()
        self.code = code
        self.input=keyboard_input
        self.__out = open(file, "w")

    reserved = {
        'daca': 'IF',
        'altfel': 'ELSE',
        'adevarat': 'TRUE',
        'fals': 'FALSE',
        'sf_daca': 'ENDIF',
        'atunci': 'ATUNCI',
        'cat_timp': 'WHILE',
        'sf_cat_timp': 'ENDWHILE',
        'executa': 'EXECUTA',
        'pentru': 'FOR',
        'sf_pentru': 'ENDFOR',
        'scrie': 'PRINT',
        'repeta': 'REPEAT',
        'pana_cand': 'UNTIL',
        'subprogram': 'FUNCTION',
        'sf_subprogram': 'ENDFUNCTION',
        'returneaza': 'RETURN',
        'div': 'DIV',
        'mod': 'MOD',
        'citeste': 'READ'
    }

    tokens = (
        'CONST',
        'ID',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'ASSIGN',
        'LPAREN',
        'RPAREN',
        'GEQUAL',
        'LEQUAL',
        'EQUAL',
        'NEQUAL',
        'LOWER',
        'GREATER',
        'COMMA',
    ) + tuple(reserved.values())

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_ASSIGN = r'<--'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_GEQUAL = r'>='
    t_LEQUAL = r'<='
    t_EQUAL = r'='
    t_LOWER = r'<'
    t_GREATER = r'>'
    t_NEQUAL =r'!='
    t_COMMA = r','

    def t_CONST(self, t):
        r'0|-{0,1}[1-9][0-9]*'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    t_ignore = ' \t\n'

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def p_error(self,p):
        err=f"Syntax error in input! Token: {p}"
        if p:
            err+=f"Unexpected token: {p.type} with value {p.value} at line {p.lineno}"
            self.__out.close()
        raise ValueError(err)

    def _build_lexer(self):
        self.lexer = lex.lex(module=self)

    def p_program(self, p):
        """program : func_l_op l_op
                   | l_op"""
        if len(p) == 3:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]

    def p_l_op(self, p):
        """l_op : op
                | op l_op"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_func_l_op(self, p):
        """func_l_op : func
                     | func func_l_op"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_ar_op(self, p):
        """ar_op : add
                 | mul
                 | sub
                 | div
                 | rdiv
                 | mod"""
        p[0] = p[1]

    def p_add(self, p):
        """add : ID PLUS ID
               | CONST PLUS ID
               | ID PLUS CONST
               | CONST PLUS CONST"""
        
        if isinstance(p[1], str) and p[1] not in self.reserved and not p[1].isdigit():
            p[1] = f"${p[1]}"
        if isinstance(p[3], str) and p[3] not in self.reserved and not p[3].isdigit():
            p[3] = f"${p[3]}"
        p[0] = f"{p[1]} + {p[3]}"

    def p_sub(self, p):
        """sub : ID MINUS ID
               | CONST MINUS ID
               | ID MINUS CONST
               | CONST MINUS CONST"""
        
        if isinstance(p[1], str) and p[1] not in self.reserved and not p[1].isdigit():
            p[1] = f"${p[1]}"
        if isinstance(p[3], str) and p[3] not in self.reserved and not p[3].isdigit():
            p[3] = f"${p[3]}"
        p[0] = f"{p[1]} - {p[3]}"

    def p_mul(self, p):
        """mul : ID TIMES ID
               | CONST TIMES ID
               | ID TIMES CONST
               | CONST TIMES CONST"""
        
        if isinstance(p[1], str) and p[1] not in self.reserved and not p[1].isdigit():
            p[1] = f"${p[1]}"
        if isinstance(p[3], str) and p[3] not in self.reserved and not p[3].isdigit():
            p[3] = f"${p[3]}"
        p[0] = f"{p[1]} * {p[3]}"

    def p_div(self, p):
        """div : ID DIV ID
               | CONST DIV ID
               | ID DIV CONST
               | CONST DIV CONST"""
        if isinstance(p[1], str) and p[1] not in self.reserved and not p[1].isdigit():
            p[1] = f"${p[1]}"
        if isinstance(p[3], str) and p[3] not in self.reserved and not p[3].isdigit():
            p[3] = f"${p[3]}"
        p[0] = f"intdiv({p[1]},{p[3]})"

    def p_rdiv(self, p):
        """rdiv : ID DIVIDE ID
                | CONST DIVIDE ID
                | ID DIVIDE CONST
                | CONST DIVIDE CONST"""
        
        if isinstance(p[1], str) and p[1] not in self.reserved and not p[1].isdigit():
            p[1] = f"${p[1]}"
        if isinstance(p[3], str) and p[3] not in self.reserved and not p[3].isdigit():
            p[3] = f"${p[3]}"
        p[0] = f"{p[1]} / {p[3]}"  

    def p_mod(self, p):
        """mod : ID MOD ID
               | CONST MOD ID
               | ID MOD CONST
               | CONST MOD CONST"""
        
        if isinstance(p[1], str) and p[1] not in self.reserved and not p[1].isdigit():
            p[1] = f"${p[1]}"
        if isinstance(p[3], str) and p[3] not in self.reserved and not p[3].isdigit():
            p[3] = f"${p[3]}"
        p[0] = f"{p[1]} % {p[3]}"  

    def p_attr(self, p):
        """attr : ID ASSIGN ID
                | ID ASSIGN CONST
                | ID ASSIGN ar_op
                | ID ASSIGN TRUE
                | ID ASSIGN FALSE
                | ID ASSIGN func_call"""
        p[0] = f"${p[1]} = {p[3]};"

    def p_ret_op(self, p):
        """ret_op : RETURN ID
                   | RETURN CONST
                   | RETURN ar_op
                   | RETURN func_call"""
        p[0] = f"return {'$'+p[2] if (isinstance(p[2], str) and p[2][0]!='$' and '(' not in p[2]) else p[2]};"

    def p_op(self, p):
        """op : ar_op
              | attr
              | write
              | read
              | func_call
              | repeat
              | ret_op
              | if
              | while
              | for
              """
        p[0] = p[1]

    def p_cond(self, p):
        """cond : TRUE
                | FALSE
                | cond_op"""
        if p[1] == 'adevarat':
            p[0] = 'true'
        elif p[1] == 'fals':
            p[0] = 'false'
        else:
            p[0] = p[1]

    def p_cond_op(self, p):
        """cond_op : ID LOWER ID
                   | ID LOWER CONST
                   | CONST LOWER ID
                   | CONST LOWER CONST
                   | ID GREATER ID
                   | ID GREATER CONST
                   | CONST GREATER ID
                   | CONST GREATER CONST
                   | ID LEQUAL ID
                   | ID LEQUAL CONST
                   | CONST LEQUAL ID
                   | CONST LEQUAL CONST
                   | ID GEQUAL ID
                   | ID GEQUAL CONST
                   | CONST GEQUAL ID
                   | CONST GEQUAL CONST
                   | ID EQUAL ID
                   | ID EQUAL CONST
                   | CONST EQUAL ID
                   | CONST EQUAL CONST
                   | ID NEQUAL ID
                   | ID NEQUAL CONST
                   | CONST NEQUAL ID
                   | CONST NEQUAL CONST
                   | ar_op LOWER ar_op
                   | ar_op GREATER ar_op
                   | ar_op LEQUAL ar_op
                   | ar_op GEQUAL ar_op
                   | ar_op EQUAL ar_op
                   | ar_op NEQUAL ar_op
                   | ar_op LOWER ID
                   | ar_op GREATER ID
                   | ar_op LEQUAL ID
                   | ar_op GEQUAL ID
                   | ar_op EQUAL ID
                   | ar_op NEQUAL ID
                   | ID LOWER ar_op
                   | ID GREATER ar_op
                  | ID LEQUAL ar_op
                  | ID GEQUAL ar_op
                  | ID EQUAL ar_op
                  | ID NEQUAL ar_op
                  | ar_op LOWER CONST
                  | ar_op GREATER CONST
                  | ar_op LEQUAL CONST
                  | ar_op GEQUAL CONST
                  | ar_op EQUAL CONST
                  | ar_op NEQUAL CONST
                  | CONST LOWER ar_op
                  | CONST GREATER ar_op
                  | CONST LEQUAL ar_op
                  | CONST GEQUAL ar_op
                  | CONST EQUAL ar_op
                  | CONST NEQUAL ar_op
        """
        a=p[1]
        if isinstance(p[1], str) and p[1][0] != '$' and not p[1][0].isdigit():
            p[1] = '$' + p[1]
        if isinstance(p[3], str) and p[3][0] != '$' and not p[3][0].isdigit():
            p[3] = '$' + p[3]
        if p[2] == '=':
            p[0] = f"{p[1]} == {p[3]}"
        else:
            p[0] = f"{p[1]} {p[2]} {p[3]}"

    def p_if(self, p):
        """if : IF cond ATUNCI l_op ENDIF
              | IF cond ATUNCI l_op ELSE l_op ENDIF"""
        if len(p) == 6:  
            body = "\n    ".join(p[4])  
            p[0] = f"if ({p[2]})\n{{\n{body}\n}}"

        elif len(p) == 8:  
            if_body = "\n    ".join(p[4])  
            else_body = "\n    ".join(p[6])  
            p[0] = f"if ({p[2]})\n{{\n{if_body}}}\n else\n{{\n{else_body}\n}}"

    def p_while(self, p):
        """while : WHILE cond EXECUTA l_op ENDWHILE"""
        body = "\n    ".join(p[4])  
        p[0] = f"while ({p[2]})\n{{\n{body}\n}}"

    def p_for(self, p):
        """for : FOR ID ASSIGN ID COMMA ID EXECUTA l_op ENDFOR
               | FOR ID ASSIGN CONST COMMA ID EXECUTA l_op ENDFOR
               | FOR ID ASSIGN ID COMMA CONST EXECUTA l_op ENDFOR
               | FOR ID ASSIGN CONST COMMA CONST EXECUTA l_op ENDFOR
               | FOR ID ASSIGN ID COMMA ID COMMA CONST EXECUTA l_op ENDFOR
               | FOR ID ASSIGN CONST COMMA ID COMMA CONST EXECUTA l_op ENDFOR
               | FOR ID ASSIGN ID COMMA CONST COMMA CONST EXECUTA l_op ENDFOR
               | FOR ID ASSIGN CONST COMMA CONST COMMA CONST EXECUTA l_op ENDFOR"""
        loop_var = '$'+p[2]
        start = p[4]
        end = p[6]
        body = "\n    ".join(p[len(p) - 2])  
        if len(p) == 10:
            step = 1
            sgn="<="
        else:
            step = p[8]
            if int(step)>=0:
                sgn="<="
            else:
                sgn=">="
        p[0] = f"for ({loop_var} = {start}; {loop_var} {sgn} {end}; {loop_var} += {step})\n{{\n{body}\n}}"

    def p_repeat(self,p):
        """repeat : REPEAT l_op UNTIL cond_op"""
        body = "\n    ".join(p[2])
        cond=p[4]
        p[0] = f"do \n{{\n{body}\n}} while (!({cond}));"

    def p_read(self,p):
        """read : READ LPAREN l_param RPAREN"""
        format="%f"*len(p[3])
        vars=",".join(["$"+str(i) for i in p[3]])
        p[0]=f"sscanf(\"{self.input}\",\"{format}\",{vars});"

    def p_write(self, p):
        """write : PRINT LPAREN l_a_param RPAREN"""
        params = []
        for param in p[3]:
            if isinstance(param, str) and param not in self.reserved and param[0]!='$' and "(" not in param and not param[0].isdigit():
                param = f"${param}"
            params.append(str(param))

        
        p[0] = f"echo {', '.join(params)};"

    def p_func(self, p):
        """func : FUNCTION ID LPAREN l_param RPAREN l_op ENDFUNCTION
                | FUNCTION ID LPAREN RPAREN l_op ENDFUNCTION"""
        func_name = p[2]
        if len(p) > 7:
            parameters = p[4]
            body = "\n    ".join(p[6])
        else:
            parameters = []
            body = "\n    ".join(p[5])

        p[0] = f"function {func_name}({', '.join(['$' + param for param in parameters])})\n{{\n{body}\n}}"

    def p_func_call(self, p):
        """func_call : ID LPAREN l_a_param RPAREN
                      | ID LPAREN RPAREN"""
        if(len(p)==5):
            params = ", ".join([f"${param}" if (isinstance(param, str) and param[0]!='$') else str(param) for param in p[3]])
        else:
            params=""
        p[0] = f"{p[1]}({params});"

    def p_l_param(self, p):
        """l_param : ID
                   | ID COMMA l_param"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_l_a_param(self, p):
        """l_a_param : CONST
                     | ID
                     | ar_op
                     | func_call
                     | l_a_param COMMA CONST
                     | l_a_param COMMA ID"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def parse(self):
        self.result = self.parser.parse(self.code, lexer=self.lexer)
        if self.result is not None:
            self.__out.write("<?php\n")
            self.__out.write("\n".join(self.result))
        self.__out.close()

    def _build_parser(self):
        self.parser = yacc.yacc(module=self)
