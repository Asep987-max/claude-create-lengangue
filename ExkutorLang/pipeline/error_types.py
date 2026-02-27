"""
Unified Error Pipeline for ExkutorLang.
"""
from typing import Dict, Optional

class ExkutorError(Exception):
    def __init__(self, error_type: str, message: str, source_line: Optional[int] = None, target_env: Optional[str] = None, timestamp: Optional[str] = None, raw_stderr: Optional[str] = None):
        self.error_type = error_type
        self.message = message
        self.source_line = source_line
        self.target_env = target_env
        self.timestamp = timestamp
        self.raw_stderr = raw_stderr
        super().__init__(self.message)
    def __str__(self) -> str:
        parts = [f"[{self.error_type}] {self.message}"]
        if self.source_line: parts.append(f"(Line {self.source_line})")
        if self.target_env: parts.append(f"[Target: {self.target_env}]")
        return " ".join(parts)
    def to_dict(self) -> Dict:
        return {"error_type": self.error_type, "message": self.message, "source_line": self.source_line, "target_env": self.target_env, "timestamp": self.timestamp, "raw_stderr": self.raw_stderr}

class ExkutorSyntaxError(ExkutorError):
    def __init__(self, message: str, source_line: int, **kwargs): super().__init__("ExkutorSyntaxError", message, source_line=source_line, **kwargs)
class ExkutorBridgeError(ExkutorError):
    def __init__(self, message: str, **kwargs): super().__init__("ExkutorBridgeError", message, **kwargs)
class ExkutorSanitizerError(ExkutorError):
    def __init__(self, message: str, target_env: str, **kwargs): super().__init__("ExkutorSanitizerError", message, target_env=target_env, **kwargs)
class ExkutorShellError(ExkutorError):
    def __init__(self, message: str, target_env: str, raw_stderr: str = "", **kwargs): super().__init__("ExkutorShellError", message, target_env=target_env, raw_stderr=raw_stderr, **kwargs)
class ExkutorAssertionError(ExkutorError):
    def __init__(self, message: str, target_env: str, **kwargs): super().__init__("ExkutorAssertionError", message, target_env=target_env, **kwargs)
