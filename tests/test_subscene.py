import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import subgrab.providers.subscene as subscene

subscene.MODE = "silent"


@pytest.mark.parametrize("name, expected", [
    ("Doctor Strange", 'https://subscene.com/subtitles/doctor-strange-2016/English'),
    ("The Intern", 'https://subscene.com/subtitles/the-intern-2015/English')
])
def test_sel_title(name, expected):
    assert subscene.sel_title(name) == expected


@pytest.mark.parametrize("url, expected", [
    ("https://subscene.com/subtitles/release?q=pele.birth.of.the.legend", ['https://subscene.com/subtitles/pel-birth-of-a-legend/english/1336174']),
])
def test_sel_sub(url, expected):
    assert subscene.sel_sub(url) == expected
