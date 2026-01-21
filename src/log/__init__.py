import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s:%(lineno)d[%(levelname)s] %(message)s",
)


def setLevel(level):
    logging.getLogger().setLevel(level=level)
