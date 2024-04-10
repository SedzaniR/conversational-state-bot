FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt update
RUN apt upgrade -y
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
RUN python3 -m venv /env 
RUN /env/bin/pip install --upgrade pip 
RUN /env/bin/pip install --no-cache-dir -r /code/requirements.txt 

COPY . /code/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
