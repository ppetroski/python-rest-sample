#!/bin/sh
cd $(dirname $0)
cd ../../
cp "$PWD"/environment/docker.py "$PWD"/config.py

db_container_name="sample-db"
db_image_name="mariadb"
container_name="sample-app"
image_name="sample-app-docker"

echo 'Building docker image...'
docker build -t ${image_name} .

echo 'Creating database container...'
docker rm -f ${db_container_name}
docker run -d \
  -e MYSQL_ROOT_PASSWORD=dev \
  -p 3306:3306 \
  --name ${db_container_name} ${db_image_name}

echo "${db_container_name}  Container Started!"
echo 'Waiting 30 seconds for Database to become available...'
sleep 30 # TODO: arbitrary wait time ~10 worked for me. Should be changed to a loop with a connectivity check and timeout
docker exec -i ${db_container_name} mysql -u root -pdev < "$PWD"/environment/build/migrations/_init.sql

echo 'Creating App Container...'
docker rm -f ${container_name}
docker run -d \
  -v "$PWD":/usr/src/app:rw \
  -p 5000:5000 \
  --name ${container_name} ${image_name}

echo "${container_name}  Container Started!"

echo 'Running database migrations...'
docker exec -i ${db_container_name} mysql sample -u web_user -pdev < "$PWD"/environment/build/migrations/profile.sql
docker exec -i ${db_container_name} mysql sample -u web_user -pdev < "$PWD"/environment/build/migrations/interaction.sql
echo 'Environments are ready for use, http://localhost:5000/profile...'
