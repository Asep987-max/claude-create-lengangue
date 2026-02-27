"""
Semantic Validator.
"""
from .parser import *
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from pipeline.error_types import ExkutorSyntaxError

class SemanticValidator:
    def validate(self, ast):
        for n in ast:
            if n.directive not in ["run_shell","run_chain","set_env","assert_exists","log"]: raise ExkutorSyntaxError(f"Unknown directive {n.directive}", n.source_line)
            if n.directive in ["run_shell","assert_exists","run_chain"] and not n.target: raise ExkutorSyntaxError(f"Missing target for {n.directive}", n.source_line)
            if not n.command_string: raise ExkutorSyntaxError("Empty command", n.source_line)
            if isinstance(n, SetEnvNode) and '=' not in n.command_string: raise ExkutorSyntaxError("set_env format VAR=VAL", n.source_line)
