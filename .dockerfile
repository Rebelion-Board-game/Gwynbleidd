# Stage 1: Build Frontend
FROM node:18-alpine AS build-frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Final Backend Image
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Kopiujemy zbudowany frontend do folderu statycznego backendu
COPY --from=build-frontend /app/frontend/dist ./static
CMD ["python", "src/main.py"]