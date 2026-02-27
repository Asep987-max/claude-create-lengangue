import os
import sys
import subprocess
import shutil

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")

def main():
    print(f"Building ExkutorLang from {PROJECT_ROOT}...")
    try: subprocess.check_call(["cmake", "--version"], stdout=subprocess.DEVNULL)
    except:
        print("Error: CMake is not installed.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(BUILD_DIR): os.makedirs(BUILD_DIR)

    root_cmake = os.path.join(PROJECT_ROOT, "CMakeLists.txt")
    if not os.path.exists(root_cmake):
        with open(root_cmake, "w") as f:
            f.write("cmake_minimum_required(VERSION 3.20)\nproject(ExkutorLang)\nadd_subdirectory(core_execution)\nadd_subdirectory(bindings)\n")

    try:
        import pybind11
        pybind11_cmake_dir = pybind11.get_cmake_dir()
    except ImportError:
        print("Error: pybind11 not installed.", file=sys.stderr)
        sys.exit(1)

    os.chdir(BUILD_DIR)
    cmd = ["cmake", "..", f"-Dpybind11_DIR={pybind11_cmake_dir}"]
    print(f"Running configuration: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    print("Building...")
    subprocess.check_call(["cmake", "--build", ".", "--config", "Release"])

    artifact_path = None
    for root, dirs, files in os.walk(BUILD_DIR):
        for file in files:
            if file.startswith("exkutor_core_binding") and (file.endswith(".so") or file.endswith(".pyd")):
                artifact_path = os.path.join(root, file)
                break
        if artifact_path: break

    if artifact_path:
        dest = os.path.join(PROJECT_ROOT, os.path.basename(artifact_path))
        shutil.copy2(artifact_path, dest)
        print(f"Build successful. Artifact copied to: {dest}")
    else:
        print("Error: Build completed but artifact not found.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__": main()
