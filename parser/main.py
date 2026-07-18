import ast
import json
import sys
from dataclasses import asdict

from parser.models.delta import Delta
from parser.engine.semantic import SemanticEngine


class DeltaVisitor(ast.NodeVisitor):
    def __init__(self):
        self.deltas = []

    def visit_FunctionDef(self, node):
        current = node.name

        for child in ast.walk(node):

            # -------------------------
            # Return
            # -------------------------
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

            # -------------------------
            # Assignment
            # -------------------------
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

            # -------------------------
            # Function Calls
            # -------------------------
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

    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename)

    visitor = DeltaVisitor()
    visitor.visit(tree)

    # -------------------------
    # Semantic Stage
    # -------------------------
    engine = SemanticEngine()

    normalized = engine.normalize_all(visitor.deltas)

    result = [asdict(delta) for delta in normalized]

    print(json.dumps(result, indent=4))


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python parser/main.py example.py")
        sys.exit(1)

    analyze(sys.argv[1])


if __name__ == "__main__":
    main()