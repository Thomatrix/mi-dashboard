FROM python:3.8
RUN curl -sSL https://install.python-poetry.org | python -
RUN $HOME/.local/bin/poetry config virtualenvs.create false
RUN pip install gunicorn
COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
WORKDIR /app
RUN $HOME/.local/bin/poetry install
COPY . /app
EXPOSE 5000
CMD ["gunicorn", "--bind",  "0.0.0.0:5000", "dashboard.app:server"]
