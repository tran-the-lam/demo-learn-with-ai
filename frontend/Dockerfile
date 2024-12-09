# Use the official Node.js image from the Docker Hub
FROM node:23-alpine as build

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json (or yarn.lock) files into the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the application
RUN npm run build

# Install a lightweight web server to serve the static files
RUN npm install -g serve

# Expose the port that the app runs on
EXPOSE 8080

# Command to run the application
CMD ["serve", "-s", "public", "-l", "8080"]