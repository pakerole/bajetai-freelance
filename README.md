# bajetAI Freelance Landing Page

One-page freelance site for data science services at [bajetai.my](https://bajetai.my).

## Tech Stack
- **Frontend:** SvelteKit + Svelte 5 (TypeScript)
- **Backend:** Python + FastAPI (managed with Pixi)
- **Deployment:** Docker + Caddy (auto HTTPS)

## Running Locally

```bash
# Frontend
cd frontend && npm install && npm run dev

# Backend
cd backend && ~/.pixi/bin/pixi run dev
```

## Deployment

```bash
# Build and run containers
docker build -t bajetai-frontend ./frontend
docker build -t bajetai-backend ./backend

docker run -d --name bajetai-backend -p 8010:8010 \
  -v $(pwd)/backend/uploads:/app/uploads \
  -v $(pwd)/backend/data:/app/data \
  bajetai-backend

docker run -d --name bajetai-frontend -p 8030:3000 \
  -e ORIGIN=https://bajetai.my \
  bajetai-frontend
```

## License
MIT
