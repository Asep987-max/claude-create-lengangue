"""
Lexer for ExkutorLang.
"""
from typing import List, Optional
from enum import Enum, auto
import sys
import os

# Fix path to include pipeline module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) # ExkutorLang root
sys.path.append(parent_dir)

try:
    from pipeline.error_types import ExkutorSyntaxError
except ImportError:
    # If package structure is weird, fallback
    from error_types import ExkutorSyntaxError

class TokenType(Enum):
    DIRECTIVE = auto(); COLON = auto(); STRING = auto(); ARROW = auto(); TARGET_KW = auto(); TARGET_VALUE = auto(); NEWLINE = auto(); EOF = auto()

class Token:
    def __init__(self, t, v, l): self.type=t; self.value=v; self.line=l
    def __repr__(self): return f"Token({self.type.name}, '{self.value}')"

class Lexer:
    def __init__(self, s): self.source=s; self.pos=0; self.line=1; self.tokens=[]
    def tokenize(self):
        while self.pos < len(self.source):
            c = self.source[self.pos]
            if c=='#': self._comment()
            elif c=='\n': self.tokens.append(Token(TokenType.NEWLINE,"\n",self.line)); self.line+=1; self.pos+=1
            elif c.isspace(): self.pos+=1
            elif c=='"': self._string()
            elif c==':': self.tokens.append(Token(TokenType.COLON,":",self.line)); self.pos+=1
            elif c=='-' and self._peek()=='>': self.tokens.append(Token(TokenType.ARROW,"->",self.line)); self.pos+=2
            elif c.isalnum() or c=='_': self._ident()
            else: raise ExkutorSyntaxError(f"Unexpected: {c}", self.line)
        self.tokens.append(Token(TokenType.EOF,"",self.line))
        return self.tokens
    def _peek(self): return self.source[self.pos+1] if self.pos+1<len(self.source) else None
    def _comment(self):
        while self.pos<len(self.source) and self.source[self.pos]!='\n': self.pos+=1
    def _string(self):
        sl=self.line; self.pos+=1; v=""
        while self.pos<len(self.source):
            c=self.source[self.pos]
            if c=='"': self.pos+=1; self.tokens.append(Token(TokenType.STRING,v,sl)); return
            elif c=='\n': raise ExkutorSyntaxError("Unterminated string", sl)
            v+=c; self.pos+=1
        raise ExkutorSyntaxError("EOF in string", sl)
    def _ident(self):
        sp=self.pos
        while self.pos<len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos]=='_'): self.pos+=1
        v=self.source[sp:self.pos]
        if v=="target": self.tokens.append(Token(TokenType.TARGET_KW,v,self.line))
        elif v in ["wsl","powershell"]: self.tokens.append(Token(TokenType.TARGET_VALUE,v,self.line))
        else: self.tokens.append(Token(TokenType.DIRECTIVE,v,self.line))
