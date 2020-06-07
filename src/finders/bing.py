from utils.config import get_config
from azure.cognitiveservices.search.entitysearch import EntitySearchClient
from msrest.authentication import CognitiveServicesCredentials
from utils.format_tools import clean_url
from lib.model import Company
from utils.exceptions import NotFoundException

subscription_key = get_config('bing.subscription_key')
endpoint = get_config('bing.endpoint')
credentials = CognitiveServicesCredentials(subscription_key)
client = EntitySearchClient(endpoint=endpoint, credentials=credentials)


def __bing_find(name: str) -> Company:
  entity_data = client.entities.search(query=name)
  if entity_data.entities is not None:
    entity = entity_data.entities.value[0]
    company = Company({'name': entity.name, 'domain': clean_url(entity.url), 'long_description': entity.description})
    return company
  else:
    raise NotFoundException(name)
