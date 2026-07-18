import ast
import json
import sys


class DeltaVisitor(ast.NodeVisitor):
    def __init__(self):
        self.deltas = []

    def visit_FunctionDef(self, node):
        current = node.name

        for child in ast.walk(node):

            if isinstance(child, ast.Return):
                self.deltas.append({
                    "function": current,
                    "type": "RETURN",
                    "line": child.lineno
                })

            elif isinstance(child, ast.Assign):
                self.deltas.append({
                    "function": current,
                    "type": "STATE_CHANGE",
                    "line": child.lineno
                })

            elif isinstance(child, ast.Call):

                if isinstance(child.func, ast.Name):

                    self.deltas.append({
                        "function": current,
                        "type": "CALL",
                        "target": child.func.id,
                        "line": child.lineno
                    })

        self.generic_visit(node)


def analyze(filename):

    with open(filename, "r", encoding="utf8") as f:
        tree = ast.parse(f.read())

    visitor = DeltaVisitor()

    visitor.visit(tree)

    print(json.dumps(visitor.deltas, indent=4))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python main.py file.py")
        exit()

    analyze(sys.argv[1])