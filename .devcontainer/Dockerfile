
FROM python:3.9

# ----- Environment Setup -----

# Set Workspace directory
ARG WORKSPACE=/workspaces/ten-second-tools
ENV WORKSPACE=${WORKSPACE}

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# ----- Primary Installs -----

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1

# Install SQLite3
RUN apt-get install -y sqlite3 libsqlite3-dev 

# Install Poetry
RUN pip --disable-pip-version-check --no-cache-dir install poetry 

# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*


# ----- Dependency Installs -----

# Installing Modules
# COPY poetry.lock pyproject.toml ${WORKSPACE}/
# RUN cd $WORKSPACE && poetry install --no-root


# ----- Workspace Prep -----

WORKDIR ${WORKSPACE}

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
