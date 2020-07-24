#!/bin/sh

set -eu

type aws > /dev/null 2>&1 && type jq > /dev/null 2>&1 || {
  echo 'Required aws-cli and jq'
  exit 1
}

repositories=$(aws ecr describe-repositories --query 'repositories[*].repositoryName' | tr -d "[\",\t\n\r\"]")

for repository in $repositories; do
  echo "$repository: Deleting untagged images"

  nextToken="initialized"

  while [ "$nextToken" != "null" ]; do
    if [ "$nextToken" == "initialized" ]; then
      response=$(aws ecr list-images --repository-name $repository --filter tagStatus=UNTAGGED --max-items 100)
    else
      response=$(aws ecr list-images --repository-name $repository --filter tagStatus=UNTAGGED --max-items 100 --starting-token $nextToken)
    fi

    nextToken=$(echo $response | jq -r '.NextToken')
    untaggedImages=$(echo $response | jq -c '.imageIds')

    if [ "$untaggedImages" == "[]" ]; then
      echo "$repository: Untagged image not found"
      break
    fi

    aws ecr batch-delete-image --repository-name $repository --image-ids $untaggedImages
  done

  echo "$repository: Deleted untagged images"
done