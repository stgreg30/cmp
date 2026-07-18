from dataclasses import dataclass, asdict


@dataclass
class MemoryNode:
    node_type: str
    name: str
    function: str
    line: int
    metadata: dict


class MemoryEngine:

    def build(self, deltas):

        memory = []

        for delta in deltas:

            if delta.kind == "WRITE":

                memory.append(
                    MemoryNode(
                        node_type="VariableWrite",
                        name="variable",
                        function=delta.function,
                        line=delta.line,
                        metadata={
                            "effects": delta.effects,
                            "evidence": delta.evidence
                        }
                    )
                )

            elif delta.kind == "INVOKE":

                target = ""

                if delta.outputs:
                    target = delta.outputs[0]

                memory.append(
                    MemoryNode(
                        node_type="FunctionInvoke",
                        name=target,
                        function=delta.function,
                        line=delta.line,
                        metadata={
                            "evidence": delta.evidence
                        }
                    )
                )

            elif delta.kind == "RETURN":

                memory.append(
                    MemoryNode(
                        node_type="Return",
                        name=delta.function,
                        function=delta.function,
                        line=delta.line,
                        metadata={
                            "evidence": delta.evidence
                        }
                    )
                )

        return memory