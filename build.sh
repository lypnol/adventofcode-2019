#!/bin/bash

set -ev

git --no-pager diff --name-only origin/master -- | grep "day-" | cut -d "/" -f1 | cut -d "-" -f2 | sort | uniq | xargs -I{} ./aoc run -fd {}
