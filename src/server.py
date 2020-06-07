from utils.logging import configure_logging
from fastapi import FastAPI, Path, HTTPException
from finders import finders
from utils.exceptions import NotFoundException
import uvicorn
import logging
configure_logging()

app = FastAPI()


@app.get('/finders', summary='List all finders')
def list_finders():
  finders_list = []
  for key, value in finders.items():
    finders_list.append(key)
  return finders_list


@app.get('/{finder}/{name}', summary='Search Wikipedia')
async def get_data(finder: str = Path(None, title='Finder to use'),
                   name: str = Path(None, title='Company name to search for')):
  try:
    logging.info(f'looking in {finder} for {name}')
    return finders[finder](name)
  except NotFoundException as ex:
    raise HTTPException(status_code=404, detail=ex.message)


if __name__ == '__main__':
  uvicorn.run(app, host="0.0.0.0", port=8000)
