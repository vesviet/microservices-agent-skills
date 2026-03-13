#!/usr/bin/env bash
# Dev cluster SSH connection
# Usage: source .agent/config/environment.sh
# Skills reference $DEV_SSH instead of hardcoding SSH credentials.
# Customize these values for your environment.

export DEV_USER="${DEV_USER:-tuananh}"
export DEV_HOST="${DEV_HOST:-dev.tanhdev.com}"
export DEV_PORT="${DEV_PORT:-8785}"
export DEV_SSH="ssh ${DEV_USER}@${DEV_HOST} -p ${DEV_PORT}"
