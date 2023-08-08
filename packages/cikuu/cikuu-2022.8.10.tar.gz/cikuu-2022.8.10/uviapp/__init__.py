# 2023.4.30 #from uviapp import *  #uvicorn index:app --port 80 --host 0.0.0.0 --reload
import json,os,uvicorn,time, fastapi,platform,requests,math,re, sys,traceback,random
from collections import Counter,defaultdict
from fastapi import FastAPI, File, UploadFile,Form, Body
from fastapi.responses import HTMLResponse, StreamingResponse, PlainTextResponse,  RedirectResponse
from functools import lru_cache

now			= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
mid			= lambda s, left, right=':':  s.split(left)[-1].split(right)[0]

tags_metadata = [ # https://fastapi.tiangolo.com/tutorial/metadata/
    {
        "name": "feishu",
        "description": "api from open.feishu.cn",
    },
    {
        "name": "redis",
        "description": "redis api",
    },
]

app = globals().get('app', fastapi.FastAPI(openapi_tags=tags_metadata)) #app=FastAPI(title= "Essay Dsk Data API",description= "data for ***",version= "0.1.0",openapi_url="/fastapi/data_manger.json",docs_url="/fastapi/docs",redoc_url="/fastapi/redoc")
from fastapi.middleware.cors import CORSMiddleware  #https://fastapi.tiangolo.com/zh/tutorial/cors/
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

setattr(uvicorn, 'title', 'uviapp api list')
@app.get('/')
def home(): 
	return HTMLResponse(content=f"<h2>{uvicorn.title}</h2>  <br> <a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>uvicorn index:app --port 80 --host 0.0.0.0 --reload <br> started: {now()}")

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=80)

'''
@app.get('/hello')
def hello(snt:str="I'm glad to meet you."): 
	return snt
from fastapi import FastAPI
from starlette.responses import JSONResponse 
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({"index":"HOme"}) 

async def about(request):
    return JSONResponse({"index":"about"}) 

routes = [
    Route("/", endpoint=homepage,methods=["GET"]),
    Route("/about", endpoint=about,methods=["POST"]),
]
app=FastAPI(routes=routes)
'''