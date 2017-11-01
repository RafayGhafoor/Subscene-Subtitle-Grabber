import re
import unittest

input_names = ['Doctor.Strange.2016.HEVC.1080p.mp4',
'The Intern  2015 Bluray.mp4',
'Spider-Man.Homecoming.2017.1080p.AMZN.WEB-DL.DD.5.1.H.264-SiGMA.avi'
]

expected_names = ['Doctor Strange 2016',
'The Intern 2015',
'Spider Man Homecoming 2017'
]

def title_parser(name):
	year_regex = re.compile(r'(?!1080|2160)p?\d{4}', 'abc 2016')
	removals = set(re.findall('\W+', name))
	for chars in removals:
		name = name.replace(chars, ' ')
	return name

class TitleParserTest(unittest.TestCase):
	def test_titles(self):
		pass
