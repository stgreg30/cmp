from models.delta import Delta


class SemanticEngine:
    """
    Normalizes language-specific events into
    Canonical Memory Protocol (CMP) events.
    """

    def __init__(self):
        self.mapping = {
            "CALL": "INVOKE",
            "STATE_CHANGE": "WRITE",
            "RETURN": "RETURN",
            "READ": "READ",
            "LOOP": "ITERATE",
            "CONDITION": "BRANCH"
        }

    def normalize(self, delta: Delta) -> Delta:
        """
        Convert parser events into canonical CMP events.
        """

        delta.kind = self.mapping.get(delta.kind, delta.kind)

        return delta

    def normalize_all(self, deltas):
        """
        Normalize an entire list of Delta objects.
        """

        return [self.normalize(d) for d in deltas]