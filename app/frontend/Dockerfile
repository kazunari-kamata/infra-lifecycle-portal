FROM node:22-slim AS base

WORKDIR /workspace

COPY app/frontend/package.json app/frontend/package-lock.json* ./
RUN npm install

COPY app/frontend/ ./

FROM base AS buildcheck

RUN npm run build

FROM base AS dev

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
