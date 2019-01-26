#from plotly import __version__
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# import plotly
# import plotly.graph_objs as go

# plotly.offline.plot({
#     "data": [go.Scatter(x=[6, 2, 3, 4], y=[4, 3, 2, 1])],
#     "layout": go.Layout(title="hello world")
# }, auto_open=True)

import networkx as nx

mydict =	{
  "fun1": ["fun2"],
  "fun2": ["fun3"],
  "fun3": [],
  "fun4": ["funprint"]
}

def get_unique_fun_from_dict(fun_dict):
    all_funs = set()
    for key in fun_dict.keys():
        all_funs.add(key)
    for fun_list in fun_dict.values():
        [all_funs.add(fun) for fun in fun_list]
    return all_funs

def get_digraph_from_dict(fun_dict):
    g = nx.DiGraph()

    #Add all nodes
    all_funs = get_unique_fun_from_dict(fun_dict)
    #[print(fun) for fun in all_funs]
    [g.add_node(fun) for fun in all_funs]
    
    #Add edges
    for key in fun_dict.keys():
        for called_fun in fun_dict[key]:
            g.add_edge(key, called_fun)
    return g

g = get_digraph_from_dict(mydict)
print(g.number_of_edges())