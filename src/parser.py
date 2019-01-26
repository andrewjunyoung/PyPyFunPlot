from tqdm import tqdm
from sys import stdout
from re import findall, match
from ast import Call, parse, NodeVisitor, walk
from collections import deque
from itertools import takewhile


def _get_occurrences(list, item):
    return [i
            for i in tqdm(range(len(list)), file = stdout)
            if list[i] == item]


def _get_words(text):
    return [word
            for word in findall(r"[^\s\(\)]+", text)]


def is_fun_definition_of(fun_name, line):
    return match(r"\s*def " + fun_name + r".+", line)


def get_indentation(line):
    return match("(\s*)", line)


def get_re_len(re_match):
    if re_match:
        return len(re_match.group(1))
    else:
        return 0


def fix_indentation_by(indent_level, lines):
    return [line[indent_level + 4:] for line in lines]


def get_fun_lines(i, lines, indent_level):
    fun_lines = []
    for line in lines[i + 1:]:
        if Parser.is_deeper_than(indent_level, line):
            fun_lines.append(line)
        else:
            return fix_indentation_by(indent_level, fun_lines)
    return fix_indentation_by(indent_level, fun_lines)


class Parser(object):
    def _get_fun_names(contents):
        words = _get_words(contents)
        def_occurrences = _get_occurrences(words, "def")
        fun_names = [words[i + 1]
                     for i in tqdm(def_occurrences, file = stdout)]
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

    def is_deeper_than(prev_level, curr_line):
        return get_re_len(match("(\s{" + str(prev_level + 1) + "})",
                                curr_line)) != 0

    def _get_body_of(fun_name, contents):
        lines = contents.splitlines()
        for i, line in enumerate(lines):
            if is_fun_definition_of(fun_name, line):
                # Pre: this definition is unique

                # Get the body of the function
                indent_level = get_re_len(get_indentation(line))
                fun_lines = get_fun_lines(i, lines, indent_level)
                print("lines:", fun_lines)
                fun_body = "\n".join(fun_lines)

                return fun_body

    def get_call_network(file_path):
        file = open(file_path)
        # {
        contents = file.read()

        print("Parsing function names from " + str(file_path) + ".")
        fun_names = Parser._get_fun_names(contents)

        print("Parsing function calls from " + str(file_path) + ".")
        call_network = {}
        for fun_name in tqdm(fun_names, file = stdout):
            fun_body = Parser._get_body_of(fun_name, contents)
            fun_calls = Parser._get_fun_calls(fun_body)
            call_network[fun_name] = fun_calls

        # }
        file.close()

        print(call_network)
        return call_network


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
    Parser.get_call_network("./parser.py")
