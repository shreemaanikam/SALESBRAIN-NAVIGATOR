# Frontend Dockerfile
FROM node:22-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy all source files
COPY . .

# Build the Next.js application
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
