from omegaconf import OmegaConf
from memoization import cached
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os

load_dotenv()
dir = os.path.dirname(os.path.realpath(__file__))


def __get_secrets_client():
  delphai_environment = os.environ.get('DELPHAI_ENVIRONMENT')
  credential = DefaultAzureCredential()
  return SecretClient(f'https://delphai-kv-{delphai_environment}.vault.azure.net', credential)


def __get_secret(name: str):
  secrets_client = __get_secrets_client()
  return secrets_client.get_secret(name).value


OmegaConf.register_resolver('azkv', __get_secret)


def __load_config():
  if 'DELPHAI_ENVIRONMENT' not in os.environ:
    raise Exception('DELPHAI_ENVIRONMENT is not defined')
  config_path = f'{dir}/../../config'
  default_config = OmegaConf.load(f'{config_path}/default.yml')
  delphai_environment = os.environ.get('DELPHAI_ENVIRONMENT')
  if os.path.isfile(f'{config_path}/{delphai_environment}.yml'):
    delphai_env_config = OmegaConf.load(f'{config_path}/{delphai_environment}.yml')
  else:
    delphai_env_config = OmegaConf.create()
  config = OmegaConf.merge(default_config, delphai_env_config)
  OmegaConf.set_readonly(config, True)
  return config


@cached
def get_config(path: str = ''):
  config = __load_config()
  selected = OmegaConf.select(config, path)
  if OmegaConf.is_config(selected):
    return OmegaConf.to_container(selected, resolve=True)
  else:
    return selected
