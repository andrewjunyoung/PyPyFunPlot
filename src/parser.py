from tqdm import tqdm
from sys import stdout
from re import findall
from ast import Call, parse, NodeVisitor, walk
from collections import deque

def _get_occurrences(list, item):
    return [i
            for i in tqdm(range(len(list)), file = stdout)
            if list[i] == item]


def _get_words(text):
    return [word
            for word in findall(r"[^\s\(\)]+", text)]


class Parser(object):
    def _get_fun_names(contents):
        words = _get_words(contents)
        def_occurrences = _get_occurrences(words, "def")

        fun_names = [words[i + 1]
                     for i in def_occurrences]

        return fun_names

    def _get_fun_calls(contents):
        tree = parse(contents)

        fun_calls = []
        for node in walk(tree):
            if isinstance(node, Call):
                callvisitor = FuncCallVisitor()
                callvisitor.visit(node.func)
                fun_calls.append(callvisitor.name)

        return fun_calls

    def get_call_network(file_path):
        file = open(file_path)
        # {

        contents = file.read()

        print("Parsing function names from " + str(file_path) + ".")
        fun_names = Parser._get_fun_names(contents)

        print("Parsing function calls from " + str(file_path) + ".")
        fun_calls = Parser._get_fun_calls(contents)

        # }
        file.close()

        return (fun_names, fun_calls)


class FuncCallVisitor(NodeVisitor):
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


if __name__ == "__main__":
    print(Parser.get_call_network("./parser.py"))
