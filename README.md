# PyPyFunPlot #

![alt text](src/res/bird.png)

Natalia & Andrew's ICHack19 project.

## Inspiration

Software projects can be complex and in need of optimiation (especially python :p)

This is especially true in languages without powerful IDEs, or where projects take on a complexity quite quickly, such as in OOP projects. This raises the question: How can we manage this complexity? Can we make a tool that will help de-fog programmers' heads when dealing with it?

## What it does

PyPyFunPlot is a static analysis tool for programmers to keep track of their complex projects. It produces a call network which shows all the function calls made within a python project, along with other information that will help programmers understand the dependencies, bottlenecks, and class structures in their project.

Current features include:
* Nodes represent funtions; (directed) arcs represent calls made by one function to another.
* Nodes are sized by their centrality (their importance in the network). We calculate this by the page rank score of function in the network, as Google uses.
* Nodes are colored and clustered by their class affiliation.

## How we built it

Python, using the grammar of python for reference, and a self-made parser-lexer. This parses the python project it's targeted at, creates a network diagram, and puts this network diagram into HTML so that it can be viewed and interacted with in the browser.

## What's next for PyPyFunPlot

This was quite a fun hackathon project, and we produced something we feel is genuinely useful for the future. Perhaps more importantly, this is a tool *we* would actually use.

We plan on maintaining this project, and maybe looking into some extensions to its functionality that will make it all the more useful to us and those who use it. Some ideas:

1. Marking class inheritance
2. Marking certain versus probabalistic function calls
3. Integration with runtime analysis which would show us how often functions are called, and possibly with what arguments.
