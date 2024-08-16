wsl podman build -f ../update-stocks.Dockerfile -t docker.io/caproni60/financial:update-stocks-latest
wsl podman push docker.io/caproni60/financial:update-stocks-latest