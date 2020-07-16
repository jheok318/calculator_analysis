# calculator analysis

node기반 ply package를 이용한 사칙연산(계산기) 분석

> 이를 조금더 개선하면 여러 형태의 DSL을 만들어낼수 있다.

- 목적
  - client가 string형태를  server로 전송한다.
  -  server는 lex,yacc를 통해 DAG의 형태로 만들어주고 이를 json형태로 변환을 시켜준다.
  - 이떄 server는 DAG형태의 data를 분석하거나 json형태를 분석하여 원하는 행동을 취할 수 있다.
  - 이후 server는 client에 json형태의 data를 string형태로 client에게 전송시켜줄수 있다.

- 결과

```python
# 1-2를 분석하자
calc> 1-2;
--------------
# 1-2를 노드형태로 연결한것을 트리형태의 그래프로 확인할 수 있다.
*    _root <CONTAINER>
*      _expr <CONTAINER>
*        - <OPERATION>
*          _expr <CONTAINER>
*            1 <NUMBER>
*          _expr <CONTAINER>
*            2 <NUMBER>
*      ; <calc_END>
-------------
# 트리형태의 작업이 제대로 되었는지 확인할 수 있다.
1 - 2 ; 
-------------
# 노드로 만들어진 계산식을 diction으로 만들수 있다.
{'type': 'CONTAINER', 'leaf': '_root', 'rule': '', 'children': [{'type': 'CONTAINER', 'leaf': '_expr', 'rule': '', 'children': [{'type': 'OPERATION', 'leaf': '-', 'rule': '', 'children': [{'type': 'CONTAINER', 'leaf': '_expr', 'rule': '', 'children': [{'type': 'NUMBER', 'leaf': '1', 'rule': '', 'children': []}]}, {'type': 'CONTAINER', 'leaf': '_expr', 'rule': '', 'children': [{'type': 'NUMBER', 'leaf': '2', 'rule': '', 'children': []}]}]}]}, {'type': 'calc_END', 'leaf': ';', 'rule': '', 'children': []}]}
-------------
# diction형태로 만들어진 data를 json형태로 만들수 있다.
{
  "type": "CONTAINER",
  "leaf": "_root",
  "rule": "",
  "children": [
    {
      "type": "CONTAINER",
      "leaf": "_expr",
      "rule": "",
      "children": [
        {
          "type": "OPERATION",
          "leaf": "-",
          "rule": "",
          "children": [
            {
              "type": "CONTAINER",
              "leaf": "_expr",
              "rule": "",
              "children": [
                {
                  "type": "NUMBER",
                  "leaf": "1",
                  "rule": "",
                  "children": []
                }
              ]
            },
            {
              "type": "CONTAINER",
              "leaf": "_expr",
              "rule": "",
              "children": [
                {
                  "type": "NUMBER",
                  "leaf": "2",
                  "rule": "",
                  "children": []
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "calc_END",
      "leaf": ";",
      "rule": "",
      "children": []
    }
  ]
}
-------------
#Json Data를 다시 diction형태로 변환 시킬수 있다.
{'type': 'CONTAINER', 'leaf': '_root', 'rule': '', 'children': [{'type': 'CONTAINER', 'leaf': '_expr', 'rule': '', 'children': [{'type': 'OPERATION', 'leaf': '-', 'rule': '', 'children': [{'type': 'CONTAINER', 'leaf': '_expr', 'rule': '', 'children': [{'type': 'NUMBER', 'leaf': '1', 'rule': '', 'children': []}]}, {'type': 'CONTAINER', 'leaf': '_expr', 'rule': '', 'children': [{'type': 'NUMBER', 'leaf': '2', 'rule': '', 'children': []}]}]}]}, {'type': 'calc_END', 'leaf': ';', 'rule': '', 'children': []}]}
```

