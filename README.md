FASTAPI service for saving files 

$ sudo apt install -y python3-venv

$ python3 -m venv env

$ source env/bin/activate

(env)$ pip install -r requirements.txt

(env)$ uvicorn start main.app:app reload

go to http://127.0.0.1:8000/docs#/