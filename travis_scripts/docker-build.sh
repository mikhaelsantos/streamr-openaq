#!/usr/bin/env bash

export OWNER=mikhaelsantos
export IMAGE_NAME=streamr-openaq
export IMAGE_VERSION=${TRAVIS_BUILD_NUMBER}
export QNAME=${OWNER}/${IMAGE_NAME}
export BUILD_TAG=${QNAME}:${IMAGE_VERSION}
export LATEST_TAG=${QNAME}:latest
export GIT_TAG=${QNAME}:${TRAVIS_TAG}
docker build -t ${BUILD_TAG} .

docker tag ${BUILD_TAG} ${LATEST_TAG}
docker login -u "${DOCKER_USER}" -p "${DOCKER_PASS}"
if [ "$TRAVIS_TAG" != "" ]; then
docker tag ${BUILD_TAG} ${GIT_TAG}
docker push ${GIT_TAG}
fi
docker push ${LATEST_TAG}
