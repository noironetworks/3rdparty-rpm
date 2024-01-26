#!/bin/bash
# Should be run from the root of the source tree

if [ ! -d rpm ]; then
   echo "Directory 'rpm' not found"
   exit 1
fi
SPEC_FILE_IN=`ls rpm/*.spec.in`
if [ -z $SPEC_FILE_IN ]; then
   echo "RPM spec file not found"
   exit 1
fi
SPEC_FILE_IN=`ls rpm/*.spec.in`
if [ -z $SPEC_FILE_IN ]; then
   echo "RPM spec file not found"
   exit 1
fi

function buildPackage {
   PYTHON_BIN=$1
    BUILD_DIR=${BUILD_DIR:-`pwd`/rpmbuild}
    mkdir -p $BUILD_DIR/BUILD $BUILD_DIR/SOURCES $BUILD_DIR/SPECS $BUILD_DIR/RPMS $BUILD_DIR/SRPMS
    NAME=`${PYTHON_BIN} setup.py --name`
    RELEASE=${RELEASE:-1}
    VERSION_PY=`${PYTHON_BIN} setup.py --version`
    VERSION=`git describe --tags | tr -d v | cut -d'-' -f1`
    SPEC_FILE=${SPEC_FILE_IN/.in/}
    SPEC_FILE=${SPEC_FILE/rpm\//}
    sed -e "s/@VERSION@/$VERSION/" \
        -e "s/@VERSION_PY@/$VERSION_PY/" \
        -e "s/@RELEASE@/$RELEASE/" \
        $SPEC_FILE_IN > $BUILD_DIR/SPECS/$SPEC_FILE
    ${PYTHON_BIN} setup.py sdist --dist-dir $BUILD_DIR/SOURCES
    mv $BUILD_DIR/SOURCES/$NAME-$VERSION_PY.tar.gz $BUILD_DIR/SOURCES/$NAME-$VERSION.tar.gz
    rpmbuild --clean -ba --define "_topdir $BUILD_DIR" $BUILD_DIR/SPECS/$SPEC_FILE
}

# Save the python2 packages
function savePackages {
   cp rpmbuild/RPMS/noarch/*.rpm .
   cp rpmbuild/SRPMS/*.rpm .
   rm -rf rpmbuild
}

# Prepare build scripts for python3
function python3Packaging {
   cp rpm/acitoolkit.spec.in .

   sed -i "s/python2/python3/g" rpm/acitoolkit.spec.in
   sed -i "s/python-/python3-/g" rpm/acitoolkit.spec.in
   sed -i "s/Name:     %{srcname}/Name:     python3-%{srcname}/g" rpm/acitoolkit.spec.in
}

function restorePackages {
   # restore the python2 packages
   mv *.src.rpm rpmbuild/SRPMS/
   mv *.noarch.rpm rpmbuild/RPMS/noarch/

   # Restore the spec file
   mv acitoolkit.spec.in rpm/acitoolkit.spec.in
}

buildPackage python2
savePackages
python3Packaging
buildPackage python3
restorePackages
