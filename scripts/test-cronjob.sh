wsl podman build -f ../test-cronjob.Dockerfile -t docker.io/caproni60/financial:test-cronjob-latest
wsl podman push docker.io/caproni60/financial:test-cronjob-latest