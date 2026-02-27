"""
Runtime.
"""
import os
import sys
try: import exkutor_core_binding
except: exkutor_core_binding=None
from .parser import *
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from pipeline.error_types import *
from pipeline.logger import *

class Runtime:
    def __init__(self):
        if not exkutor_core_binding: raise ExkutorBridgeError("Binding missing")
        if hasattr(exkutor_core_binding, 'set_bridge_error_type'): exkutor_core_binding.set_bridge_error_type(ExkutorBridgeError)
    def run(self, ast):
        for n in ast:
            if isinstance(n, RunShellNode): self._exec(n.command_string, n.target, n)
            elif isinstance(n, RunChainNode): self._exec(n.command_string, n.target+":chain", n)
            elif isinstance(n, SetEnvNode): k,v=n.command_string.split('=',1); os.environ[k]=v
            elif isinstance(n, AssertExistsNode):
                cmd = f"test -e \"{n.command_string}\"" if n.target=="wsl" else f"Get-Item \"{n.command_string}\""
                res = exkutor_core_binding.execute_command(cmd, n.target)
                if res.exit_code!=0: raise ExkutorAssertionError(f"Assert failed: {n.command_string}", n.target)
            elif isinstance(n, LogNode): log_info(n.command_string, n.target or "")
    def _exec(self, c, t, n):
        log_info(f"Exec: {c}", n.target)
        res = exkutor_core_binding.execute_command(c, t)
        if res.exit_code!=0: raise ExkutorShellError(f"Failed: {res.exit_code}", n.target, raw_stderr=res.stderr_out)
        if res.stdout_out: print(res.stdout_out, end="")
