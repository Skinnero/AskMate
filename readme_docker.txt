docker compose -f {path/to/file} up -d {"-d" runs container in background}
docker ps {lists docker-containers}
docker exec -it {"-it" opens command in terminal} {container-name} {comand to execute}
docker rm {container-name}
docker cp {path/to/file} {container-name}:/home/{file}
