#!/bin/bash

# set defaults, try to read from json if exists
if [ -f docker_container_version.json ]; then
  image_name=$(cat docker_container_version.json | python3 -c "import sys, json; print(json.load(sys.stdin)['image_name'])")
  image_version=$(cat docker_container_version.json | python3 -c "import sys, json; print(json.load(sys.stdin)['image_version'])")
else
  image_name="artifactory-04.boschdevcloud.com/devops-ccm-docker-develop/bsh/dev-mason"
  image_version="latest"
fi

syntax_error() {
    echo "mason-docker-run -v <version> <command>"
    echo "  -v              set dev-mason image version"
    echo "  -i              set custom image name"
    echo "  -p              pull docker container"
    echo "  -x              specify a proxy for the container"
    echo "  -h --help       show this text"
    echo ""
    exit 1
}

# assign command line params
shift2="false"
while [ "$1" != "" ]
  do
    [ $1 == "-v" -a "${2:0:1}" != "-" ] && image_version=$2 && echo "Set dev-mason image version $2" && shift2="true"
    [ $1 == "-v" -a "${2:0:1}" == "-" ] && syntax_error
    [ $1 == "-i" -a "${2:0:1}" != "-" ] && image_name=$2 && echo "Set image name $2" && shift2="true"
    [ $1 == "-i" -a "${2:0:1}" == "-" ] && syntax_error
    [ $1 == "-x" -a "${2:0:1}" != "-" ] && arg_proxy=$2 && echo "Set Proxy $2 to container" && shift2="true"
    [ $1 == "-x" -a "${2:0:1}" == "-" ] && syntax_error
    [ $1 == "-p" ] && pull="true" && echo "Pull docker container"
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

###################################### Go Willi Go !!! ############################################
docker login https://artifactory-04.boschdevcloud.com/artifactory

# Check if we can run the inspect
if [ "$pull" != "true" ]
then
  docker inspect $image_name:$image_version > /dev/null
  rc=$?; if [ $rc -ne 0 ]; then pull="true"; fi
fi

# Force pull the container
if [ "$pull" == "true" ]
then
  docker pull $image_name:$image_version
  rc=$?; if [ $rc -ne 0 ]; then exit $rc; fi
fi

echo "Using the docker container $image_name:$image_version"

# check if we execute a command
if [ "$*" != "" ]
then
  terminal="-i"
  command=$*
  echo "Execute '${command}' in container"
  echo "Mount working dir ${PWD} from host"
else
  terminal="-it"
  command="/bin/bash"
  echo "Use interactive tty"
fi

# clear pyc files if exists
find . -name "*.pyc" -exec rm -f {} \;

# get the entrypoint of the image to use
docker_entrypoint=$(docker inspect $image_name:$image_version | python3 -c "import sys, json; print(str(json.load(sys.stdin)[0]['Config']['Entrypoint'])[1:-1])")

if [[ $docker_entrypoint == *"docker-entrypoint.sh"* ]]
then
  # we have a container with the entrypoint skript so we need to start it as root and let the the skript do the work
  docker run --privileged $terminal --hostname $HOSTNAME \
    -v /dev:/dev \
    -v /etc/timezone:/etc/timezone \
    --network host \
    -e HOST_UID=$(id -u) \
    -e HOST_GID=$(id -g) \
    -e HOST_USER=$USER \
    -e GIT_COMMIT=$GIT_COMMIT \
    -e BUILD_URL=$BUILD_URL \
    -e NODE_NAME=$NODE_NAME \
    -e GIT_BRANCH=$GIT_BRANCH \
    -e GIT_URL=$GIT_URL \
    -e JOB_NAME=$JOB_NAME \
    -v $PWD:/home/docker/work \
    -w /home/docker/work \
  $image_name:$image_version $command
else
  echo "ERROR: MASON don't support fixid as entrypoint, switch your custom container to use our docker-entrypoint.sh script!"
  exit 1
fi
