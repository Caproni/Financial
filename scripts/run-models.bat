wsl buildah bud --arch arm --os linux -f ../dockerfiles/Dockerfile.run-models -t docker.io/caproni60/financial:run-models-latest ..
wsl podman push docker.io/caproni60/financial:run-models-latest