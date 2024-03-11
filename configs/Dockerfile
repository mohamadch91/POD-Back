
FROM nginx:alpine
# Copy the ngnix.conf to the container
# COPY etc/cert/goldiranasayesh.crt /etc/certs/goldiranasayesh.crt
# COPY etc/cert/goldiranasayesh.key /etc/nginx/certs/goldiranasayesh.key
COPY ngnix.conf /etc/nginx/conf.d/ngnix.conf
# Copy the React app build files to the container
# Expose port 80 for Nginx
EXPOSE 80
# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]

# Build the Docker image:
# docker build -t your-image-name .