#!/usr/bin/env bash

echo "This will remove all untracked files in this repo and extern repos."
echo "Are you sure you want to continue? [y/N] "
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    # Clean main repo
    git clean -fdx

    # Clean extern repos
    pushd extern/leptonica && git clean -fdx && popd || exit 1
    pushd extern/libpng && git clean -fdx && popd || exit 1
    pushd extern/tesseract && git clean -fdx && popd || exit 1
    pushd extern/zlib && git clean -fdx && popd || exit 1
else
    echo "Cleanup cancelled"
    exit 0
fi
