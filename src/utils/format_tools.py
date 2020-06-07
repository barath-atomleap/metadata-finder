import datetime


def clean_url(url: str) -> str:
  """
    Clean an url.
    :param url: String
    :return: clean url String
  """

  url = url.strip()
  url = url.replace('https://', '').replace('http://', '')
  url = url.replace('www.', '').rstrip('/')
  split_url = url.split('/')
  return split_url[0].lower()


def format_to_date(datestr: str):
  return datetime.datetime.strptime(datestr.replace('00', '01'), '+%Y-%m-%dT%H:%M:%SZ')


def format_wp_number(num):
  return int(num['amount'].replace('+', ''))
