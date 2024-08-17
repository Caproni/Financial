wsl buildah bud --arch arm --os linux -f ../dockerfiles/Dockerfile.base -t docker.io/caproni60/financial:base-latest ..
wsl podman push docker.io/caproni60/financial:base-latest