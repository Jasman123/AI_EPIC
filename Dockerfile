# 1. Base image (Python installed)
FROM python:3.13-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy dependency file first (best practice)
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application
COPY . .

# 6. Expose Streamlit port
EXPOSE 8080

# 7. Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]