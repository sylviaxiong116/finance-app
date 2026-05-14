FROM python:3.10-slim as backend
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
ENV PYTHONUNBUFFERED=1

FROM nginx:alpine as frontend
COPY frontend/index.html /usr/share/nginx/html/index.html
COPY --from=backend /app/backend /usr/share/nginx/html/api
RUN echo 'server { listen 80; location / { root /usr/share/nginx/html; index index.html; try_files $uri $uri/ /index.html; } location /api/ { proxy_pass http://127.0.0.1:8000/api/; proxy_set_header Host $host; } }' > /etc/nginx/conf.d/default.conf
COPY --from=backend /app/backend /app
EXPOSE 80
CMD ["sh", "-c", "cd /app && pip install uvicorn && uvicorn main:app --host 127.0.0.1 --port 8000 & nginx -g 'daemon off;'"]
