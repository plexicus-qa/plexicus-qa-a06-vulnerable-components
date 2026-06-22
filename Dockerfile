# VULNERABILITY: EOL base image with unpatched CVEs
FROM python:3.6-slim-buster
# Python 3.6 EOL December 2021, Debian Buster EOL June 2024

WORKDIR /app
COPY requirements.txt .

# Installing all vulnerable packages
RUN pip install --no-cache-dir -r requirements.txt

# VULNERABILITY: Running as root (no USER directive)
COPY . .
EXPOSE 5006

# VULNERABILITY: No health check, no read-only filesystem
CMD ["python", "app.py"]
