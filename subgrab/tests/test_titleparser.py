import re
import pytest


teststr = ["Doctor Strange 2016", "Doctor-Strange", "Doctor-Strange-2016"]

def title_parser(name):
	if re.search(r'\d{4}', name):
		name, year, removal = name.partition(re.search(r'\d{4}', name).group())
		return name.strip()
	else:
		return name


@pytest.mark.parametrize("name, answer", [
    (teststr[0], 'Doctor Strange'),
    (teststr[1], 'Doctor-Strange'),
    (teststr[2], 'Doctor-Strange'),
])

def test_answer(name, answer):
    assert title_parser(name) == answer



