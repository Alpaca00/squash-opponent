echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -t alpaca00/opponent .
docker push alpaca00/opponent:latest
