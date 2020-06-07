import datetime


def clean_url(url: str) -> str:
  if url is not None:
    url = url.strip()
    url = url.replace('https://', '').replace('http://', '')
    url = url.replace('www.', '').rstrip('/')
    split_url = url.split('/')
    return split_url[0].lower()
  else:
    return None


def format_to_date(datestr: str, format: str = '+%Y-%m-%dT%H:%M:%SZ'):
  if datestr is not None:
    return datetime.datetime.strptime(datestr.replace('00', '01'), format)
  else:
    return None


def format_wp_number(num):
  return int(num['amount'].replace('+', ''))
