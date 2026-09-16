#!/bin/bash

syntax_error() {
    echo "push -v <version>"
    echo "  -v              set version for docker tag"
    echo "  -o              force override if version exists"
    echo "  -h --help       show this text"
    echo ""
    exit 1
}

# assign command line params over env vars
shift2="false"
while [ "$1" != "" ]
  do
    [ $1 == "-v" -a "${2:0:1}" != "-" ] && DOCKER_TAG_VERSION=$2 && shift2="true"
    [ $1 == "-v" -a "${2:0:1}" == "-" ] && syntax_error
    [ $1 == "-o" ] && IGNORE_DOCKER_TAG_CHECK="true"
    [ $1 == "-h" -o $1 == "--help" ] && syntax_error
    if [ "${1:0:1}" == "-" ]
    then
      shift
      if [ "$shift2" == "true" ]
      then
        shift
        shift2="false"
      fi
    else
      break
    fi
done

# set default name read from json
json_file="../docker_container_version.json"
if [ -f "$json_file" ]; then
  image_name=$(cat $json_file | python3 -c "import sys, json; print(json.load(sys.stdin)['image_name'])")

  if [ -z $image_name ]; then
    echo "ERROR: \"image_name\" isn't define in $json_file"
    exit 1
  elif [ $image_name == "artifactory-04.boschdevcloud.com/devops-ccm-docker-develop/bsh/dev-mason" ]; then
    echo "ERROR: it's not allowed to override \"/bsh/dev-mason\" define you image name in $json_file"
    exit 1
fi
else
  echo "ERROR: define you image name in $json_file"
  exit 1
fi
echo "Container name: $image_name"

# check if version env variable exists from jenkins or was set via cmd line params
if [ -z ${DOCKER_TAG_VERSION} ]; then
    echo "ERROR: Env variable DOCKER_TAG_VERSION is not set!"
    exit 1
else
    tst_project_ver=${DOCKER_TAG_VERSION}
    echo "INFO: Tag with version: $tst_project_ver"
fi

# push continer
docker push $image_name:latest

# verify docker tag
set +e
if [ "$IGNORE_DOCKER_TAG_CHECK" != "true" ]; then
    docker pull $image_name:${tst_project_ver}
    if [ $? -ne 0 ];  then
        echo "INFO: Tag unused"
    else
        echo "ERROR: Docker Tag already exists"
        exit 1
    fi
else
    echo "INFO: Ignore tag check"
fi

# tag and push
docker tag $image_name:latest $image_name:${tst_project_ver}
docker push $image_name:${tst_project_ver}

exit 0
