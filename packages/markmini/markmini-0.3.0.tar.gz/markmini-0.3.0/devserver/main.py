from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import markmini

app = FastAPI()

app.mount("/static", StaticFiles(directory="devserver/static"), name="static")

templates = Jinja2Templates(directory="devserver/templates")

md = markmini.Markmini()

usernames = ["iverks", "testy"]
user_ids = ["1", "2"]
links = [f"/users/{id}" for id in user_ids]
fullnames = ["Iver Småge", "Testy McTestFace"]

md.add_users(usernames, user_ids, links, fullnames)


@app.get("/", response_class=HTMLResponse)
def rootpage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class Data(BaseModel):
    input: str


# Note: We only expose this function for testing
# In production we would only do this on submit
@app.post("/mdcompile")
def read_item(data: Data):
    return md.compile(data.input)
