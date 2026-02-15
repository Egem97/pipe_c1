#!/bin/bash

IMAGE_NAME="schedule-app-image_c1"
CONTAINER_NAME="schedule-app-container_c1"

echo "🚀 Iniciando despliegue de $CONTAINER_NAME..."

echo "🔨 Construyendo la imagen..."
docker build -t $IMAGE_NAME .


if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "🛑 Deteniendo y eliminando contenedor anterior..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi


echo "▶️ Iniciando nuevo contenedor..."

docker run -d \
    --name $CONTAINER_NAME \
    --restart always \
    -v "$(pwd):/app" \
    $IMAGE_NAME

echo "✅ Despliegue completado exitosamente!"
echo "📜 Logs del contenedor:"
docker logs --tail 10 $CONTAINER_NAME