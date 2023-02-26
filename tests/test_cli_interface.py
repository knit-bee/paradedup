import subprocess
import tempfile
import os


def test_package_callable_without_error():
    process = subprocess.run(["paradedup", "--help"], check=True, capture_output=True)
    assert process.returncode == 0


def test_package_callable_with_arguements():
    with tempfile.TemporaryDirectory() as tempdir:
        for i in range(5):
            _, tmp_file = tempfile.mkstemp(".txt", dir=tempdir, text=True)
            with open(tmp_file, "w") as fp:
                fp.write("some text")
        process = subprocess.run(
            ["paradedup", tempdir, "-o", os.path.join(tempdir, "out")],
            check=True,
            capture_output=True,
        )
    assert process.returncode == 0
