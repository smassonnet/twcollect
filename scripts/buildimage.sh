#!/usr/bin/env bash

TWCOLLECT_VERSION="$(python -m setuptools_scm)"
docker build -t "ghcr.io/smassonnet/twcollect:${TWCOLLECT_VERSION}" --build-arg "TWCOLLECT_VERSION=${TWCOLLECT_VERSION}" .
