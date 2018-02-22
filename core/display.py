'''
A model for interfacing with the providers.
'''

class CLI:
	'''
	A base class that provides functionality for interacting with
	the providers, interactively.
	'''
	def __init__(self, provider, category):
		self.category = category
		self.provider = provider


	def welcome(self, provider):
		'''
		Welcome Message displayed at every start-up
		in command-line for providers.
		'''
		print("Welcome to the {} Command-Line Interface".format(provider))


	def quit(self, provider):
		'''
		An exit message displayed at exiting from the CLI.
		'''
		print("Exiting from the {} provider.".format(provider))


	def sub_menu(self, language, release_name, rating):
		'''
		A table that displays menu for the subtitles
		in Lang | Release Name | Rating order.

		Parameters:

		language: Language of the subtitle.
		release_name (lst): Name of the subtitle file.
		rating: Rating of the subtitle
		'''
		pass


	def sort_by(self, order="language", release_name):
		'''
		Allows to sort titles according to language, rating and helps
		displaying them accordingly.

		Parameters:
		release_name: Release names. (lst)
		order: Sort by language or rating.
		'''
		pass


	def clean(self):
		'''
		A filter method used for filtering out the subtitles with same name,
		media which is related to trailer, different release names but same
		files (specific for subscene site as it allows to preview subtitles)
		'''
		pass
