#!/usr/bin/env bash

FORCE=0
VERSION=""
MINOR=0
HOTFIX=0

# Function to increment version
increment_version() {
    local version=$1
    local minor=$2
    local hotfix=$3

    IFS='.' read -r major minor_ver patch <<<"$version"

    if [ "$minor" -eq 1 ]; then
        minor_ver=$((minor_ver + 1))
        patch=0
    elif [ "$hotfix" -eq 1 ]; then
        patch=$((patch + 1))
    else
        echo "Either --minor or --hotfix must be specified when no version is provided"
        exit 1
    fi

    echo "${major}.${minor_ver}.${patch}"
}

# Function to get latest version from git tags
get_current_version() {
    git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0"
}

while test $# -gt 0; do
    case "$1" in
    -h | --help)
        SCRIPT_NAME=$(basename "$0")
        echo "$SCRIPT_NAME - create a release"
        echo " "
        echo "$SCRIPT_NAME [options] [version]"
        echo " "
        echo "options:"
        echo "-h, --help                show brief help"
        echo "-f, --force               force (skip git status check)"
        echo "--minor                   increment minor version"
        echo "--hotfix                  increment patch version"
        exit 0
        ;;
    -f | --force)
        shift
        FORCE=1
        ;;
    --minor)
        shift
        MINOR=1
        ;;
    --hotfix)
        shift
        HOTFIX=1
        ;;
    *)
        VERSION=$1
        shift
        ;;
    esac
done

if [ -z "$VERSION" ]; then
    current_version=$(get_current_version)
    if ! VERSION=$(increment_version "$current_version" "$MINOR" "$HOTFIX"); then
        echo "$VERSION"
        exit 1
    fi
fi

# check if git tag exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "tag $VERSION already exists"
    exit 1
fi

if [ "$FORCE" -eq 1 ]; then
    echo "force enabled, skipping git status check"
elif [ -z "$(git status --porcelain)" ]; then
    echo "git working directory clean, proceeding with release"
else
    echo "please clean git working directory first"
    exit 1
fi

git tag -a "$VERSION" -m "release $VERSION"

git push --atomic origin master "$VERSION"

gh release create "$VERSION" --latest --verify-tag --generate-notes
