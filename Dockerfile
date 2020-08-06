FROM python:3.8

WORKDIR /opt/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python","./manage.py", "runserver"]