import re

from transpiler.cython.nodes import (
    BlockNode,
    CallNode,
    ReturnNode,
    RaiseNode,
    AssignmentNode,
)


CALL_PATTERN = re.compile(
    r"([A-Za-z_][A-Za-z0-9_\.]*)\("
)

ASSIGNMENT_PATTERN = re.compile(
    r"^([A-Za-z_][A-Za-z0-9_\.]*)\s*=\s*(.+)$"
)

def indentation(line: str):

    return len(line) - len(
        line.lstrip()
    )


def collect_statement(lines, start):

    statement = lines[start].strip()

    balance = (
        statement.count("(")
        - statement.count(")")
    )

    i = start

    while balance > 0 and i + 1 < len(lines):

        i += 1

        next_line = lines[i].strip()

        statement += " " + next_line

        balance += (
            next_line.count("(")
            - next_line.count(")")
        )

    return statement, i


def parse_blocks(source: str):

    root = BlockNode(
        kind="root"
    )

    stack = [
        (-1, root)
    ]

    lines = source.splitlines()

    i = 0

    while i < len(lines):

        raw_line = lines[i]

        if not raw_line.strip():

            i += 1

            continue

        level = indentation(
            raw_line
        )

        line, i = collect_statement(
            lines,
            i,
        )

        while (
            stack
            and level <= stack[-1][0]
        ):
            stack.pop()

        parent = stack[-1][1]

        if line.startswith("while "):

            node = BlockNode(
                kind="while",
                condition=line[6:].rstrip(":"),
            )

            parent.children.append(
                node
            )

            stack.append(
                (level, node)
            )

        elif line.startswith("for "):

            node = BlockNode(
                kind="for",
                condition=line[4:].rstrip(":"),
            )

            parent.children.append(
                node
            )

            stack.append(
                (level, node)
            )

        elif line.startswith("if "):

            condition = (
                line[3:]
                .rstrip(":")
                .strip()
            )

            node = BlockNode(
                kind="if",
                condition=condition,
            )

            parent.children.append(
                node
            )

            stack.append(
                (level, node)
            )

        elif line.startswith("elif "):

            condition = (
                line[5:]
                .rstrip(":")
                .strip()
            )

            node = BlockNode(
                kind="if",
                condition=condition,
            )

            parent.children.append(
                node
            )

            stack.append(
                (level, node)
            )

        elif line.startswith("else"):

            node = BlockNode(
                kind="else"
            )

            parent.children.append(
                node
            )

            stack.append(
                (level, node)
            )

        elif line.startswith("return"):

            parent.children.append(
                ReturnNode(
                    value=line[6:].strip()
                )
            )

        elif line.startswith("raise"):

            exception = (
                line[5:]
                .strip()
                .replace("()", "")
            )

            parent.children.append(
                RaiseNode(
                    exception=exception
                )
            )

        elif "=" in line and not line.startswith("=="):

            match = ASSIGNMENT_PATTERN.match(
                line
            )

            if match:

                parent.children.append(
                    AssignmentNode(
                        target=match.group(1).strip(),
                        value=match.group(2).strip(),
                    )
                )

        else:

            for match in CALL_PATTERN.finditer(
                line
            ):

                parent.children.append(
                    CallNode(
                        name=match.group(1)
                    )
                )

        i += 1

    return root