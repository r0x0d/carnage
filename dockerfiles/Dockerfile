FROM python:3.13-slim as base

# Skip all interaction with apt
ENV DEBIAN_FRONTEND="noninteractive" \
    # Update $PATH preferences
    PATH="/home/carnage/.local/bin:/opt/venv/bin:/root/.local/bin:$PATH" \
    # Set language preferences to C.UTF-8
    LANGUAGE="C.UTF-8" \
    LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    LC_CTYPE="C.UTF-8" \
    LC_MESSAGES="C.UTF-8"

SHELL ["/bin/bash", "-o", "pipefail", "-o", "errexit", "-o", "nounset", "-o", "nolog", "-c"]

# Create the user
RUN groupadd --gid 1000 carnage \
    && useradd --uid 1000 --gid 1000 -m carnage

FROM base as build

WORKDIR /build
COPY ["pyproject.toml", "README.md", "LICENSE", "/build/"]
ADD carnage /build/carnage

RUN python -m venv --copies /opt/venv
RUN . /opt/venv/bin/activate && pip install --no-cache-dir --upgrade pip build && \
    . /opt/venv/bin/activate && python -m build

FROM base as runner

COPY --chown=carnage:carnage --from=build /build/dist /tmp

USER carnage

RUN pip install --user --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*

EXPOSE 5050

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ \
     "python3", \
     "-c", \
     "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5050/api/v1/health_check')" \
    ]

CMD [ "carnage", "serve" ]
