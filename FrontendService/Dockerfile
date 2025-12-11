FROM python:3

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Streamlit default port is 8501 override to 5007
EXPOSE 5007


CMD ["streamlit", "run", "app.py", "--server.port=5007", "--server.address=0.0.0.0"]
