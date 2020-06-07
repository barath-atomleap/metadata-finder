import requests
import datetime
from utils.config import get_config
from lib.model import Company, Headquarters
from utils.exceptions import NotFoundException

base_url = 'https://company.clearbit.com'
api_key = get_config('clearbit.api_key')


def __clearbit_find(name: str) -> Company:
  r_domain = requests.get(f'{base_url}/v1/domains/find?name={name}', auth=(api_key, ''))
  if r_domain.status_code == 200:
    domain = r_domain.json()['domain']
    r_company = requests.get(f'{base_url}/v2/companies/find?domain={domain}', auth=(api_key, ''))
    if r_company.status_code == 200:
      data = r_company.json()
      company = Company()
      company.domain = domain
      company.founded = datetime.datetime(data['foundedYear'], 1, 1)
      company.full_name = data['legalName']
      company.name = data['name']
      company.short_description = data['description']
      company.num_employees = data['metrics']['employees']
      headquarters = Headquarters()
      geo = data['geo']
      headquarters.address = f'{geo["streetNumber"]} {geo["streetName"]}'
      headquarters.country = geo['country']
      headquarters.city = geo['city']
      headquarters.zip_code = geo['postalCode']
      headquarters.geo = (geo['lat'], geo['lng'])
      company.headquarters = headquarters
      return company
    else:
      raise Exception(r_company.text)
  else:
    raise NotFoundException(name)
