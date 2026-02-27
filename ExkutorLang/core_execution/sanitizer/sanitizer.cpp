#include "sanitizer.h"
#include <iostream>
#include <algorithm>
#include <vector>

bool is_allowed(char c) {
    if (isalnum(c)) return true;
    std::string allowed = " -_./\\:\"$";
    return allowed.find(c) != std::string::npos;
}

bool contains_blocked(const std::string& cmd, bool allow_chaining) {
    std::vector<std::string> blocked = {";", "||", "$()", "`", ">&"};
    if (!allow_chaining) blocked.push_back("&&");
    for (const auto& p : blocked) if (cmd.find(p) != std::string::npos) return true;
    return false;
}

SanitizeResult Sanitizer::sanitize(const std::string& cmd, const std::string& target) {
    bool allow_chaining = (target.length() >= 6 && target.substr(target.length() - 6) == ":chain");
    if (contains_blocked(cmd, allow_chaining)) return {false, "Command contains blocked metacharacters"};
    for (char c : cmd) {
        if (!is_allowed(c)) {
            if (allow_chaining && c == '&') continue;
            return {false, std::string("Disallowed char: ") + c};
        }
    }
    return {true, ""};
}
