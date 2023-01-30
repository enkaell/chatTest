FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]