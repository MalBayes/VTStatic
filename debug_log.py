import logging

formatter = logging.Formatter('%(asctime)s %(funcName)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                              '%m-%d %H:%M:%S')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

gui_logger = logging.getLogger("gui_logger")
gui_logger.setLevel(logging.DEBUG)
gui_logger.addHandler(console_handler)

comm_logger = logging.getLogger("comm_logger")
comm_logger.setLevel(logging.DEBUG)
comm_logger.addHandler(console_handler)

mdm_logger = logging.getLogger("comm_logger")
mdm_logger.setLevel(logging.DEBUG)
mdm_logger.addHandler(console_handler)
