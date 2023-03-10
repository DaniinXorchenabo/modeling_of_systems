import os
# from datetime import time
from math import sin
from os.path import dirname, join, split
import asyncio
from time import time

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


session: WolframCloudAsyncSession | None = None
wolfram_code: str | None = None

app = FastAPI()

def eller_m(last_y, h, y):
    return last_y + h*y

def func(
        h,
        p=5 * 10 ** 4,
        a=1.1,
        m=2000,
        u=50,
        c_x=0.02,
        c_y=0.005,
        m1=0.05,
        m2=0.005,
        T=14,
        g=9.81,
):
    h = float(h)
    x_last = [1500, 1, 0, 0, 1]
    x_next = [0] * 5
    results = {float(0): x_last}
    for t in (i * h for i in range(round(T / h))):
        x_next = [0] * 5
        x_next[0] = eller_m(x_last[0], h, -g * sin(x_last[1]) + (p - a * c_x * x_last[0] ** 2) / (m - u * t))
        x_next[1] = eller_m(x_last[1], h,(-g + (p * sin(x_last[4] - x_last[1]) + a * c_y * x_last[0] ** 2) / (m - u * t)) / x_last[0])
        x_next[2] = eller_m(x_last[2], h,(m1 * a * (x_last[1] - x_last[4]) * x_last[0] ** 2 - m2 * a * x_last[0] ** 2 * x_last[2]) / (
                m - u * t))
        x_next[3] = eller_m(x_last[3], h,x_last[0] * sin(x_last[1]))
        x_next[4] = eller_m(x_last[4], h,x_last[2])
        results[t] = x_last
        x_last = x_next
    results[float(T)] = x_next
    return results


def get_delta(data, h, T):
    res = func(h / 2, T=T)
    return abs((res[T][3] - data[T][3]) / res[T][3]) * 100


@app.get('/calculate/task_1', response_model=list[list[Decimal]] | Any)
async def test(
        h: Decimal = Query(1),
        T: int = Query(14),
):
    d = time()
    results = dict()
    results["task1"] = {"graph": func(h, T=T)}
    print(time() - d)
    results["task1"]["delta"] = get_delta(results["task1"]["graph"], h, T)
    results["task1"]['target_variable'] = results["task1"]["graph"][T][3]

    return results


@app.get('/calculate/task_2', response_model=list[list[Decimal]] | Any)
async def test(
        h: Decimal = Query(1),
        T: int = Query(14),
):
    n = 5
    result_graph = {}
    for h in sorted(list(i + (10 / n) * ii * i for i in (1, 0.1, 0.01, 0.001) for ii in range(0, n))):
        res = func(h, T=T)
        delta = get_delta(res, h, T)
        result_graph[h] = [delta, T / h]
    results = dict()
    results["task2"] = {"graph": result_graph}
    return results


@app.get('/calculate/task_3', response_model=list[list[Decimal]] | Any)
async def test(
        h: Decimal = Query(1),
        T: int = Query(14),
):
    h = 10
    delta = float("inf")
    graph_data = dict()
    while delta > 1:
        h /= 2
        graph_data = func(h, T=T)
        delta = get_delta(graph_data, h, T)
    print(h)
    result = {"task3": {"graph": graph_data, "delta": delta, 'target_variable': graph_data[T][3]}}
    return result


@app.get('/')
async def root_f():
    return RedirectResponse('/public/index.html')


app.mount("/public", StaticFiles(directory=join(split(__file__)[0], 'public')), name="static")

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=10012, reload=True, reload_includes=['*.py', '*.nb'])
