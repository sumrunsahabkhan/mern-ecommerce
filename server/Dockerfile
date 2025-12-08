# Use a lightweight Node.js base image
FROM node:24-alpine

# Set working directory
WORKDIR /app

# Copy dependency files first for better caching
COPY package*.json ./

# Install only production dependencies
RUN npm ci --omit=dev

# Copy the rest of the app code
COPY . .

# Set environment to production
ENV NODE_ENV=production

# Expose the app port
EXPOSE 5000

# Run the app
CMD ["node", "server.js"]