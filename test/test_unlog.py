from sh import python3
from io import StringIO

path2main = 'unlog/main.py'

def test_basic_filter():
    program_output = 'test/program_output'
    program_output_filtered = 'test/program_output_filtered'
    
    output = StringIO()
    python3(path2main, program_output, _out=output)
    
    with open(program_output_filtered, 'r') as correctly_filtered_output:
        assert correctly_filtered_output.read() == output.getvalue()
