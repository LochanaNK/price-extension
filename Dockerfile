# Base image
FROM python:3.12-slim

# Install system dependencies for Playwright / Chromium
RUN apt-get update && apt-get install -y \
    wget curl git \
    libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libdrm2 \
    fonts-liberation libappindicator3-1 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install ONLY Chromium (lightest + avoids Fly deploy timeout)
RUN python -m playwright install chromium

# Let Playwright know where browsers are stored
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Expose port for FastAPI
EXPOSE 8080

# Run backend
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8080"]
