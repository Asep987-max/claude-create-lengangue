#ifndef EXKUTOR_SANITIZER_H
#define EXKUTOR_SANITIZER_H
#include <string>
struct SanitizeResult { bool passed; std::string rejection_reason; };
class Sanitizer { public: static SanitizeResult sanitize(const std::string& cmd, const std::string& target); };
#endif
