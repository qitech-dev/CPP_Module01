#!/usr/bin/env python3
"""CPP01/ex04 -- black-box tests for the file-replacement executable.

Place this file beside main.cpp and Makefile, then run:
    python3 test_ex04.py

The tests compile with the project's Makefile and run in a temporary directory;
none of the test input/output files are written into your project.
"""

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXECUTABLE = ROOT / "replace"
passed = 0
failed = 0


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print("[PASS] " + name)
    else:
        failed += 1
        print("[FAIL] " + name)
        if detail:
            print("       " + detail)


def run(args):
    try:
        return subprocess.run(
            [str(EXECUTABLE)] + [str(arg) for arg in args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Program timed out (>10 s)")


def test_replace(workdir, name, original, s1, s2, expected, filename="input.txt"):
    """Verify exit status, exact output bytes, and unchanged original file."""
    with tempfile.TemporaryDirectory(dir=str(workdir)) as folder:
        source = Path(folder) / filename
        source.write_bytes(original)
        dest = Path(str(source) + ".replace")
        try:
            result = run([source, s1, s2])
            ok = (result.returncode == 0 and dest.is_file()
                  and dest.read_bytes() == expected
                  and source.read_bytes() == original)
            detail = ("exit={}, actual={!r}, expected={!r}, stdout={!r}, stderr={!r}"
                      .format(result.returncode,
                              dest.read_bytes() if dest.is_file() else None,
                              expected, result.stdout, result.stderr))
        except RuntimeError as exc:
            ok, detail = False, str(exc)
        check(name, ok, "" if ok else detail)


def test_error(workdir, name, args, source=None):
    """Invalid calls must fail (nonzero exit status)."""
    try:
        result = run(args)
        ok = result.returncode != 0
        if source is not None:
            ok = ok and not Path(str(source) + ".replace").exists()
        detail = "exit={}, stdout={!r}, stderr={!r}".format(
            result.returncode, result.stdout, result.stderr)
    except RuntimeError as exc:
        ok, detail = False, str(exc)
    check(name, ok, "" if ok else detail)


def main():
    try:
        build = subprocess.run(["make", "-s", "all"], cwd=str(ROOT),
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as exc:
        print("[FAIL] Cannot run make: {}".format(exc))
        return 1
    if build.returncode != 0 or not EXECUTABLE.is_file():
        print("[FAIL] Build failed (check main.cpp and Makefile)")
        print((build.stdout + build.stderr).decode("utf-8", errors="replace"))
        return 1
    print("[PASS] Build with Makefile")

    with tempfile.TemporaryDirectory(prefix="cpp01-ex04-") as tmp:
        workdir = Path(tmp)

        # Expected results are explicit rather than computed by the program under test.
        test_replace(workdir, "single occurrence", b"hello world\n", "world", "42", b"hello 42\n")
        test_replace(workdir, "multiple occurrences", b"cat cat cat", "cat", "dog", b"dog dog dog")
        test_replace(workdir, "pattern absent", b"abc\n", "xyz", "Q", b"abc\n")
        test_replace(workdir, "empty replacement", b"banana", "na", "", b"ba")
        test_replace(workdir, "same search and replacement", b"abc abc", "abc", "abc", b"abc abc")
        test_replace(workdir, "replacement contains search", b"a-a", "a", "aa", b"aa-aa")
        test_replace(workdir, "longer replacement", b"X X", "X", "LONG", b"LONG LONG")
        test_replace(workdir, "non-overlapping matches", b"aaaaa", "aa", "X", b"XXa")
        test_replace(workdir, "search across newline", b"abc\ndef", "c\nd", "X", b"abXef")
        test_replace(workdir, "empty input file", b"", "abc", "X", b"")
        test_replace(workdir, "no trailing newline", b"abc", "b", "X", b"aXc")
        test_replace(workdir, "multiple empty lines", b"\n\nabc\n\n", "abc", "X", b"\n\nX\n\n")
        test_replace(workdir, "CRLF line endings", b"cat\r\ncat\r\n", "cat", "dog", b"dog\r\ndog\r\n")
        test_replace(workdir, "binary input with NUL bytes", b"\x00cat\x00cat\xff", "cat", "dog", b"\x00dog\x00dog\xff")
        test_replace(workdir, "UTF-8 text", "你好，世界！你好".encode(), "你好", "Hello", "Hello，世界！Hello".encode())
        test_replace(workdir, "spaces in filename", b"hello", "hello", "yes", b"yes", "file with spaces.txt")
        test_replace(workdir, "case-sensitive replacement", b"ABC abc Abc", "abc", "X", b"ABC X Abc")

        source = workdir / "errors.txt"
        source.write_bytes(b"abc")
        test_error(workdir, "missing arguments", [])
        test_error(workdir, "too few arguments", [source, "a"])
        test_error(workdir, "too many arguments", [source, "a", "b", "extra"])
        test_error(workdir, "empty search string", [source, "", "X"], source)
        missing = workdir / "no_such_file.txt"
        test_error(workdir, "missing input file", [missing, "a", "X"], missing)

        # An existing directory at the destination path prevents file creation.
        output_as_directory = Path(str(source) + ".replace")
        output_as_directory.mkdir()
        try:
            result = run([source, "a", "X"])
            check("cannot create output file", result.returncode != 0
                  and source.read_bytes() == b"abc",
                  "expected a nonzero exit code without modifying input")
        except RuntimeError as exc:
            check("cannot create output file", False, str(exc))
        output_as_directory.rmdir()

        # Existing output must be replaced, not appended to.
        output_as_directory.write_bytes(b"OLD OUTPUT")
        try:
            result = run([source, "a", "X"])
            check("overwrite existing .replace file",
                  result.returncode == 0
                  and output_as_directory.read_bytes() == b"Xbc")
        except RuntimeError as exc:
            check("overwrite existing .replace file", False, str(exc))

    print("\nResults: {} passed, {} failed".format(passed + 1, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
