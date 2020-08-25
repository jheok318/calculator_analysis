# coding: utf-8

import os.path
import ply.lex as lex
import ply.yacc as yacc
import json

from __init__ import Node


class Parser(object):

    tokens = ()
    precedence = ()

    def __init__(self):

        self._fun_list = []
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__

        self.tabmodule = modname + "_" + "parsetab"

        lex.lex(module=self)

        yacc.yacc(module=self,
                  method="LALR",
                  tabmodule=self.tabmodule,
                  write_tables=True,
                  optimize=True)

    def parse(self, query):

        # remove comment
        r_query = []
        for line in query.split('\n'):
            if line.lstrip()[:2] == '--':
                line = ''
            r_query.append(line)
        query = '\n'.join(r_query)

        # yacc.parse(query)

    # def token_test(self, query):
    #     lex.Lexer.input(query)
    #     while 1:
    #         tok = lex.Lexer.token(query)
    #         if not tok: break
    #         print(tok)

    # noinspection PyMethodMayBeStatic
    def run(self):
        query = input('calc> ')
        yacc.parse(query)
        # self.debugNode(query)


class CalcParser(Parser):
    # Lex
    tokens = (
        'STRING', 'NUMBER',
        'PLUS', 'MINUS', 'MULTI', 'DIVIDE', 'EQUALS',
        'LPAREN', 'RPAREN',
        'SEMI',)

    t_SEMI = r';'
    t_MULTI = r'\*'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_DIVIDE = r'/'
    t_EQUALS = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_STRING = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # noinspection PyMethodMayBeStatic
    def t_NUMBER(self, t):
        # 소수점 지원
        r"""[\d]+[.]?[\d]*"""
        return t

    # noinspection PyMethodMayBeStatic
    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    # noinspection PyMethodMayBeStatic
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    t_ignore = " \t"

    ###############################################################################################

    # Yacc

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTI', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    start = 'calc_grammar'

    def p_calc_grammar(self, p):
        """calc_grammar : expr SEMI"""

        self.nodeRoot = Node("CONTAINER", None, "_root")
        self.nodeRoot.children.append(p[1])
        node = Node("calc_END", None, ";")
        self.nodeRoot.children.append(node)

    # noinspection PyMethodMayBeStatic
    def p_expr(self, p):
        """expr : operation_expression"""

        node = Node("CONTAINER", None, "_expr")
        node.children.append(p[1])
        p[0] = node

    # noinspection PyMethodMayBeStatic
    def p_operation_expression(self, p):
        """operation_expression : expr PLUS expr
                                | expr MINUS expr
                                | expr MULTI expr
                                | expr DIVIDE expr
                                | expr EQUALS expr
                                """

        node = Node("OPERATION", None, p[2])
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

    # noinspection PyMethodMayBeStatic
    def p_group(self, p):
        """expr : LPAREN expr RPAREN"""

        node = Node("CONTAINER", None, "_expr")
        node.children.append(Node("KEYWORD", None, "("))
        node.children.append(p[2])
        node.children.append(Node("KEYWORD", None, ")"))
        p[0] = node

    # noinspection PyMethodMayBeStatic
    def p_value(self, p):
        """expr : term"""

        node = Node("CONTAINER", None, "_expr")
        node.children.append(p[1])
        p[0] = node

    # noinspection PyMethodMayBeStatic
    def p_uminus(self, p):
        """term : MINUS term %prec UMINUS"""

        node = Node("NUMBER", None, p[2])
        # node.leaf = -node.leaf
        p[0] = node

    # noinspection PyMethodMayBeStatic
    def p_term(self, p):
        """term : STRING
                | NUMBER"""

        if p.slice[1].type == 'STRING':
            node = Node("STRING", None, p[1])
        else:
            node = Node("NUMBER", None, p[1])
        p[0] = node

    # noinspection PyMethodMayBeStatic
    def p_error(self, p):
        if False:
            print(p.value)
            print("-------------")
            for t in p.lexer.lexstatere: print(t)
            print("-------------")

    def get_root(self):
        return self.nodeRoot

    def get_fun_list(self):
        return self._fun_list


if __name__ == "__main__":

    s = CalcParser()
    while 1:
        s.run()
        nod = Node()
        nod.debug_node(s.get_root())
        print("-------------")
        nod.debug_tree(s.get_root())
        print()
        print("-------------")
        a = nod.to_dict_from_node(s.get_root(), {})
        print(a)
        print("-------------")
        a = nod.to_json_string_from_dict(a)
        print(a)
        print("-------------")
        a = nod.to_node_from_json(a)
        print(nod.debug_node(a))
        print("-------------")
