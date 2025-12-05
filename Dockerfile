# Base image
FROM python:3.12-slim

# Install system deps for Playwright / Chromium
RUN apt-get update && apt-get install -y \
    wget curl git \
    libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libdrm2 \
    fonts-liberation libappindicator3-1 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Install only Chromium to speed build
RUN python -m playwright install chromium

# Let Playwright know browsers path
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

EXPOSE 8080

# Use the actual module that defines app object
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8080"]
