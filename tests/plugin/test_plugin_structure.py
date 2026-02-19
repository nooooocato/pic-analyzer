import os

def test_plugin_directory_exists():
    assert os.path.exists("plugins")
    assert os.path.isdir("plugins")

def test_plugin_subdirectories_exist():
    subdirs = ["sort", "group"]
    for subdir in subdirs:
        path = os.path.join("plugins", subdir)
        assert os.path.exists(path)
        assert os.path.isdir(path)
        assert os.path.exists(os.path.join(path, "__init__.py"))
