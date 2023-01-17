FROM python:3.11

RUN python -m pip install pipenv
RUN pipenv install
