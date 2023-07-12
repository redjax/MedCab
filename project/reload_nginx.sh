#!/bin/bash

CONTAINER_NAME="medcab_proxy"

echo "Reloading NGINX container [$CONTAINER_NAME]"

docker exec $CONTAINER_NAME nginx -s reload

exit $?
