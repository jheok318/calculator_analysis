# coding: utf-8 
# import PostProcessing_CREATE_INDEX

import json


class Enum(object):
    def __init__(self, names, separator=None):
        self.names = names.split(separator)
        for value, name in enumerate(self.names):
            setattr(self, name.upper(), value)

    def tuples(self):
        return tuple(enumerate(self.names))


class QueryType(object):
    class Kind(Enum):
        NONE = 0
        SELECT = 1
        CREATE_TABLE = 2
        CREATE_INDEX = 3
        CREATE_PROC = 4
        CREATE_SCHEDULE = 5
        DROP_TABLE = 6
        DROP_INDEX = 7
        DROP_PROC = 8
        DROP_BACKEND = 9
        DROP_SCHEDULE = 10
        DELETE = 11
        UPDATE = 12
        INSERT = 13
        GRANT_OM = 14
        GRANT_DM = 15
        REVOKE_OM = 16
        REVOKE_DM = 17
        USER_ADD = 18
        USER_DELETE = 19
        USER_PASSWORD = 20
        USER_DENY = 21
        USER_ALLOW = 22
        COMMAND = 23
        CALL = 24
        ALTER_TABLE = 25
        SELECTINFO = 26
        CREATE_DATABASE = 27
        DROP_DATABASE = 28
        USE = 29
        GRANT_DBM = 30
        REVOKE_DBM = 31
        GRANT = 32
        REVOKE = 33
        CREATE_VIEW = 34
        DROP_VIEW = 35

        names = []
        obj_type = None
        obj_pos = None
        for obj in dir():
            # exec('obj_type = type(%s)') % obj
            # exec('ojb_pos = %s') % obj
            if obj_type == type(0):
                names.append((obj_pos, obj))

        names = [x[1] for x in sorted(names)]


# Query Tree를 표현하기 위한 Node Class
#
class Node(object):

    # 생성자
    #
    def __init__(self, type=None, children=None, leaf=None, rule=""):
        self.type = type
        self.children = []
        self.leaf = leaf
        self.rule = rule
        if children:
            self.children.append(children)

        self.qk = QueryType.Kind.NONE

    # 문자열 변환 함수
    #
    def __str__(self):
        return "type [%s], leaf[%s]" % (self.type, self.leaf)

    # eq 연산자
    #
    def __eq__(self, tmp):
        if type(tmp) != Node:
            return False
        if self.type != tmp.type or self.leaf != tmp.leaf:
            return False
        if len(self.children) != len(tmp.children):
            return False

        count = len(self.children)

        for i in range(count):
            if not (self.children[i] == tmp.children[i]):
                return False

        return True

    def clone(self):
        new_node = Node(self.type, None, self.leaf)
        for child in self.children:
            new_node.children.append(child.clone())
        return new_node

    # Rule 정의 함수
    #
    def set_rule(self, rule):
        self.rule = rule

    # type 이름과 leaf 이름을 바탕으로 인덱스 리턴
    #  0 이상의 값이면 해당 인덱스
    #  -1 이면 해당 노드 없음
    def index_child(self, type_name=None, leaf_name=None):
        for child in self.children:
            if child.type == type_name and leaf_name is None:
                return self.chidren.index(child)
            elif type_name is None and child.leaf == leaf_name:
                return self.chidren.index(child)
            elif child.type == type_name and child.leaf == leaf_name:
                return self.chidren.index(child)
        return -1

    # type 이름과 leaf 이름을 바탕으로 해당 노드가 있는지 확인
    #
    def exist_child(self, type_name=None, leaf_name=None):
        for child in self.children:
            if child.type == type_name and leaf_name is None:
                return True
            elif type_name is None and child.leaf == leaf_name:
                return True
            elif child.type == type_name and child.leaf == leaf_name:
                return True

        return False

    # 해당하는 모든 하위 노드 리턴
    #
    def get_all_child(self, type_name=None, leaf_name=None):
        return_list = []
        for child in self.children:
            if child.type == type_name and leaf_name is None:
                return_list.append(child)
            elif type_name is None and child.leaf == leaf_name:
                return_list.append(child)
            elif child.type == type_name and child.leaf == leaf_name:
                return_list.append(child)
            elif type_name is None and leaf_name is None:
                return self.children

        return return_list

    def debug_node(self, node, indentation=0):

        if node is None:
            return

        _TAB = "  "

        if indentation == 0:
            print()
            print()

        cur_inden = indentation + 1

        try:
            print("*", _TAB * cur_inden, node.leaf, "<%s>" % node.type)
        except Exception as e:
            print("***", type(node), node)
            print(e)
            raise (Exception, "Node Print Error!!!!!")

        for n in node.children:
            self.debug_node(n, cur_inden)

    def debug_tree(self, node):

        try:
            for n in node.children:
                if n.leaf == '_expr':
                    self.debug_tree(n)
                elif len(n.children) > 1:
                    self.debug_tree(n.children[0])
                    print(n.leaf, end=' ')
                    self.debug_tree(n.children[1])
                elif len(n.children) == 0:
                    print(n.leaf, end=' ')

        except Exception as e:
            print("***", type(node), node)
            print(e)
            raise (Exception, "Node Print Error!!!!!")

    def to_dict_from_node(self, node, py_dict=None):
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
                    py_dict["children"].append(self.to_dict_from_node(n, temp_dict))

        except Exception as e:
            print("***", type(node), node)
            print(e)
            raise (Exception, "Node Print Error!!!!!")

        return py_dict

    def to_json_string_from_dict(self, node):
        node = self.to_dict_from_node(node)
        return json.dumps(node, indent=2)

    # noinspection PyMethodMayBeStatic
    def to_dict_from_json_string(self, json_data):
        return json.loads(json_data)
