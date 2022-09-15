import coloredlogs, logging
import application.logformatter as lf

log_level = logging.DEBUG

fh = logging.StreamHandler()
fh.setFormatter(lf.CustomFormatter())
fh.setLevel(log_level)

logger = logging.getLogger('muheqa')
logger.addHandler(fh)
logger.setLevel(log_level)


logging.getLogger().setLevel(logging.DEBUG)

logger.debug("New Test ready")