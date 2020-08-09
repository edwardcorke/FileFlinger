import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# TODO: create different loggers for user and upload messages
file_handler = logging.FileHandler('log.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

log.addHandler(file_handler)
log.addHandler(stream_handler)


# logger.debug('Text: {} {} {}'.format(x, x, x))