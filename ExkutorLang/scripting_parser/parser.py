"""
Parser for ExkutorLang.
"""
from typing import List, Optional
from .lexer import Token, TokenType
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from pipeline.error_types import ExkutorSyntaxError

class ASTNode:
    def __init__(self, d, c, t, l): self.directive=d; self.command_string=c; self.target=t; self.source_line=l
class RunShellNode(ASTNode): pass
class RunChainNode(ASTNode): pass
class SetEnvNode(ASTNode): pass
class AssertExistsNode(ASTNode): pass
class LogNode(ASTNode): pass

class Parser:
    def __init__(self, t): self.tokens=t; self.pos=0
    def parse(self):
        ast=[]
        while self.pos<len(self.tokens):
            t=self.tokens[self.pos]
            if t.type==TokenType.EOF: break
            if t.type==TokenType.NEWLINE: self.pos+=1; continue
            if t.type==TokenType.DIRECTIVE: ast.append(self._stmt())
            else: raise ExkutorSyntaxError(f"Expected directive", t.line)
        return ast
    def _stmt(self):
        d=self._eat(TokenType.DIRECTIVE); self._eat(TokenType.COLON); c=self._eat(TokenType.STRING)
        t=None
        if self._peek()==TokenType.ARROW: self._eat(TokenType.ARROW); self._eat(TokenType.TARGET_KW); self._eat(TokenType.COLON); t=self._eat(TokenType.TARGET_VALUE).value
        if self.pos<len(self.tokens) and self.tokens[self.pos].type not in (TokenType.NEWLINE, TokenType.EOF): raise ExkutorSyntaxError("Expected EOL", d.line)
        cls=RunShellNode
        if d.value=="run_chain": cls=RunChainNode
        elif d.value=="set_env": cls=SetEnvNode
        elif d.value=="assert_exists": cls=AssertExistsNode
        elif d.value=="log": cls=LogNode
        return cls(d.value, c.value, t, d.line)
    def _eat(self, typ):
        if self.pos<len(self.tokens) and self.tokens[self.pos].type==typ: t=self.tokens[self.pos]; self.pos+=1; return t
        raise ExkutorSyntaxError(f"Expected {typ.name}", -1)
    def _peek(self): return self.tokens[self.pos].type if self.pos<len(self.tokens) else None
