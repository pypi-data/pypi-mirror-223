import uvicorn
from devserver.main import app as app

if __name__ == "__main__":
    uvicorn.run("devserver:main.app", host="0.0.0.0", port=8000, reload=True)
