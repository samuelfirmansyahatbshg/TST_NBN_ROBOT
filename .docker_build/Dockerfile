# Inherit from mason base environment container, TODO generally use the latest version, if no special reasons
FROM artifactory-04.boschdevcloud.com/devops-ccm-docker-develop/bsh/mason-env-2204:1.9.3

# TODO add yourself as maintainer
LABEL maintainer="You<you@bshg.com>"

USER root

ARG BUILD_USER
ARG UID
ARG GID

# Set Env Variable for jfrog tool
ENV CI=true

# Configure pipx PATH early (prevents some stdout spam)
ENV PATH="/root/.local/bin:${PATH}"

# Install additional linux tools. Winflash is added, if you need you can also insert your needed stuff.
# TODO add you needed apt packages here
RUN --mount=type=secret,id=auth_apt,required,dst=/etc/apt/auth.conf \
    apt-get update \
    && apt-get install -y -f \
    winflash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Install poetry
RUN --mount=type=secret,id=pip_ini,required,dst=/root/.config/pip/pip.conf \
    pipx install poetry~=1.7.1

# Copy the poetry files into the container
COPY poetry.toml poetry.toml
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

# Create and activate venv
RUN python3 -m venv "/opt/.virtualenvs/mason"
ENV PATH="/opt/.virtualenvs/mason/bin:${PATH}"
ENV VIRTUAL_ENV="/opt/.virtualenvs/mason"

# Update pip of venv
RUN --mount=type=secret,id=pip_ini,required,dst=/root/.config/pip/pip.conf \
    /opt/.virtualenvs/mason/bin/python3 -m pip install --upgrade pip

# Check lockfile etc OK
RUN poetry check --no-ansi
RUN poetry check --lock --no-ansi
# Install the dependencies from the lockfile into the docker container
RUN poetry config virtualenvs.create false --local --no-ansi
RUN poetry config virtualenvs.in-project false --local --no-ansi
RUN poetry config repositories

# Install tools for TestCase lint check
RUN --mount=type=secret,id=auth_toml,required,dst=/root/.config/pypoetry/auth.toml poetry install --sync --no-ansi \
    &&rm -rf $(poetry config cache-dir)

# Update venv activation script to include LD_LIBRARY_PATH setting (for any compiled libs)
RUN echo LD_LIBRARY_PATH=/usr/bin/winflash/lib/:/opt/.virtualenvs/mason/lib/python3.11/site-packages/HCPServiceTestAPI/ >> /opt/.virtualenvs/mason/bin/activate
RUN echo export LD_LIBRARY_PATH >> /opt/.virtualenvs/mason/bin/activate

# Update to poetry specific entrypoint skript
COPY docker-entrypoint.sh /docker-entrypoint.sh

# User management
RUN groupadd --gid $GID $BUILD_USER \
    && useradd --uid $UID --gid $GID --groups sudo,users,audio --create-home --shell /bin/bash --password '' $BUILD_USER

# Set env for desktop bus support
ENV DISPLAY=:0
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

USER root
CMD ["/bin/bash"]
