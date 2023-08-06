import logging as l


class Logger:
    def __init__(self, name):
        self.logger = l.Logger(name)

        # stream handler
        stream_formatter = l.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        stream_handler = l.StreamHandler()
        stream_handler.setFormatter(stream_formatter)
        stream_handler.setLevel(l.INFO)
        self.logger.addHandler(stream_handler)

        # file handler
        file_handler = l.FileHandler("./log.log", mode="a", encoding="utf-8")
        file_formatter = l.Formatter("[%(asctime)s] %(levelname)s(%(name)s) %(message)s")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(l.INFO)
        self.logger.addHandler(file_handler)


logger = Logger("opaw").logger


def name(lv):
    return l._levelToName[lv]
