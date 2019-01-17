#!/bin/bash

usage() {
    echo "Usage: $0 [options]" 1>&2;
    echo " -g: Skip the history entry and git commits/tags." 1>&2;
    echo " -r [patch|minor|major]: The type of update (default patch)." 1>&2;
    echo " -p (python versions): A comma separated list of versions to test against (default ALL)." 1>&2
    exit 1;
}

skipGit=false
release="patch"
pythonVersions="ALL"

while getopts "gp:r:" o; do
    case "${o}" in
        g)
            skipGit=true
            ;;
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

echo $skipGit

lastVersion=`git tag | tail -1`
if $skipGit
then
    newVersion=$lastVersion
else
    # Compute the new version number.
    major=`echo $lastVersion | sed 's|v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)|\1|g'`
    minor=`echo $lastVersion | sed 's|v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)|\2|g'`
    patch=`echo $lastVersion | sed 's|v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)|\3|g'`
    if [[ "$release" == "major" ]]
    then
      major=$(($major + 1))
      minor=0
      patch=0
    fi
    if [[ "$release" == "minor" ]]
    then
      minor=$(($minor + 1))
      patch=0
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
fi

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
snapcraft clean mountain-tapir mountain-tapir-copy wrappers
snapcraft prime

export PYTHONPATH=./prime/usr/lib/python3.5/
./prime/usr/bin/python3 setup.py install

snapcraft snap

versionWithoutV=`echo $newVersion | sed "s|v||g"`
snapcraft push "mountain-tapir_"$versionWithoutV"_amd64.snap"
