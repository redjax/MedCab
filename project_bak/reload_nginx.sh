#!/bin/bash

docker compose exec proxy nginx -s reload

exit $?
