# Best-practice Dockerfile for Flask app
# 1. Use slim base image for smaller attack surface
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy only requirements first for layer caching
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 4. Copy rest of the code
COPY . ./

# 5. Create non-root user and switch to it
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# 6. Avoid secrets in image (use .env at runtime, not in image)
# 7. Expose port
EXPOSE 5000

# 8. Run app with gunicorn as non-root user
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers=3"]

# ---
# Comments:
# - Only requirements.txt is copied first for better build caching.
# - Non-root user (appuser) is used for security.
# - Secrets (API keys, .env) should be mounted at runtime, not baked into image.
# - Gunicorn is used for production WSGI serving.
