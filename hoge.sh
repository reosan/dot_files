#!/bin/bash
abs_dirname() {
  local cwd="$(pwd)"
  local path="$1"

  while [ -n "$path" ]; do
      echo $(set -o | grep errexit)
      echo "${path%/*}"
      cd "${path%/*}"
      echo $?
    local name="${path##*/}"
    path="$(readlink "$name" || true)"
  done

  pwd -P
  cd "$cwd"
}

script_dir="$(abs_dirname "$0")"
abs_dirname $0
