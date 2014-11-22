from sh import python3, cat
from io import StringIO


path2main = 'unlog/main.py'
program_output = 'test/program_output'
program_output_filtered = 'test/program_output_filtered'


def test_basic_filter():
    output = StringIO()
    python3(path2main, program_output,
            start_pattern='/home/assos/drupal7/sites/assos.centrale-marseille.fr.\w',
            error_pattern='(error|warning)',
            _out=output)
    
    with open(program_output_filtered, 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()


def test_basic_filter_pipe():
    output = StringIO()
    python3(cat(program_output), path2main,
            start_pattern='/home/assos/drupal7/sites/assos.centrale-marseille.fr.\w',
            error_pattern='(error|warning)',
            _out=output)

    with open(program_output_filtered, 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()


def test_filter_pipe_config():
    output = StringIO()
    python3(cat(program_output), path2main, config='test/test_config',
            use_config_section='TEST', _out=output)

    with open(program_output_filtered, 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()


def test_basic_filter_config():
    "Filter the file according to the config file."
    output = StringIO()
    python3(path2main, 'test/program_output_config', config='test/test_config', _out=output)

    with open(program_output_filtered, 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()


def test_use_config_section():
    output = StringIO()
    python3(path2main, program_output, u='TEST',
            config='test/test_config', _out=output)

    with open(program_output_filtered, 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()


def test_mail():
    output = StringIO()
    python3(path2main, 'test/program_output_mail', config='test/test_config', _err=output)

    with open('test/program_output_filtered_mail', 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()

def test_mail_empty_mail():
    output = StringIO()
    python3(path2main, 'test/program_output_mail_empty', config='test/test_config', _err=output)

    correctly_filtered_output = ''
    assert correctly_filtered_output == output.getvalue()

def test_mail_empty_mail_group():
    output = StringIO()
    python3(path2main, 'test/program_output_mail_empty_group', config='test/test_config', _err=output)

    correctly_filtered_output = ''
    assert correctly_filtered_output == output.getvalue()


def test_filter_group():
    output = StringIO()
    python3(path2main, 'test/program_output_group', config='test/test_config', _out=output)

    with open('test/program_output_filtered_group', 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()


def test_filter_end_file():
    file = 'test/program_output_end_file'
    filtered_output_file = 'test/program_output_filtered_end_file'
    # Test with the file passed as a parameter.
    output = StringIO()
    python3(path2main, file,
            start_pattern='/home/assos/drupal7/sites/assos.centrale-marseille.fr.\w',
            error_pattern='(error|warning)',
            _out=output)

    with open(filtered_output_file, 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()

    # Test with stdout
    output = StringIO()
    python3(cat(file), path2main,
        start_pattern='/home/assos/drupal7/sites/assos.centrale-marseille.fr.\w',
        error_pattern='(error|warning)',
        _out=output)

    with open(filtered_output_file, 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()


def test_filter_empty_group():
    file = 'test/program_output_empty_group'
    filtered_output_file = 'test/program_output_filtered_empty_group'
    # Test with the file passed as a parameter.
    output = StringIO()
    python3(path2main, file,
            start_pattern='/home/assos/drupal7/sites/assos.centrale-marseille.fr.\w',
            error_pattern='(error|warning)',
            start_group='#### (?P<command>.+) - (?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})',
            end_group='#### END',
            mail_to='jenselme@spam.fr',
            _out=output)

    with open(filtered_output_file, 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()
