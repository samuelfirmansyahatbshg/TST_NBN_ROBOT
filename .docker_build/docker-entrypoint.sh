#!/bin/bash

# set timezone link
ln -snf /usr/share/zoneinfo/$(cat /etc/timezone) /etc/localtime

# start services for bluetooth
service dbus start || echo "desktop bus didn't start"
bluetoothd &

# Check if host user is there and set it in container
if [ -z "${HOST_USER}" ]; then
    echo "WARNING: We need HOST_USER to be set! Use docker default user."
fi

if [ -z "${HOST_UID}" ]; then
    echo "WARNING: We need HOST_UID be set! Use docker default user."
fi

if [ -z "${HOST_GID}" ]; then
    echo "WARNING: We need HOST_GID be set! Use docker default user."
fi

# get all parameters to run as command
CMD=$@

if [ -z "${HOST_USER}" -o -z "${HOST_UID}" -o -z "${HOST_GID}" ];
then
    # We have no user to be used, lets use the default
    /bin/bash -c "$CMD"
else
    # Let's create that user
    USER_UID=${HOST_UID:=$UID}
    USER_GID=${HOST_GID:=$GID}

    # create group
    groupadd -g ${USER_GID} ${HOST_USER}

    # create user with specified uid and gid
    useradd -u ${USER_UID} -g ${USER_GID} -m -s /bin/bash ${HOST_USER}

    # add user to groups
    usermod -a -G sudo ${HOST_USER}
    usermod -a -G users ${HOST_USER}
    usermod -a -G audio ${HOST_USER}

    DOCKER_SOCKET=/var/run/docker.sock
    DOCKER_GROUP=docker

    if [ -S ${DOCKER_SOCKET} ]; then
        DOCKER_GID=$(stat -c '%g' ${DOCKER_SOCKET})
        groupadd -for -g ${DOCKER_GID} ${DOCKER_GROUP}
        usermod -aG ${DOCKER_GROUP} ${HOST_USER}
        chown root:docker /var/run/docker.sock
    fi

    # set password for user
    echo "${HOST_USER}:docker" | chpasswd
    echo "INFO: Current user ${HOST_USER} has the password 'docker' inside the docker container (you might need it for sudo)"
    # venv activation
    echo "source /opt/.virtualenvs/mason/bin/activate" >> /home/"${HOST_USER}"/.bashrc
    echo "source /opt/.virtualenvs/mason/bin/activate" >> /root/.bashrc
    # switch to current user and run next command
    echo "Starting: $CMD as user ${HOST_USER}"
    sudo -E -H -u ${HOST_USER} /bin/bash -c "source /opt/.virtualenvs/mason/bin/activate; $CMD"
fi