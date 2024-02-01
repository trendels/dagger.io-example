#!/bin/bash
set -eu -o pipefail

exec python3 -m http.server 8080
