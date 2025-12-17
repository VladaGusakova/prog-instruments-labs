import os
import json
import tempfile
import pytest

from lab_6.file_manager import FileManager


@pytest.fixture
def fm():
    return FileManager()


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


def test_read_key_length_success(fm, temp_dir):
    path = os.path.join(temp_dir, "keylen.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("2048")

    assert fm.read_key_length_from_file(path) == 2048


def test_read_key_length_invalid_content(fm, temp_dir):
    path = os.path.join(temp_dir, "keylen.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("not_a_number")

    with pytest.raises(IOError):
        fm.read_key_length_from_file(path)


def test_write_and_read_file(fm, temp_dir):
    data = b"hello world"
    path = os.path.join(temp_dir, "sub", "file.bin")

    fm.write_file(data, path)
    result = fm.read_file(path)

    assert result == data


def test_load_json_config_success(fm, temp_dir):
    config_data = {"a": 1, "b": "text"}
    path = os.path.join(temp_dir, "config.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(config_data, f)

    result = fm.load_json_config(path)
    assert result == config_data


@pytest.mark.parametrize(
    "content,expected",
    [
        ("0", 0),
        ("16", 16),
        ("4096", 4096),
    ],
)
def test_read_key_length_parametrized(fm, temp_dir, content, expected):
    path = os.path.join(temp_dir, "keylen.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    assert fm.read_key_length_from_file(path) == expected


def test_save_private_key_calls_write_file(monkeypatch, fm):
    class FakePrivateKey:
        def private_bytes(self, **kwargs):
            return b"PEM_DATA"

    calls = {}

    def fake_write(data, path):
        calls['data'] = data
        calls['path'] = path

    monkeypatch.setattr(fm, "write_file", fake_write)

    fm.save_private_key_pem(FakePrivateKey(), "some/path/key.pem")

    assert calls['data'] == b"PEM_DATA"
    assert calls['path'] == "some/path/key.pem"


def test_load_private_key_uses_read_file(monkeypatch, fm):
    monkeypatch.setattr(fm, "read_file", lambda path: b"PEM_DATA")
    monkeypatch.setattr("lab_6.file_manager.load_pem_private_key", lambda data, password=None: "PRIVATE_KEY")

    result = fm.load_private_key_pem("key.pem")

    assert result == "PRIVATE_KEY"
