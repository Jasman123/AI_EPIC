# 1. Base image (Python installed)
FROM python:3.13-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy only requirements first (best practice)
COPY requirements.txt .

# 4. Install lightweight dependencies first to reduce temporary disk usage
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# 5. Copy the rest of the application
COPY . .

# 6. Expose Streamlit port
EXPOSE 8080

# 7. Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
