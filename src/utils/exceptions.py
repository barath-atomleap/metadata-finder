import logging


class NotFoundException(Exception):
  def __init__(self, name):
    self.message = f'{name} not found'
    logging.error(self.message)
    super().__init__(self.message)
