# Multi-Container Web Architecture

Цей проєкт демонструє мікросервісну архітектуру з використанням Docker Compose.

## Компоненти системи

1. **Frontend**: Nginx сервер, що надає UI на порту `8080`.
2. **API Gateway**: Nginx шлюз на порту `80`, що перенаправляє запити `/api/*` на Backend.
3. **Backend**: Python (Flask) сервіс, що обробляє REST API запити (`/info`, `/users`).
4. **Database**: PostgreSQL 15 з persistent volume.

## Як запустити проєкт у VS Code

1. Переконайтеся, що Docker Desktop запущено.
2. Відкрийте термінал у VS Code (`Ctrl + ~`) та виконайте:

```bash
docker-compose up --build -d
```
