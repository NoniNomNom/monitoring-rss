# Use an official Python runtime as a parent image
FROM python:3.9

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]


