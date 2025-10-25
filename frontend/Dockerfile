FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Set environment variable
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

# Run the application
CMD ["node", ".output/server/index.mjs"]
