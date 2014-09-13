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
