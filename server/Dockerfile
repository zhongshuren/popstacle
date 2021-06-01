FROM python:3.6
COPY ./app.py /
COPY ./gunicorn.conf.py /
COPY ./requirements.txt /
COPY ./static /static
COPY ./templates /templates
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]