#!/usr/bin/env bash

TWCOLLECT_VERSION="$(python -m setuptools_scm)"
docker push "ghcr.io/smassonnet/twcollect:${TWCOLLECT_VERSION}"
