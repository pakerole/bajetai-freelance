# Build stage
FROM node:22-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Run stage
FROM node:22-alpine
WORKDIR /app

COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./

RUN addgroup -S appuser && adduser -S appuser -G appuser \
    && chown -R appuser:appuser /app

USER appuser

ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

CMD ["node", "build"]
