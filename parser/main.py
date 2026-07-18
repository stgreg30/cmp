import ast
import json
import sys
from dataclasses import asdict

from parser.models.delta import Delta
from parser.engine.semantic import SemanticEngine
from parser.engine.memory import MemoryEngine


class DeltaVisitor(ast.NodeVisitor):

    def __init__(self):
        self.deltas = []

    def visit_FunctionDef(self, node):

        current = node.name

        for child in ast.walk(node):

            # --------------------------
            # Assignment
            # --------------------------
            if isinstance(child, ast.Assign):

                variables = []

                for target in child.targets:
                    if isinstance(target, ast.Name):
                        variables.append(target.id)

                self.deltas.append(
                    Delta(
                        kind="STATE_CHANGE",
                        function=current,
                        line=child.lineno,
                        inputs=[],
                        outputs=variables,
                        effects=[],
                        evidence=f"{current}:{child.lineno}"
                    )
                )

            # --------------------------
            # Function Call
            # --------------------------
            elif isinstance(child, ast.Call):

                target = "unknown"

                if isinstance(child.func, ast.Name):
                    target = child.func.id

                elif isinstance(child.func, ast.Attribute):
                    target = child.func.attr

                arguments = []

                for arg in child.args:

                    if isinstance(arg, ast.Name):
                        arguments.append(arg.id)

                    elif isinstance(arg, ast.Constant):
                        arguments.append(arg.value)

                self.deltas.append(
                    Delta(
                        kind="CALL",
                        function=current,
                        line=child.lineno,
                        inputs=arguments,
                        outputs=[target],
                        effects=[],
                        evidence=f"{current}:{child.lineno}"
                    )
                )

            # --------------------------
            # Return
            # --------------------------
            elif isinstance(child, ast.Return):

                outputs = []

                if isinstance(child.value, ast.Name):
                    outputs.append(child.value.id)

                elif isinstance(child.value, ast.Constant):
                    outputs.append(child.value.value)

                self.deltas.append(
                    Delta(
                        kind="RETURN",
                        function=current,
                        line=child.lineno,
                        inputs=[],
                        outputs=outputs,
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

    # --------------------------
    # Semantic Stage
    # --------------------------

    semantic = SemanticEngine()

    normalized = semantic.normalize_all(visitor.deltas)

    # --------------------------
    # Memory Stage
    # --------------------------

    memory = MemoryEngine()

    nodes = memory.build(normalized)

    print(
        json.dumps(
            [asdict(node) for node in nodes],
            indent=4
        )
    )


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python parser/main.py parser/example.py")
        sys.exit(1)

    analyze(sys.argv[1])


if __name__ == "__main__":
    main()