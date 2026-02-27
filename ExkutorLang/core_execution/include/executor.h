#ifndef EXECUTOR_H
#define EXECUTOR_H
#include <string>
struct ExecutionResult { std::string stdout_out; std::string stderr_out; int exit_code; bool sanitizer_passed; };
class Executor { public: static ExecutionResult execute(const std::string& command, const std::string& target); };
#endif
