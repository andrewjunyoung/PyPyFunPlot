from tqdm import tqdm
from sys import stdout
from re import findall

def _get_occurrences(list, item):
    return [i
            for i in tqdm(range(len(list)), file = stdout)
            if list[i] == item]

class Parser(object):
    def _get_fun_names(file):
        contents = file.read()
        words = [word
                 for word in findall(r"[^\s\(\)]+", contents)]

        def_occurrences = _get_occurrences(words, "def")
        print(def_occurrences)

        fun_names = [words[i + 1]
                     for i in def_occurrences]

        return fun_names

    def get_call_network(file_path):
        file = open(file_path)
        # {
        print("Parsing function names from " + str(file_path) + ".")
        fun_names = Parser._get_fun_names(file)
        # }
        file.close()

        print(fun_names)

if __name__ == "__main__":
    Parser.get_call_network("./parser.py")
