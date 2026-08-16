import re

from transpiler.ir.models import IRModule, IROperation


OPERATION_MAP = {
    "splitter.node_split": "EvaluateSplit",
    "tree._add_node": "CreateNode",
    "tree._resize": "ResizeTree",
    "tree._resize_c": "ResizeTree",
    "builder_stack.push": "PushStack",
    "builder_stack.pop": "PopStack",
    "builder_stack.top": "PeekStack",
}


class CythonStatementParser:

    def __init__(self):
        self.graph = IRModule()

    def _add(self, opcode: str, **attrs):
        self.graph.add(IROperation(opcode=opcode, inputs=[], outputs=[], attributes=attrs))

    def parse(self, source: str):
        call_pattern = re.compile(r"([A-Za-z_][A-Za-z0-9_\.]*)\(")

        for line in source.splitlines():
            line = line.strip()
            if not line:
                continue

            match = call_pattern.search(line)
            if match:
                call = match.group(1)
                opcode = OPERATION_MAP.get(call)
                if opcode:
                    self._add(opcode, name=call)

            if line.startswith("while "):
                self._add("BeginLoop", type="while")
            elif line.startswith("for "):
                self._add("BeginLoop", type="for")
            elif line.startswith("if "):
                condition = line[3:].rstrip(":").strip()
                self._add("Branch", condition=condition)
            elif line.startswith("return"):
                value = line.replace("return", "", 1).strip()
                self._add("Return", value=value)

        return self.graph