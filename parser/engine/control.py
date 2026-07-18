import ast

from parser.models.delta import Delta


class ControlFlowEngine(ast.NodeVisitor):

    def __init__(self):
        self.control = []
        self.function = None

    def visit_FunctionDef(self, node):

        self.function = node.name

        self.generic_visit(node)

    def visit_If(self, node):

        condition = ast.unparse(node.test)

        self.control.append(
            Delta(
                kind="BRANCH",
                function=self.function,
                line=node.lineno,
                inputs=[condition],
                outputs=[],
                effects=["CONTROL_FLOW"],
                evidence=f"{self.function}:{node.lineno}"
            )
        )

        self.generic_visit(node)

    def visit_For(self, node):

        iterator = ast.unparse(node.iter)

        self.control.append(
            Delta(
                kind="LOOP",
                function=self.function,
                line=node.lineno,
                inputs=[iterator],
                outputs=[],
                effects=["ITERATION"],
                evidence=f"{self.function}:{node.lineno}"
            )
        )

        self.generic_visit(node)

    def visit_While(self, node):

        condition = ast.unparse(node.test)

        self.control.append(
            Delta(
                kind="LOOP",
                function=self.function,
                line=node.lineno,
                inputs=[condition],
                outputs=[],
                effects=["ITERATION"],
                evidence=f"{self.function}:{node.lineno}"
            )
        )

        self.generic_visit(node)

    def visit_Try(self, node):

        self.control.append(
            Delta(
                kind="TRY",
                function=self.function,
                line=node.lineno,
                inputs=[],
                outputs=[],
                effects=["ERROR_BOUNDARY"],
                evidence=f"{self.function}:{node.lineno}"
            )
        )

        self.generic_visit(node)