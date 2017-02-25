#!/bin/bash

usage() {
    echo "Usage: $0 [options]" 1>&2;
    echo " -r [patch|minor|major]: The type of update (default patch)." 1>&2;
    echo " -p (python versions): A comma separated list of versions to test against (default ALL)." 1>&2
    exit 1;
}

release="patch"
pythonVersions="ALL"

while getopts "p:r:" o; do
    case "${o}" in
        p)
            pythonVersions=${OPTARG}
            ;;
        r)
            release=${OPTARG}
            if [[ "$release" != "major" && "$release" != "minor" && "$release" != "patch" ]]
            then
                echo "The release type must be patch, minor or major.";
                usage
            fi
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

# Compute the new version number.
lastVersion=`git tag | tail -1`
major=`echo $lastVersion | sed 's|v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)|\1|g'`
minor=`echo $lastVersion | sed 's|v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)|\2|g'`
patch=`echo $lastVersion | sed 's|v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)|\3|g'`
if [[ "$release" == "major" ]]
then
  major=$(($major + 1))
fi
if [[ "$release" == "minor" ]]
then
  minor=$(($minor + 1))
fi
if [[ "$release" == "patch" ]]
then
  patch=$(($patch + 1))
fi
newVersion="$major.$minor.$patch"

# Update HISTORY.rst
scite HISTORY.rst

# Commit the changes:
git add HISTORY.rst
git commit -m "Changelog for upcoming release $newVersion."

# Update version number
bumpversion "$release" || exit 1

# Install the package again for local development, but with the new version number:

sudo python setup.py develop

# Run the tests:

tox -e "$pythonVersions" || exit 1

# Release on PyPI by uploading both sdist and wheel:

python setup.py sdist upload
python setup.py bdist_wheel upload

#    Push:
git push origin HEAD:master
#    Push tags:
git push --tags

#    Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, copy and paste the RestructuredText into http://rst.ninjs.org/ to find out what broke the formatting.
#    Edit the release on GitHub (e.g. https://github.com/audreyr/cookiecutter/releases). Paste the release notes into the release's release page, and come up with a title for the release.

# Create the snap and upload it.
snapcraft clean mountain-tapir mountain-tapir-copy wrappers && snapcraft && snapcraft push "mountain-tapir_"$newVersion"_amd64.snap"