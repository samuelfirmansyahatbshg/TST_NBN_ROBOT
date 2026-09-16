#!/bin/bash

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

echo "Building Docker Image ${image_name}"

git_hash=$(git rev-parse --short HEAD)
echo "git hash ${git_hash}"

git_described=$(git describe --long --tags --dirty --always | sed 's/[\-\g]//')
echo "git described ${git_described}"

# /etc/apt/auth.conf file delivered by IT Linux team to this location, this will be used to access RB internal Artifactory mirror
echo -e "[global]\nextra-index-url = https://$ARTIFACTORY_USER:$ARTIFACTORY_ID_KEY@artifactory-04.boschdevcloud.com/artifactory/api/pypi/pypi-virtual/simple">> pip.ini
echo -e '[http-basic]\n[http-basic.pypi-virtual]\nusername = "'${ARTIFACTORY_USER}'"\npassword = "'${ARTIFACTORY_ID_KEY}'"'>> auth.toml
cp ../poetry.toml ./poetry.toml
cp ../poetry.lock ./poetry.lock
cp ../pyproject.toml ./pyproject.toml

docker build --pull \
             --no-cache \
             --secret id=auth_apt,src=/etc/apt/auth.conf \
             --secret id=pip_ini,src=pip.ini \
             --secret id=auth_toml,src=auth.toml \
             --label "git.hash=${git_hash}" \
             --label "git.described=${git_described}" \
             -t ${image_name} \
             --build-arg BUILD_USER=${USER} \
             --build-arg GID=$(id -g) \
             --build-arg UID=$(id -u) \
                          .
docker_result=$?

rm pip.ini
rm auth.toml
rm poetry.toml
rm poetry.lock
rm pyproject.toml

if [ $docker_result -eq 0 ]
then
  echo "Docker Build ${image_name} OK!"
else
	echo "ERROR Docker Build ${image_name} Failed!"
	exit 1
fi

docker tag ${image_name} ${image_name}:latest

echo "Label git.hash: " $(docker inspect ${image_name} --format "{{ index .Config.Labels \"git.hash\"}}")
echo "Label git.described: " $(docker inspect ${image_name} --format "{{ index .Config.Labels \"git.described\"}}")
