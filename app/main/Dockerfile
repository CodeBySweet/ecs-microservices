FROM python:3.9-alpine3.21

WORKDIR /app

# Add dependencies for requests & Flask on Alpine
RUN apk add --no-cache build-base libffi-dev openssl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000
CMD ["python3", "main.py"]