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
