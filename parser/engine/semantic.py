from models.delta import Delta


class SemanticEngine:

    def normalize(self, delta: Delta):

        mapping = {

            "CALL": "INVOKE",

            "STATE_CHANGE": "WRITE",

            "RETURN": "RETURN"

        }

        delta.kind = mapping.get(delta.kind, delta.kind)

        return delta
