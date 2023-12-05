FROM python:alpine3.18

# Update all the things
RUN apk update && apk upgrade --no-cache \
    && rm -rf /var/cache/apk/*

# Install the kubernetes module
RUN pip install kubernetes==28.1.0

# Copy the script to the container
COPY sync.py .

# Set the required variables by the script
ENV ALLOW_LIST_DOMAINS=
ENV ALLOW_LIST_MIDDLEWARE_NAME=ip-allow-list
ENV ALLOW_LIST_TRAEFIK_NAMESPACE=traefik-system

# add and enable nonroot user
RUN addgroup --system --gid 1000 vdbnonroot && \
    adduser --system --disabled-password --no-create-home \
    --uid 1000 --ingroup vdbnonroot vdbnonroot

USER vdbnonroot

# Run the script
CMD ["python", "sync.py"]
