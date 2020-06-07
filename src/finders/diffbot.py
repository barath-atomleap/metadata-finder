import requests
from lib.model import Company, Headquarters
from utils.config import get_config
from utils.format_tools import clean_url, format_to_date
from utils.exceptions import NotFoundException
base_url = 'https://kg.diffbot.com/kg/dql_endpoint?type=query&size=3'
token = get_config('diffbot.token')


def __diffbot_find(name: str) -> Company:
  query = f'type%3AOrganization%20name%3A%22{name}%22%20'
  r = requests.get(f'{base_url}&token={token}&query={query}')

  if r.status_code == 200:
    response_json = r.json()
    company = Company()
    descriptions = []
    for result in response_json['data']:
      if 'allDescriptions' in result:
        descriptions.extend(result['allDescriptions'])
      if company.domain is None:
        company.domain = clean_url(result.get('homepageUri'))
      if company.name is None:
        company.name = result.get('allNames')[0]
      if company.full_name is None and len(result.get('allNames')) > 1:
        company.full_name = result.get('allNames')[1]
      if company.founded is None and 'foundingDate' in result:
        company.founded = format_to_date(result.get('foundingDate')['str'].replace('d', ''), format='%Y-%m-%d')
      if company.num_employees is None and 'nbEmployeesMax' in result:
        company.num_employees = result.get('nbEmployeesMax')
      if company.headquarters is None and 'location' in result:
        headquarters = Headquarters()
        if 'country' in result['location']:
          headquarters.country = result['location']['country']['name']
        if 'city' in result['location']:
          headquarters.city = result['location']['city']['name']
        if 'street' in result['location']:
          headquarters.address = result['location']['street']
        if 'postalCode' in result['location']:
          headquarters.zip_code = result['location']['postalCode']
        if 'latitude' in result['location']:
          headquarters.geo = (result['location']['latitude'], result['location']['longitude'])
        company.headquarters = headquarters
    company.short_description = min(descriptions, key=len)
    company.long_description = max(descriptions, key=len)
    return company
  else:
    raise NotFoundException(name)
