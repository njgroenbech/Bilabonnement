FROM python:3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Perhaps expose a port here in the future
CMD [ "python", "app.py" ]
EXPOSE 5001
