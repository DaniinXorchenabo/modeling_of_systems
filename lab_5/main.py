import os
from os.path import dirname, join, split
import asyncio
import uvicorn
from decimal import Decimal
from typing import Any

from dotenv import load_dotenv
from wolframclient.evaluation import WolframCloudAsyncSession, SecuredAuthenticationKey
from fastapi import FastAPI
from wolframclient.serializers import export
from fastapi import FastAPI, Path, Query
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from wolframclient.language.expression import WLFunction, WLSymbol
from wolframclient.utils.packedarray import PackedArray
from wolframclient.exception import RequestException


session: WolframCloudAsyncSession | None = None
wolfram_code: str | None = None

app = FastAPI()


@app.on_event('startup')
async def create_connection_with_wolfram():
    global session
    last_environ = {key: val for key, val in os.environ.items()}
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    try:
        key = SecuredAuthenticationKey(
            os.environ['CONSUMER_KEY'],
            os.environ['CONSUMER_SECRET']
        )
    except KeyError as e:
        raise AttributeError('You should set a CONSUMER_KEY and CONSUMER_SECRET environ variables.\n'
                             'See a example.env file for more information.')
    session = WolframCloudAsyncSession(credentials=key)
    await session.start()
    session.authorized()


@app.on_event('startup')
async def get_wolfram_code_from_file():
    global wolfram_code
    with open('code.nb', 'r', encoding='utf-8') as f:
        wolfram_code = f.read()


@app.on_event('shutdown')
async def create_connection_with_wolfram():
    global session
    await session.stop()


@app.get('/calculate', response_model=list[list[Decimal]] | Any)
async def test(n: int = 10, a: Decimal = 0, b: Decimal = 100, eps='10^-8'):
    """ ln(x) - (1 /(x + 1))  = 0 => x > 0 """
    global wolfram_code
    with open('code.nb', 'r', encoding='utf-8') as f:
        wolfram_code = f.read()

    # How to update part in matrix see: https://reference.wolfram.com/language/howto/UpdatePartsOfAMatrix.html
    params = f'n = {n};' \
             f'a = {a};' \
             f'b = {b};' \
             f'eps = {eps};' \
             'xData = {3, 5, 7};' \
             'yData = {-3, -7, 1};'
    # print(params)
    try:
        data = session.evaluate(params + wolfram_code)
        # print(data)
        awaited_data: PackedArray = await data
    except RequestException as e:
        if e.response.response.status == 401:
            await create_connection_with_wolfram()
            data = session.evaluate(params + wolfram_code)
            awaited_data: PackedArray = await data
        else:
            raise e from e

    # print(type(awaited_data), type(awaited_data[0][0]), awaited_data)

    def normalized_result(awaited_data_):
        res_ = awaited_data_
        if isinstance(awaited_data_, (list, set, tuple, frozenset)):
            res_ = [normalized_result(i) for i in awaited_data_]
        if isinstance(awaited_data_, WLFunction):
            res_ = [normalized_result(j) for j in awaited_data_.args]
        if hasattr(awaited_data_, 'tolist'):
            res_ = [list(map(lambda i: str(round(i, 30)), i)) for i in awaited_data_]
        return res_

    res: WLSymbol = normalized_result(awaited_data)
    print(awaited_data, sep='\n')

    return {i[0]: i[1] for i in res}


@app.get('/')
async def root_f():
    return RedirectResponse('/public/index.html')


app.mount("/public", StaticFiles(directory=join(split(__file__)[0], 'public')), name="static")

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=9010, reload=True, reload_includes=['*.py', '*.nb'])
