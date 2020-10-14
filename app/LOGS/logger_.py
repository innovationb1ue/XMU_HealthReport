import logging



class NewLogger:
    def __init__(self, log_abs_path:str):
        self.logger = logging.getLogger()
        handler = logging.FileHandler(log_abs_path)
        handler.setLevel(logging.ERROR)
        self.logger.addHandler(handler)

    def log(self, msg:str):
        self.logger.log(logging.ERROR, msg)




