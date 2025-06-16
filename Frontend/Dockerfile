FROM python:3.12.11

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt 

COPY text_files /app/text_files

COPY my_helpers.py /app

COPY frontend.py /app

CMD [ "python", "-u","frontend.py" ]
