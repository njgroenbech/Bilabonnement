FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Perhaps expose a port here in the future
CMD [ "python", "app.py" ]