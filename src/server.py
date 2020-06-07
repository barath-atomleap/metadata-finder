from utils.logging import configure_logging
from fastapi import FastAPI, Path, HTTPException
from finders import finders
from utils.exceptions import NotFoundException
import uvicorn
import logging
import asyncio

configure_logging()

app = FastAPI()


@app.get('/finders', summary='List all finders')
def list_finders():
  finders_list = []
  for key, value in finders.items():
    finders_list.append(key)
  return finders_list


@app.get(('/all/{name}'), summary='Search all finders')
async def get_all(name: str = Path(None, title='Company name to search')):
  name = name.replace('+', ' ')
  all_finders = list_finders()
  results = {}

  async def get_one(finder: str):
    try:
      logging.info(f'looking in {finder} for {name}')
      result = await finders[finder](name)
      results[finder] = result
    except Exception as ex:
      logging.error(f'[{finder}] {str(ex)}')
      results[finder] = {'error': str(ex)}

  futures = [get_one(f) for f in all_finders]
  await asyncio.gather(*futures)
  return results


@app.get('/{finder}/{name}', summary='Search one finder')
async def get_data(finder: str = Path(None, title='Finder to use'),
                   name: str = Path(None, title='Company name to search')):
  name = name.replace('+', ' ')
  try:
    logging.info(f'looking in {finder} for {name}')
    return await finders[finder](name)
  except NotFoundException as ex:
    raise HTTPException(status_code=404, detail=ex.message)
  except Exception as ex:
    raise HTTPException(status_code=500, detail=str(ex))


if __name__ == '__main__':
  uvicorn.run(app, host="0.0.0.0", port=8000)
