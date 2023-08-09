import pytest
import yaml
import os
from k8sutils import Yaml

def test_nested_plain_values():
    with open('test.yaml', 'w') as file:
        yaml.dump({'a': {'b': {'c': 42, 'd': 'hello'}}}, file)

    obj = Yaml('test.yaml')
    obj.set('a.b.c', 99)
    obj.set('a.b.d', 'world')
    obj.save('another.yaml')

    with open('another.yaml', 'r') as file:
        data = yaml.safe_load(file)
        assert data['a']['b']['c'] == 99
        assert data['a']['b']['d'] == 'world'

    os.remove('test.yaml')
    os.remove('another.yaml')

def test_arrays_with_int_string():
    with open('test.yaml', 'w') as file:
        yaml.dump({'numbers': [1, 2, 3], 'words': ['a', 'b', 'c']}, file)

    obj = Yaml('test.yaml')
    obj.set('numbers[1]', 5)
    obj.set('words[2]', 'z')
    obj.save('another.yaml')

    with open('another.yaml', 'r') as file:
        data = yaml.safe_load(file)
        assert data['numbers'][1] == 5
        assert data['words'][2] == 'z'

    os.remove('test.yaml')
    os.remove('another.yaml')

