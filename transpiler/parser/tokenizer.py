from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    STRING = "STRING"
    NUMBER = "NUMBER"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    COLON = "COLON"
    DOT = "DOT"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    NEWLINE = "NEWLINE"
    OPERATOR = "OPERATOR"
    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


KEYWORDS = {
    "def",
    "class",
    "cdef",
    "cpdef",
    "return",
    "if",
    "elif",
    "else",
    "for",
    "while",
    "with",
    "try",
    "except",
    "finally",
    "raise",
    "import",
    "from",
    "as",
    "pass",
    "break",
    "continue",
    "and",
    "or",
    "not",
    "in",
    "is",
    "yield",
    "lambda",
    "ctypedef",
    "cimport",
    "nogil",
}


def _tokenize_segment(segment: str, line_no: int, start_col: int) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    length = len(segment)
    while i < length:
        ch = segment[i]

        if ch in " \t":
            i += 1
            continue

        if ch in "([{":
            tokens.append(Token({"(": TokenType.LPAREN, "[": TokenType.LBRACKET, "{": TokenType.LBRACE}[ch], ch, line_no, start_col + i))
            i += 1
            continue

        if ch in ")]}":
            tokens.append(Token({")": TokenType.RPAREN, "]": TokenType.RBRACKET, "}": TokenType.RBRACE}[ch], ch, line_no, start_col + i))
            i += 1
            continue

        if ch == ",":
            tokens.append(Token(TokenType.COMMA, ch, line_no, start_col + i))
            i += 1
            continue

        if ch == ":":
            tokens.append(Token(TokenType.COLON, ch, line_no, start_col + i))
            i += 1
            continue

        if ch == ".":
            tokens.append(Token(TokenType.DOT, ch, line_no, start_col + i))
            i += 1
            continue

        if ch in "+-*/%<>=!&|^~":
            tokens.append(Token(TokenType.OPERATOR, ch, line_no, start_col + i))
            i += 1
            continue

        if ch in "'\"":
            quote = ch
            j = i + 1
            while j < length:
                if segment[j] == "\\":
                    j += 2
                    continue
                if segment[j] == quote:
                    j += 1
                    break
                j += 1
            value = segment[i:j]
            tokens.append(Token(TokenType.STRING, value, line_no, start_col + i))
            i = j
            continue

        if ch.isdigit() or (ch == "." and i + 1 < length and segment[i + 1].isdigit()):
            j = i
            while j < length and (segment[j].isdigit() or segment[j] in ".eE+-"):
                j += 1
            tokens.append(Token(TokenType.NUMBER, segment[i:j], line_no, start_col + i))
            i = j
            continue

        if ch.isalpha() or ch == "_":
            j = i
            while j < length and (segment[j].isalnum() or segment[j] == "_"):
                j += 1
            value = segment[i:j]
            token_type = TokenType.KEYWORD if value in KEYWORDS else TokenType.IDENTIFIER
            tokens.append(Token(token_type, value, line_no, start_col + i))
            i = j
            continue

        raise ValueError(f"Unsupported token at {line_no}:{start_col + i}: {ch!r}")

    return tokens


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    indent_stack = [0]
    lines = source.splitlines()

    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        leading = len(line) - len(line.lstrip(" "))
        if leading > indent_stack[-1]:
            indent_stack.append(leading)
            tokens.append(Token(TokenType.INDENT, " " * leading, line_no, 1))
        elif leading < indent_stack[-1]:
            while indent_stack and leading < indent_stack[-1]:
                indent_stack.pop()
                tokens.append(Token(TokenType.DEDENT, "", line_no, 1))
            if leading != indent_stack[-1]:
                raise IndentationError(f"Inconsistent indentation at line {line_no}")

        body = line.strip()
        tokens.extend(_tokenize_segment(body, line_no, leading + 1))
        tokens.append(Token(TokenType.NEWLINE, "\n", line_no, len(line) + 1))

    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(Token(TokenType.DEDENT, "", len(lines), 1))

    tokens.append(Token(TokenType.EOF, "", len(lines) + 1, 1))
    return tokens
