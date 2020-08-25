# coding: utf-8 
# import PostProcessing_CREATE_INDEX
import json


class NodeType(object):
    """
    Node Class 의 Type 을 개발자가 더 효율적으로 쓰기 위한 NodeType class
    """

    CONTAINER = "CONTAINER"
    KEYWORD = "KEYWORD"
    VALUE = "VALUE"

    def __init__(self, type=None):
        """
        생성자

        Parameter
        -----------
        type : String
          - 노드의 타입을 사용자가 명시할 수 있다.
        """
        self.type = type

    def __str__(self):
        """
        문자열 변환 함수
        노드타입을 문자열로 변환시 출력되는 형태
        """
        return "type [%s]" % self.type


# Query Tree를 표현하기 위한 Node Class
#
class Node(NodeType):
    """
    Query Tree 를 표현하기 위한 Node Class
    """

    def __init__(self, type=None, children=None, data=None, rule=""):
        """
        생성자

        Parameter
        -----------
        type : String
          - 노드의 타입을 사용자가 명시할 수 있다.

        children : Node
          - 노드의 자식노드를 children 리스트에 추가할 수 있다.

        data : String
          - 노드에 실질적으로 들어가는 data 의 형태(string)가 들어간다
            이후 lexer,parser 에 의해 type 검증 후 data 의 type 이 결정된다.

        rule : String
          - 노드의 type,data 를 통해 직관적으로 이해하기 어려운경우 rule 에 내용을 추가할 수 있다.
        """
        super().__init__(type)
        self.children = []
        self.data = data
        self.rule = rule
        if children:
            self.children.append(children)

    def __str__(self):
        """
        문자열 변환 함수
        노드를 문자열로 변환시 출력되는 형태
        """
        return "type [%s], data[%s]" % (self.type, self.data)

    def __eq__(self, tmp):
        """
        eq 연산자

        Parameter
        ------------------
        tmp : Node
          - 비교를 원하는 노드의 root

        Return
        ------------------
        Boolean
          - 기존의 노드와 비교를 하고싶은 노드를 type, data, children 까지
              비교후 일치하면 True, 일치하지 않으면 False 를 return 한다.
        """
        if type(tmp) != Node:
            return False
        if self.type != tmp.type or self.data != tmp.data:
            return False
        if len(self.children) != len(tmp.children):
            return False

        count = len(self.children)

        for i in range(count):
            if not (self.children[i] == tmp.children[i]):
                return False

        return True

    def clone(self):
        """
        Node 의 복제

        Return
        ------------------
        Node
          - 노드를 복제하여 새로운 노드를 생성가능하다.
        """
        new_node = Node(self.type, None, self.data)
        for child in self.children:
            new_node.children.append(child.clone())
        return new_node

    def set_rule(self, rule):
        """
        Rule 정의 함수

        Parameter
        ------------------
        rule : String
          - 해당 노드의 주석

        Return
        ------------------
        해당 노드의 rule 을 새롭게 정의할 수 있다.
        """
        self.rule = rule

    def index_child(self, type_name=None, data_name=None):
        """
        type 이름과 data 이름을 바탕으로 인덱스 리턴

        Parameter
        ------------------
        type_name : string form of node.type
          - 해당 노드의 type 명

        data_name : string form of node.data
          - 해당 노드의 data 명

        Return
        ------------------
        index or -1
          - 0 이상의 값이면 해당 인덱스, -1 이면 해당 노드 없음
        """
        for child in self.children:
            if child.type == type_name and data_name is None:
                return self.chidren.index(child)
            elif type_name is None and child.data == data_name:
                return self.chidren.index(child)
            elif child.type == type_name and child.data == data_name:
                return self.chidren.index(child)
        return -1

    def exist_child(self, type_name=None, data_name=None):
        """
        type 이름과 data 이름을 바탕으로 해당 노드가 있는지 확인

        Parameter
        ------------------
        type_name : string form of node.type
          - 해당 노드의 type 명

        data_name : string form of node.data
          - 해당 노드의 data 명

        Return
        ------------------
        Boolean
          - 해당하는 노드가 있다면 True 없다면  False 를 return 한다.
        """
        for child in self.children:
            if child.type == type_name and data_name is None:
                return True
            elif type_name is None and child.data == data_name:
                return True
            elif child.type == type_name and child.data == data_name:
                return True

        return False

    def get_child_by_index(self, number):
        """
        type 이름과 data 이름을 바탕으로 해당하는 노드의 child 중 일치하는 노드를 출력

        Parameter
        ------------------
        number : int
          - 노드의 children 중 원하는 노드의 위치

        Return
        ------------------
        return_list[number] : node
          - 해당 노드중 선택한 하위 노드를 출력
        """
        return self.children[number]

    def get_child_with_name(self, type_name=None, data_name=None):
        """
        type 이름과 data 이름을 바탕으로 해당하는 노드의 child 중 일치하는 것을 list로 출력

        Parameter
        ------------------
        type_name : string form of node.type
          - 해당 노드의 type 명

        data_name : string form of node.data
          - 해당 노드의 data 명

        Return
        ------------------
        return_list : list
          - 해당 노드의 하위 노드를 list 형태로 출력
        """
        return_list = []

        if type_name is None and data_name is None:
            return self.children

        for child in self.children:
            if child.type == type_name and data_name is None:
                return_list.append(child)
            elif type_name is None and child.data == data_name:
                return_list.append(child)
            elif child.type == type_name and child.data == data_name:
                return_list.append(child)

        return return_list

    def debug_node(self, node, indentation=0):
        """
        해당하는 노드의 하위 노드를 재귀 호출하여 트리타입의 그래프로 콘솔 출력

        Parameters
        ------------------
        node : Node
          - Node 클래스
        indentation : int
          - 해당 노드까지의 재귀횟수

        Return
        ------------------
        print tree of (node.leap & node.type)
          - 노드의 leap, type 을 트리형태의 그래프로 출력
        """
        if node is None:
            return

        _TAB = "  "

        if indentation == 0:
            print()
            print()

        cur_inden = indentation + 1

        try:
            print("*", _TAB * cur_inden, node.data, "<%s>" % node.type)
        except Exception as e:
            print("***", type(node), node)
            print(e)
            raise (Exception, "Node Print Error!!!!!")

        for n in node.children:
            self.debug_node(n, cur_inden)

    def debug_tree(self, node):
        """
        해당 노드의 연결이 적절하게 이루어 졌는지 확인하기 위해 콘솔 출력

        Parameter
        ------------------
        node : Node
          - Node 클래스

        Return
        ------------------
        print string of node
          - input 으로 들어온 node 를 string 타입으로 출력
        """
        try:
            for n in node.children:
                if n.data == '_expr':
                    self.debug_tree(n)
                elif len(n.children) > 1:
                    self.debug_tree(n.children[0])
                    print(n.data, end=' ')
                    self.debug_tree(n.children[1])
                elif len(n.children) == 0:
                    print(n.data, end=' ')

        except Exception as e:
            print("***", type(node), node)
            print(e)
            raise (Exception, "Node Print Error!!!!!")

    def to_dict_from_node(self, node, py_dict=None):
        """
        노드들의 연결을 dictionary 타입으로 변환시켜 주는 함수

        Parameter
        ------------------
        node : Node
          - Node 클래스
        py_dict : dictionary
          - dictionary 타입의 집합이 모이게 된다.

        Return
        ------------------
        py_dict : dictionary
          - node 타입의 집합이 dictionary 타입으로 변형
        """
        if py_dict is None:
            py_dict = {}

        if node is None:
            return

        try:
            py_dict["type"] = node.type
            py_dict["data"] = node.data
            py_dict["rule"] = node.rule
            py_dict["children"] = []

            for n in node.children:
                temp_dict = {}
                py_dict["children"].append(
                    self.to_dict_from_node(n, temp_dict))

        except Exception as e:
            print("***", type(node), node)
            print(e)
            raise (Exception, "Node Print Error!!!!!")

        return py_dict

    def to_json_string_from_dict(self, py_dict):
        """
        dictionary 타입을 json 타입으로 변형 시켜주는 함수

        Parameter
        ------------------
        py_dict : dictionary
          - dictionary 타입

        Return
        ------------------
        json data
          - json 데이터
        """
        return json.dumps(py_dict, indent=2)

    def to_node_from_json(self, json_data, node=None):
        """
        json 타입을 node 타입으로 변형 시켜주는 함수

        Parameter
        ------------------
        json_data : json string
          - json type string

        Return
        ------------------
        node : Node
          - Node 클래스
        """
        if node is None:
            node = Node(Node.CONTAINER, None, "root")

        if json_data is None:
            return

        dict_data = json.loads(json_data)

        try:
            for n in dict_data['children']:
                temp_node = Node(n['type'], None, n['data'], n['rule'])
                if n['children']:
                    temp_json_data = self.to_json_string_from_dict(n)
                    self.to_node_from_json(temp_json_data, temp_node)
                else:
                    temp_json_data = self.to_json_string_from_dict(n)
                    self.to_node_from_json(temp_json_data, temp_node)
                node.children.append(temp_node)

        except Exception as e:
            print(e)
            raise (Exception, "json_data Error!!!!!")

        return node
