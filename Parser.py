# coding: utf-8

import os.path
import ply.lex as lex
import ply.yacc as yacc
import json

from __init__ import Node


def debug_node(node, indentation=0):

    if node is None:
        return

    _TAB = "  "

    if indentation == 0:
        print()
        # print()
        # print()

    cur_inden = indentation + 1

    try:
        print("*", _TAB * cur_inden, node.leaf, "<%s>" % node.type)
    except Exception as e:
        print("***", type(node), node)
        print(e)
        raise (Exception, "Node Print Error!!!!!")

    for n in node.children:
        debug_node(n, cur_inden)


def debug_tree(node):

    try:
        for n in node.children:
            if n.leaf == '_expr':
                debug_tree(n)
            elif len(n.children) > 1:
                debug_tree(n.children[0])
                print(n.leaf, end=' ')
                debug_tree(n.children[1])
            elif len(n.children) == 0:
                print(n.leaf, end=' ')

    except Exception as e:
        print("***", type(node), node)
        print(e)
        raise (Exception, "Node Print Error!!!!!")


def to_dict_from_node(node, py_dict=None):
    if py_dict is None:
        py_dict = {}

    if node is None:
        return

    try:
        py_dict["type"] = node.type
        py_dict["leaf"] = node.leaf
        py_dict["rule"] = node.rule
        py_dict["children"] = []

        if len(node.children) > 0:
            for n in node.children:
                temp_dict = {}
                py_dict["children"].append(to_dict_from_node(n, temp_dict))

    except Exception as e:
        print("***", type(node), node)
        print(e)
        raise (Exception, "Node Print Error!!!!!")

    return py_dict


def to_json_string_from_dict(node):
    node = to_dict_from_node(node)
    return json.dumps(node, indent=2)


def to_dict_from_json_string(json_data):
    return json.loads(json_data)


def to_tree_from_dict(dict_data, indentation=0):

    if dict_data is None:
        return

    cur_inden = indentation + 1
    _TAB = "  "

    try:
        node_data = Node(dict_data['type'], dict_data['children'], dict_data['leaf'], dict_data['rule'])
        print("*", _TAB * cur_inden, node_data.leaf, "<%s>" % node_data.type)
    except Exception as e:
        print("***", type(node_data), node_data)
        print(e)
        raise (Exception, "Node Print Error!!!!!")

    for n in dict_data['children']:
        to_tree_from_dict(n, cur_inden)

class Parser(object):

    tokens = ()
    precedence = ()

    def __init__(self):

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

    def parse(self, query) :
        self._fun_list = []

        # remove comment
        r_query = []
        for line in query.split('\n'):
            if line.lstrip()[:2] == '--':
                line = ''
            r_query.append(line)
        query = '\n'.join(r_query)

        #yacc.parse(query)

    def tokenTest(self, query) :
        lex.Lexer.input(query)
        while 1:
            tok = lex.Lexer.token(query)
            if not tok: break
            print(tok)

    def run(self):
        query = input('calc> ')
        yacc.parse(query)
        # self.debugNode(query)


class calcParser(Parser):

    #Lex

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


    def t_NUMBER(self, t):
        r'[\d]+[.]?[\d]*' # 소수점 지원

        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    t_ignore = " \t"

    ###############################################################################################

    #Yacc

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

    def p_expr(self, p):
        """expr : operation_expression"""

        node = Node("CONTAINER", None, "_expr")
        node.children.append(p[1])
        p[0] = node

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

    def p_group(self, p):
        """expr : LPAREN expr RPAREN"""

        node = Node("CONTAINER", None, "_expr")
        node.children.append(Node("KEYWORD", None, "("))
        node.children.append(p[2])
        node.children.append(Node("KEYWORD", None, ")"))
        p[0] = node

    def p_value(self, p):
        '''expr : term'''

        node = Node("CONTAINER", None, "_expr")
        node.children.append(p[1])
        p[0] = node

    def p_uminus(self, p):
        '''term : MINUS term %prec UMINUS'''

        node = Node("NUMBER", None, p[2])
        # node.leaf = -node.leaf
        p[0] = node

    def p_term(self, p) :
        """term : STRING
                | NUMBER"""

        if p.slice[1].type == 'STRING':
            node = Node("STRING", None, p[1])
        else:
            node = Node("NUMBER", None, p[1])
        p[0] = node

    def p_error(self, p):
        if False:
            print(p.value)
            print("-------------")
            for t in p.lexer.lexstatere: print(t)
            print("-------------")

    def getRoot(self):
        return self.nodeRoot

    def get_fun_list(self):
        return self._fun_list



s = calcParser()
while 1:
    s.run()
    debug_node(s.getRoot())
    print("-------------")
    debug_tree(s.getRoot())
    print()
    print("-------------")
    print(to_dict_from_node(s.getRoot(), {}))
    print("-------------")
    a = to_json_string_from_dict(s.getRoot())
    print(a)
    print("-------------")
    print(to_dict_from_json_string(a))
    print("-------------")