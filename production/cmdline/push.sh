#!/bin/bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 066517844483.dkr.ecr.us-east-1.amazonaws.com

docker build . -t 8mile-portland
docker tag 8mile-portland:latest 066517844483.dkr.ecr.us-east-1.amazonaws.com/8mile-portland:latest
docker push 066517844483.dkr.ecr.us-east-1.amazonaws.com/8mile-portland:latest

bash ./cmdline/clean_up_image.sh