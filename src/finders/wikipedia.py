from utils.format_tools import clean_url, format_to_date, format_wp_number
import wptools
import logging
from lib.model import Company, Headquarters
import requests
from utils.exceptions import NotFoundException
sparql_base_url = 'https://query.wikidata.org/sparql'

silent = True
labels = {'domain': 'P856', 'founded': 'P571', 'full_name': 'P1448', 'num_employees': 'P1128'}
cleaners = {'domain': clean_url, 'founded': format_to_date, 'num_employees': format_wp_number}


def __get_headquarters(label: str) -> Headquarters:
  query = '''
  SELECT ?city ?country ?geo ?zip_code ?address ?address_deprecated WHERE {{
    ?company rdfs:label "{0}"@en.
    OPTIONAL{{ ?company wdt:P159/wdt:P1448 ?city }}.
    OPTIONAL{{ ?company wdt:P159/wdt:P17/rdfs:label ?country }}.
    OPTIONAL{{ ?company p:P159 [pq:P625 ?geo] }}.
    OPTIONAL{{ ?company p:P159 [pq:P281 ?zip_code] }}.
    OPTIONAL{{ ?company p:P159 [pq:P6375 ?address] }}.
    OPTIONAL{{ ?company p:P159 [pq:P969 ?address_deprecated] }}.
    FILTER(LANG(?country) = "en")
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
  }}
  LIMIT 1
  '''
  query = query.format(label)
  r = requests.get(sparql_base_url, params={'format': 'json', 'query': query})
  data_json = r.json()
  data = data_json['results']['bindings'][0]
  headquarters = Headquarters()
  for key, value in data.items():
    if key != 'address_deprecated':
      final_value = value['value']
      if (key == 'geo'):
        split = final_value.replace('Point(', '').replace(')', '').split(' ')
        final_value = (float(split[0]), float(split[1]))
      headquarters[key] = final_value
  if headquarters.address is None and 'address_deprecated' in data:
    headquarters.address = data['address_deprecated']['value']
  return headquarters


def __wikipedia_find(name: str) -> Company:
  name = name.replace('+', ' ')
  wp_page = wptools.page(name, silent=silent).get_parse()
  wp_page.get_restbase('/page/summary/')
  wikibase_id = wp_page.data['wikibase']
  page = wptools.page(wikibase=wikibase_id, silent=silent)
  page.wanted_labels(list(labels.values()))
  page.get_wikidata()
  claim = page.data['claims']
  try:
    company = Company()
    for field, label in labels.items():
      if label in claim:
        value = claim[label][0]
        company[field] = value
        if field in cleaners and value is not None:
          try:
            company[field] = cleaners[field](value)
          except Exception as ex:
            logging.warn(str(ex))

    company.short_description = page.data['description']
    company.long_description = wp_page.data['exrest']
    company.name = page.data['title'].replace('_', ' ')
    if company.full_name is None:
      company.full_name = company.name
    company.headquarters = __get_headquarters(company.name)
    return company
  except LookupError:
    raise NotFoundException(name)
