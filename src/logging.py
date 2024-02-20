import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('[%(asctime).19s] [%(levelname).3s] [%(name)s] %(message)s')
# %(thread)d : Thread ID (if available)
# %(threadName)s : Thread name (if available)
# formatter = logging.Formatter('[%(asctime).19s] [%(levelname).3s] [%(threadName)s] [%(name)s] %(message)s')
formatter = logging.Formatter('[%(asctime).19s] [%(levelname).3s] [%(threadName)s] %(message)s')

# handler = logging.FileHandler('../logs/app.log')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)




