"""
ExkutorLang Entry Point.
"""
import sys
import os
import argparse
from scripting_parser.lexer import Lexer
from scripting_parser.parser import Parser
from scripting_parser.semantic import SemanticValidator
from scripting_parser.runtime import Runtime
from pipeline.logger import log_error, log_info
from pipeline.error_types import ExkutorError

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script")
    args = parser.parse_args()
    if not os.path.exists(args.script) or not args.script.endswith(".exkutor"): sys.exit(1)
    try:
        with open(args.script, "r") as f: source = f.read()
        ast = Parser(Lexer(source).tokenize()).parse()
        SemanticValidator().validate(ast)
        Runtime().run(ast)
        log_info("Execution completed successfully.")
        sys.exit(0)
    except ExkutorError as e: log_error(e); sys.exit(1)
    except Exception as e: print(f"CRITICAL: {e}", file=sys.stderr); sys.exit(1)

if __name__ == "__main__": main()
