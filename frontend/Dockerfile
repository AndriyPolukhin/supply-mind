# Stage 1: Ultra-light build stage (pure Alpine)
FROM alpine:latest AS builder

WORKDIR /app

# Install Node.js and npm only for building
RUN apk add --no-cache nodejs npm

COPY package.json package-lock.json ./
RUN npm ci --omit=optional

COPY . .
RUN npm run build

# Stage 2: Runtime (still Alpine with Node.js)
FROM node:18-alpine

WORKDIR /app

# Install production dependencies only
COPY --from=builder /app/package.json /app/package-lock.json ./
RUN npm ci --only=production --omit=optional


# Copy built assets from builder stage
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

# Create a non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S -u 1001 -G nodejs nodejs && \
    chown -R nodejs:nodejs /app


USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD node healthcheck.js || exit 1

# Start the application
CMD ["npm", "run", "dev"]

# Expose
EXPOSE 3000
