import uvicorn
from nahat_server.core.app import app

main = app


if __name__ == "__main__":
    uvicorn.run("main:main", reload=True, port=8080)
