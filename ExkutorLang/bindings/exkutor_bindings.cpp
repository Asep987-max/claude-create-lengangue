#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "executor.h"
namespace py = pybind11;
py::object ExkutorBridgeError;
PYBIND11_MODULE(exkutor_core_binding, m) {
    m.doc() = "ExkutorLang Binding";
    py::class_<ExecutionResult>(m, "ExecutionResult")
        .def(py::init<>())
        .def_readwrite("stdout_out", &ExecutionResult::stdout_out)
        .def_readwrite("stderr_out", &ExecutionResult::stderr_out)
        .def_readwrite("exit_code", &ExecutionResult::exit_code)
        .def_readwrite("sanitizer_passed", &ExecutionResult::sanitizer_passed);
    m.def("execute_command", [](const std::string &c, const std::string &t) -> ExecutionResult {
        try { return Executor::execute(c, t); }
        catch (const std::exception &e) {
            if (ExkutorBridgeError && !ExkutorBridgeError.is(py::none())) { PyErr_SetString(ExkutorBridgeError.ptr(), e.what()); throw py::error_already_set(); }
            throw std::runtime_error(e.what());
        }
    });
    m.def("set_bridge_error_type", [](py::object c) { ExkutorBridgeError = c; });
}
