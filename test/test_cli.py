import pytest

from potojson.__main__ import run
from test import POFILE_START


@pytest.mark.parametrize('arg', ['-m', '--fallback-to-msgid'])
def test_fallback_to_msgid(capsys, arg):
    pofile_content = POFILE_START + 'msgid "Hello"\nmsgstr ""\n'
    output, exitcode = run([pofile_content, arg])
    out, err = capsys.readouterr()

    expected_output = '{"Hello": "Hello"}\n'
    assert exitcode == 0
    assert output == expected_output
    assert out == expected_output


@pytest.mark.parametrize('arg', ['-f', '--fuzzy'])
def test_fuzzy(capsys, arg):
    pofile_content = POFILE_START + '#, fuzzy\nmsgid "Hello"\nmsgstr "Hola"\n'
    output, exitcode = run([pofile_content, arg])
    out, err = capsys.readouterr()

    expected_output = '{"Hello": "Hola"}\n'
    assert exitcode == 0
    assert output == expected_output
    assert out == expected_output


@pytest.mark.parametrize('arg', ['-p', '--pretty'])
def test_pretty(capsys, arg):
    pofile_content = POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\n'
    output, exitcode = run([pofile_content, arg])
    out, err = capsys.readouterr()

    expected_output = '{\n  "Hello": "Hola"\n}\n'
    assert exitcode == 0
    assert output == expected_output
    assert out == expected_output


@pytest.mark.parametrize('arg', ['-i', '--indent'])
def test_indent(capsys, arg):
    pofile_content = POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\n'
    output, exitcode = run([pofile_content, arg, '3', '-p'])
    out, err = capsys.readouterr()

    expected_output = '{\n   "Hello": "Hola"\n}\n'
    assert exitcode == 0
    assert output == expected_output
    assert out == expected_output


@pytest.mark.parametrize('arg', ['-i', '--indent'])
def test_indent_no_pretty(capsys, arg):
    pofile_content = POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\n'
    output, exitcode = run([pofile_content, arg, '3'])
    out, err = capsys.readouterr()

    # without pretty doesn't work
    expected_output = '{"Hello": "Hola"}\n'
    assert exitcode == 0
    assert output == expected_output
    assert out == expected_output


@pytest.mark.parametrize('arg', ['-l', '--language'])
def test_language(capsys, arg):
    pofile_content = POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\n'
    output, exitcode = run([pofile_content, arg, 'es'])
    out, err = capsys.readouterr()

    expected_output = '{"Hello": "Hola", "": {"language": "es"}}\n'
    assert exitcode == 0
    assert output == expected_output
    assert out == expected_output


@pytest.mark.parametrize('arg', ['-s', '--plural-forms'])
def test_plural_forms(capsys, arg):
    pofile_content = POFILE_START + 'msgid "Hello"\nmsgstr "Hola"\n'
    output, exitcode = run([pofile_content, arg, 'nplurals=2; plural=n != 1;'])
    out, err = capsys.readouterr()

    expected_output = ('{"Hello": "Hola", '
                       '"": {"plural-forms": "nplurals=2; plural=n != 1;"}}\n')
    assert exitcode == 0
    assert output == expected_output
    assert out == expected_output