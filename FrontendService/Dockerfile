FROM python:3

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Streamlit default port is 8501 – we’ll override to 5007
EXPOSE 5007

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=5007", "--server.address=0.0.0.0"]
