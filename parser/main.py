import ast
import json
import sys
from dataclasses import asdict

from models.delta import Delta


class DeltaVisitor(ast.NodeVisitor):
    def __init__(self):
        self.deltas = []

    def visit_FunctionDef(self, node):
        current = node.name

        for child in ast.walk(node):

            if isinstance(child, ast.Return):
                self.deltas.append(
                    Delta(
                        kind="RETURN",
                        function=current,
                        line=child.lineno,
                        inputs=[],
                        outputs=[],
                        effects=[],
                        evidence=f"{current}:{child.lineno}"
                    )
                )

            elif isinstance(child, ast.Assign):
                self.deltas.append(
                    Delta(
                        kind="STATE_CHANGE",
                        function=current,
                        line=child.lineno,
                        inputs=[],
                        outputs=[],
                        effects=[],
                        evidence=f"{current}:{child.lineno}"
                    )
                )

            elif isinstance(child, ast.Call):

                target = "unknown"

                if isinstance(child.func, ast.Name):
                    target = child.func.id

                elif isinstance(child.func, ast.Attribute):
                    target = child.func.attr

                self.deltas.append(
                    Delta(
                        kind="CALL",
                        function=current,
                        line=child.lineno,
                        inputs=[],
                        outputs=[target],
                        effects=[],
                        evidence=f"{current}:{child.lineno}"
                    )
                )

        self.generic_visit(node)


def analyze(filename):
    with open(filename, "r", encoding="utf8") as f:
        tree = ast.parse(f.read(), filename)

    visitor = DeltaVisitor()
    visitor.visit(tree)

    print(
        json.dumps(
            [asdict(delta) for delta in visitor.deltas],
            indent=4
        )
    )


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python main.py <file.py>")
        sys.exit(1)

    analyze(sys.argv[1])