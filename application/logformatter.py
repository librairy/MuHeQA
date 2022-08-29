import logging

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

class CustomFormatter(logging.Formatter):

	grey = "\x1b[38;20m"
	blue = "\x1b[33;94m"
	yellow = "\x1b[33;20m"
	red = "\x1b[31;20m"
	bold_red = "\x1b[31;1m"
	reset = "\x1b[0m"
	format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

	FORMATS = {
		logging.DEBUG: grey + format + reset,
		logging.INFO: blue + format + reset,
		logging.WARNING: yellow + format + reset,
		logging.ERROR: red + format + reset,
		logging.CRITICAL: bold_red + format + reset
	}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)