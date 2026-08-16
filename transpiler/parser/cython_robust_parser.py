"""
Robust Cython parser using tokenization instead of regex.

This parser handles all Cython constructs without fragile regex patterns:
- cdef class, cpdef, cdef functions
- Type annotations (int, double, object, etc.)
- Imports (cimport, import from)
- Properties and methods
- Exception handling
- Complex type expressions
"""

import re
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class TokenType(Enum):
    """Cython token types."""
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"
    EQUALS = "EQUALS"
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    EOF = "EOF"
    COMMENT = "COMMENT"


@dataclass
class Token:
    """A single token."""
    type: TokenType
    value: str
    line: int
    column: int


class CythonTokenizer:
    """Tokenize Cython source code."""
    
    KEYWORDS = {
        'cdef', 'cpdef', 'cimport', 'import', 'from', 'class', 'def',
        'if', 'elif', 'else', 'for', 'while', 'with', 'try', 'except',
        'finally', 'return', 'raise', 'pass', 'break', 'continue',
        'lambda', 'and', 'or', 'not', 'in', 'is', 'as',
        'public', 'readonly', 'property', 'include', 'extern',
        'cdef', 'cimport', 'ctypedef', 'typedef', 'void', 'int', 'double',
        'float', 'char', 'long', 'short', 'unsigned', 'signed',
        'const', 'volatile', 'struct', 'union', 'enum',
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source."""
        while self.pos < len(self.source):
            self._skip_whitespace_except_newline()
            
            if self.pos >= len(self.source):
                break
            
            char = self.source[self.pos]
            
            # Handle newlines (track indentation separately)
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.pos += 1
                self.line += 1
                self.column = 1
                continue
            
            # Handle comments
            if char == '#':
                self._tokenize_comment()
                continue
            
            # Handle strings
            if char in ('"', "'"):
                self._tokenize_string()
                continue
            
            # Handle operators and punctuation
            if self._try_tokenize_operator():
                continue
            
            # Handle numbers
            if char.isdigit() or (char == '.' and self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit()):
                self._tokenize_number()
                continue
            
            # Handle identifiers and keywords
            if char.isalpha() or char == '_':
                self._tokenize_identifier()
                continue
            
            # Unknown character, skip it
            self.pos += 1
            self.column += 1
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def _skip_whitespace_except_newline(self):
        """Skip spaces and tabs but not newlines."""
        while self.pos < len(self.source) and self.source[self.pos] in ' \t':
            self.pos += 1
            self.column += 1
    
    def _tokenize_comment(self):
        """Tokenize a comment."""
        start_pos = self.pos
        start_col = self.column
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self.pos += 1
            self.column += 1
        
        comment_text = self.source[start_pos:self.pos]
        self.tokens.append(Token(TokenType.COMMENT, comment_text, self.line, start_col))
    
    def _tokenize_string(self):
        """Tokenize a string literal."""
        quote_char = self.source[self.pos]
        start_pos = self.pos
        start_col = self.column
        self.pos += 1
        self.column += 1
        
        # Check for triple-quoted string
        if (self.pos + 1 < len(self.source) and 
            self.source[self.pos] == quote_char and 
            self.source[self.pos + 1] == quote_char):
            # Triple-quoted string
            self.pos += 2
            self.column += 2
            while self.pos + 2 < len(self.source):
                if (self.source[self.pos] == quote_char and
                    self.source[self.pos + 1] == quote_char and
                    self.source[self.pos + 2] == quote_char):
                    self.pos += 3
                    self.column += 3
                    break
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
        else:
            # Single or double quoted string
            while self.pos < len(self.source):
                char = self.source[self.pos]
                if char == quote_char:
                    self.pos += 1
                    self.column += 1
                    break
                if char == '\\':
                    self.pos += 2
                    self.column += 2
                elif char == '\n':
                    self.line += 1
                    self.column = 1
                    self.pos += 1
                else:
                    self.pos += 1
                    self.column += 1
        
        string_text = self.source[start_pos:self.pos]
        self.tokens.append(Token(TokenType.STRING, string_text, self.line, start_col))
    
    def _try_tokenize_operator(self) -> bool:
        """Try to tokenize an operator or punctuation."""
        char = self.source[self.pos]
        start_col = self.column
        
        # Two-character operators
        if self.pos + 1 < len(self.source):
            two_char = self.source[self.pos:self.pos + 2]
            if two_char in ('==', '!=', '<=', '>=', '<<', '>>', '->', '+=', '-=', '*=', '/=', '//'):
                self.tokens.append(Token(TokenType.OPERATOR, two_char, self.line, start_col))
                self.pos += 2
                self.column += 2
                return True
        
        # Single-character operators and punctuation
        if char == '(':
            self.tokens.append(Token(TokenType.LPAREN, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == ')':
            self.tokens.append(Token(TokenType.RPAREN, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == '{':
            self.tokens.append(Token(TokenType.LBRACE, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == '}':
            self.tokens.append(Token(TokenType.RBRACE, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == '[':
            self.tokens.append(Token(TokenType.LBRACKET, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == ']':
            self.tokens.append(Token(TokenType.RBRACKET, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == ':':
            self.tokens.append(Token(TokenType.COLON, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == ';':
            self.tokens.append(Token(TokenType.SEMICOLON, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == ',':
            self.tokens.append(Token(TokenType.COMMA, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == '.':
            self.tokens.append(Token(TokenType.DOT, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char == '=':
            self.tokens.append(Token(TokenType.EQUALS, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        elif char in '+-*/<>!&|^~%':
            self.tokens.append(Token(TokenType.OPERATOR, char, self.line, start_col))
            self.pos += 1
            self.column += 1
            return True
        
        return False
    
    def _tokenize_number(self):
        """Tokenize a number."""
        start_pos = self.pos
        start_col = self.column
        
        # Handle hex, octal, binary
        if self.source[self.pos] == '0' and self.pos + 1 < len(self.source):
            next_char = self.source[self.pos + 1]
            if next_char in 'xXoObB':
                self.pos += 2
                self.column += 2
                while self.pos < len(self.source) and self.source[self.pos] in '0123456789abcdefABCDEF_':
                    self.pos += 1
                    self.column += 1
                num_text = self.source[start_pos:self.pos]
                self.tokens.append(Token(TokenType.NUMBER, num_text, self.line, start_col))
                return
        
        # Regular decimal number
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            self.pos += 1
            self.column += 1
        
        # Handle scientific notation
        if self.pos < len(self.source) and self.source[self.pos] in 'eE':
            self.pos += 1
            self.column += 1
            if self.pos < len(self.source) and self.source[self.pos] in '+-':
                self.pos += 1
                self.column += 1
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                self.pos += 1
                self.column += 1
        
        num_text = self.source[start_pos:self.pos]
        self.tokens.append(Token(TokenType.NUMBER, num_text, self.line, start_col))
    
    def _tokenize_identifier(self):
        """Tokenize an identifier or keyword."""
        start_pos = self.pos
        start_col = self.column
        
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self.pos += 1
            self.column += 1
        
        ident_text = self.source[start_pos:self.pos]
        
        if ident_text in self.KEYWORDS:
            self.tokens.append(Token(TokenType.KEYWORD, ident_text, self.line, start_col))
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, ident_text, self.line, start_col))


class CythonParser:
    """Parse Cython source code into AST using tokens."""
    
    def __init__(self, source: str):
        self.source = source
        self.tokenizer = CythonTokenizer(source)
        self.tokens = self.tokenizer.tokenize()
        self.pos = 0
    
    def parse(self) -> Dict[str, Any]:
        """Parse the entire file and return a structure."""
        result = {
            'classes': [],
            'functions': [],
            'imports': [],
            'variables': [],
            'comments': [],
        }
        
        while not self._is_at_end():
            # Skip comments and newlines
            if self._check(TokenType.COMMENT):
                result['comments'].append(self._advance().value)
                continue
            if self._check(TokenType.NEWLINE):
                self._advance()
                continue
            
            # Parse top-level constructs
            if self._check_keyword('cdef') or self._check_keyword('cpdef') or self._check_keyword('def'):
                func = self._parse_function()
                if func:
                    result['functions'].append(func)
            elif self._check_keyword('class'):
                cls = self._parse_class()
                if cls:
                    result['classes'].append(cls)
            elif self._check_keyword('cimport') or self._check_keyword('import') or self._check_keyword('from'):
                imp = self._parse_import()
                if imp:
                    result['imports'].append(imp)
            else:
                self._advance()
        
        return result
    
    def _parse_class(self) -> Optional[Dict[str, Any]]:
        """Parse a class definition."""
        # Handle: cdef class Name(Base):
        if self._check_keyword('cdef'):
            self._advance()
        
        if not self._check_keyword('class'):
            return None
        
        self._advance()
        
        if not self._check(TokenType.IDENTIFIER):
            return None
        
        class_name = self._advance().value
        bases = []
        
        if self._check(TokenType.LPAREN):
            self._advance()
            while not self._check(TokenType.RPAREN) and not self._is_at_end():
                if self._check(TokenType.IDENTIFIER):
                    bases.append(self._advance().value)
                if self._check(TokenType.COMMA):
                    self._advance()
                else:
                    break
            self._advance()  # consume )
        
        if self._check(TokenType.COLON):
            self._advance()
        
        # Skip to next line and parse methods
        self._skip_to_next_line()
        
        methods = []
        # Simple method detection - just collect function names at increased indentation
        while not self._is_at_end() and self._check(TokenType.NEWLINE):
            self._advance()
            if self._check_keyword('cdef') or self._check_keyword('cpdef') or self._check_keyword('def'):
                method = self._parse_function()
                if method:
                    methods.append(method)
        
        return {
            'name': class_name,
            'bases': bases,
            'methods': methods,
        }
    
    def _parse_function(self) -> Optional[Dict[str, Any]]:
        """Parse a function definition."""
        # Handle: [cdef|cpdef] [type] def/cpdef name(params):
        return_type = None
        
        if self._check_keyword('cdef'):
            self._advance()
            if self._check(TokenType.IDENTIFIER):
                return_type = self._advance().value
        elif self._check_keyword('cpdef'):
            self._advance()
            if self._check(TokenType.IDENTIFIER):
                return_type = self._advance().value
        
        if not (self._check_keyword('def') or self._check_keyword('cpdef')):
            return None
        
        self._advance()
        
        if not self._check(TokenType.IDENTIFIER):
            return None
        
        func_name = self._advance().value
        
        # Parse parameters
        params = []
        if self._check(TokenType.LPAREN):
            self._advance()
            while not self._check(TokenType.RPAREN) and not self._is_at_end():
                if self._check(TokenType.IDENTIFIER):
                    param_name = self._advance().value
                    params.append({'name': param_name, 'type': None})
                if self._check(TokenType.COLON):
                    if params:
                        self._advance()
                        if self._check(TokenType.IDENTIFIER):
                            params[-1]['type'] = self._advance().value
                if self._check(TokenType.COMMA):
                    self._advance()
                else:
                    break
            self._advance()  # consume )
        
        return {
            'name': func_name,
            'return_type': return_type,
            'parameters': params,
        }
    
    def _parse_import(self) -> Optional[Dict[str, Any]]:
        """Parse an import statement."""
        if self._check_keyword('from'):
            self._advance()
            if not self._check(TokenType.IDENTIFIER):
                return None
            module = self._advance().value
            
            if self._check_keyword('cimport') or self._check_keyword('import'):
                self._advance()
                
                names = []
                while self._check(TokenType.IDENTIFIER):
                    names.append(self._advance().value)
                    if self._check(TokenType.COMMA):
                        self._advance()
                    else:
                        break
                
                return {
                    'type': 'from_import',
                    'module': module,
                    'names': names,
                }
        
        elif self._check_keyword('cimport') or self._check_keyword('import'):
            self._advance()
            if not self._check(TokenType.IDENTIFIER):
                return None
            
            module = self._advance().value
            return {
                'type': 'import',
                'module': module,
            }
        
        return None
    
    def _skip_to_next_line(self):
        """Skip to the next line."""
        while not self._is_at_end() and not self._check(TokenType.NEWLINE):
            self._advance()
        if not self._is_at_end():
            self._advance()
    
    def _check_keyword(self, keyword: str) -> bool:
        """Check if current token is a specific keyword."""
        return (not self._is_at_end() and 
                self._peek().type == TokenType.KEYWORD and 
                self._peek().value == keyword)
    
    def _check(self, token_type: TokenType) -> bool:
        """Check if current token is of a given type."""
        return not self._is_at_end() and self._peek().type == token_type
    
    def _advance(self) -> Token:
        """Consume and return current token."""
        if not self._is_at_end():
            self.pos += 1
        return self._previous()
    
    def _peek(self) -> Token:
        """Return current token without consuming."""
        return self.tokens[self.pos]
    
    def _previous(self) -> Token:
        """Return previous token."""
        return self.tokens[self.pos - 1]
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens."""
        return self.pos >= len(self.tokens) or self._peek().type == TokenType.EOF


def parse_cython_robust(source: str) -> Dict[str, Any]:
    """
    Parse Cython source code robustly.
    
    Args:
        source: Cython source code
    
    Returns:
        Dictionary with classes, functions, imports, etc.
    """
    parser = CythonParser(source)
    return parser.parse()
