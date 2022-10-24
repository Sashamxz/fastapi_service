import uvicorn
from app.main import get_app
from app.config import settings


app = get_app()

if __name__ == '__main__':
    uvicorn.run(app, host= settings.server_host, port= settings.server_port)