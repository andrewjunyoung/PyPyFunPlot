from tqdm import tqdm
from sys import stdout
from re import findall, match
from ast import Call, parse, NodeVisitor, walk
from collections import deque
from itertools import takewhile

def get_occurrences(lines, str):
    indexes = []
    for i, line in enumerate(lines):
        if match(r"\s*" + str + "\s", line):
            indexes.append(i)
    return indexes


def get_indent_level(line):
    return get_re_len(match(r"(\s*)", line))


def get_re_len(re_match):
    if re_match:
        return len(re_match.group(1))
    else:
        return 0


def fix_indentation_by(indent_level, lines):
    return [line[indent_level + 4:] for line in lines]


class Parser(object):
    def is_fun_def_of(fun_name, line):
        return match(r"\s*def " + fun_name + r".+", line)

    def get_fun_lines(i, lines, indent_level):
        fun_lines = []
        for line in lines[i + 1:]:
            if Parser.is_deeper_than(indent_level, line):
                fun_lines.append(line)
            else:
                return fix_indentation_by(indent_level, fun_lines)
        return fix_indentation_by(indent_level, fun_lines)


    def get_class_name(i, lines):
        indent_level = get_indent_level(lines[i])

        if indent_level == 0:
            return ""

        for line in lines[i - 1::-1]:
            if Parser.is_shallower_than(indent_level, line):
                re_match = match(r"\s*class (\w+)", line)
                if re_match:
                    return re_match.group(1)
                else:
                    return ""
        return ""

    def get_fun_name_from_def(line):
        return match(r"\s*def (\w+)", line).group(1)

    def get_fun_names(contents):
        lines = contents.splitlines()
        def_occurrences = get_occurrences(lines, "def")

        fun_names = []
        for index in tqdm(def_occurrences, file = stdout):
            prev_lines = lines[:index]
            class_name = Parser.get_class_name(index, lines)
            method_name = Parser.get_fun_name_from_def(lines[index])
            if len(class_name) > 0:
                fun_names.append(class_name + "." + method_name)
            else:
                fun_names.append(method_name)

        return fun_names

    def get_fun_calls(contents):
        tree = parse(contents)

        fun_calls = []
        for node in walk(tree):
            if isinstance(node, Call):
                callvisitor = FunCallVisitor()
                callvisitor.visit(node.func)
                fun_calls.append(callvisitor.name)

        return fun_calls

    def is_deeper_than(prev_level, curr_line):
        indent_level = get_indent_level(curr_line)
        return get_re_len(match("^(\s{" + str(prev_level + 4) + "})",
                                curr_line)) != 0

    def is_shallower_than(prev_level, curr_line):
        # Catch empty lines.
        if match("^\s*$", curr_line):
            return False

        curr_level = get_indent_level(curr_line)
        return curr_level < prev_level

    def get_body_of(fun_name, contents):
        lines = contents.splitlines()
        for i, line in enumerate(lines):
            if Parser.is_fun_def_of(fun_name, line):
                indent_level = get_indent_level(line)
                fun_lines = Parser.get_fun_lines(i, lines, indent_level)
                fun_body = "\n".join(fun_lines)

                return fun_body

    def get_call_network(file_path):
        file = open(file_path)
        # {
        contents = file.read()

        print("Parsing function names from " + str(file_path) + ".")
        fun_names = Parser.get_fun_names(contents)

        print("Parsing function calls from " + str(file_path) + ".")
        call_network = {}
        for fun_name in tqdm(fun_names, file = stdout):
            if "." in fun_name:
                prefix = fun_name.split('.')[0]
                suffix = fun_name.split('.')[1]

                fun_body = Parser.get_body_of(suffix, contents)
            else:
                fun_body = Parser.get_body_of(fun_name, contents)

            fun_calls = Parser.get_fun_calls(fun_body)
            call_network[fun_name] = fun_calls

        # }
        file.close()

        return call_network


class FunCallVisitor(NodeVisitor):
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

