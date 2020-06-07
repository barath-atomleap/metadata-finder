import requests
from utils.config import get_config
from utils.format_tools import clean_url
from lib.model import Company
from utils.exceptions import NotFoundException

base_url = 'https://kgsearch.googleapis.com/v1/entities:search'
api_key = get_config('google.api_key')


def __google_graph_find(name: str) -> Company:
  name = name.replace(' ', '+')
  r = requests.get(f'{base_url}?key={api_key}&query={name}&limit=1&indent=true')
  response_json = r.json()

  if r.status_code == 200 and 'itemListElement' in response_json:
    data = response_json['itemListElement'][0]['result']
    company = Company()
    if 'url' in data:
      company.domain = clean_url(data['url'])
    company.short_description = data.get('description')

    if 'detailedDescription' in data:
      company.long_description = data['detailedDescription'].get('articleBody')
    company.name = data.get('name')
    return company
  else:
    raise NotFoundException(name)
