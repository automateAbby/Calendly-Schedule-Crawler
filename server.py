from distutils.log import debug
from fastapi import FastAPI, UploadFile, Request, Response
import uvicorn
from api import schedule as setSched
import os
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os

chrome_options = webdriver.ChromeOptions()
service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(service=service, options=chrome_options)

origins = [
   "*"
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=origins,  allow_headers=["*"])
]

app = FastAPI(middleware=middleware)

ALLOWED_ORIGINS = '*' 

class Schedule(BaseModel):
    email: str
    name: str
    url: str

# handle CORS preflight requests
@app.options('/*')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


@app.get('/main')
async def hello():
	return "HELLO"
    
@app.post('/schedule')
async def schedule(schedule_data: Schedule):
    email = schedule_data.email
    name = schedule_data.name
    url = schedule_data.url
    try:
        browser.get(url)
        browser.find_element(By.ID, "email_input").send_keys(email)
        browser.find_element(By.ID,"full_name_input").send_keys(name)
        submit_button = browser.find_element(By.CSS_SELECTOR,"button[type='submit']")
        submit_button.click()
    except:
        browser.quit()
    

if __name__ == "__main__":
	uvicorn.run(app, host='0.0.0.0', port=os.environ.get('PORT', '5000'))
