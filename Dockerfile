FROM python:3.11

ADD server.py logger.py ./

CMD ["python", "server.py"]