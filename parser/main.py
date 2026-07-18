import ast
import json
import sys
from pathlib import Path

graph = {
    "functions": [],
    "imports": [],
    "classes": []
}

class Visitor(ast.NodeVisitor):

    def visit_FunctionDef(self,node):
        graph["functions"].append({
            "name":node.name,
            "line":node.lineno
        })
        self.generic_visit(node)

    def visit_ClassDef(self,node):
        graph["classes"].append({
            "name":node.name,
            "line":node.lineno
        })
        self.generic_visit(node)

    def visit_Import(self,node):
        for alias in node.names:
            graph["imports"].append(alias.name)

    def visit_ImportFrom(self,node):
        graph["imports"].append(node.module)

path = Path(sys.argv[1])

tree = ast.parse(path.read_text())

Visitor().visit(tree)

print(json.dumps(graph,indent=4))
