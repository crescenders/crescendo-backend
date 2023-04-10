FROM python:3.11-slim

COPY ./ app

WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]