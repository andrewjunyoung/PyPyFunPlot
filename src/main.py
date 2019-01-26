from parser import Parser
from network_vis import get_digraph_from_dict, plot_digraph

if __name__ == "__main__":
    call_network = Parser.get_call_network("./src/parser.py")
    digraph = get_digraph_from_dict(call_network)
    plot_digraph(digraph)
