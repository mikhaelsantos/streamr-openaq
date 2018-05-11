#!/usr/bin/env bash

export OWNER=mikhaelsantos
export IMAGE_NAME=streamr-openaq
export IMAGE_VERSION=${TRAVIS_BUILD_NUMBER}
export QNAME=${OWNER}/${IMAGE_NAME}
export BUILD_TAG=${QNAME}:${IMAGE_VERSION}
export LATEST_TAG=${QNAME}:latest
export GIT_TAG=${QNAME}:${TRAVIS_TAG}
docker build -t ${BUILD_TAG} .
