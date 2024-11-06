#!/usr/bin/env sh

for dir in $(find . -name 'git-dir'); do
    mv "$dir" "${dir//git-dir/.git}"
done
