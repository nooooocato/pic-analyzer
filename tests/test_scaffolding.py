import os

def test_directory_structure():
    expected_dirs = ['src', 'plugins', 'assets']
    for d in expected_dirs:
        assert os.path.isdir(d), f"Directory {d} should exist"

def test_requirements_file():
    assert os.path.isfile('requirements.txt'), "requirements.txt should exist"
    with open('requirements.txt', 'r') as f:
        content = f.read()
        assert 'PySide6' in content, "PySide6 should be in requirements.txt"

def test_package_structure():
    assert os.path.isfile('src/__init__.py'), "src/__init__.py should exist"
