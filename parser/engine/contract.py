from collections import defaultdict

from parser.models.delta import Delta


class ContractEngine:

    def build(self, deltas):

        contracts = defaultdict(list)

        for delta in deltas:

            key = (
                delta.kind,
                tuple(delta.inputs),
                tuple(delta.outputs)
            )

            contracts[key].append(delta)

        result = []

        for key, evidence in contracts.items():

            result.append(
                {
                    "contract": {
                        "kind": key[0],
                        "inputs": list(key[1]),
                        "outputs": list(key[2]),
                    },
                    "implementations": len(evidence),
                    "evidence": [
                        d.evidence
                        for d in evidence
                    ]
                }
            )

        return result