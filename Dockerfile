FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir numpy scipy aiohttp
COPY . .
EXPOSE 8080
CMD ["python", "api_server.py"]
