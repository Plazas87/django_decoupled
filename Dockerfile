ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim AS python

ARG ENV
ARG POETRY_VERSION=1.5.0

ENV ENV=${ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=${POETRY_VERSION} \
  POETRY_HOME=/opt/poetry
# POETRY_VIRTUALENVS_CREATE=false \
# POETRY_VIRTUALENVS_IN_PROJECT=false \

ENV PATH="$POETRY_HOME/bin:$PATH"

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  bash \
  build-essential \
  curl \
  gettext \
  git \
  libpq-dev \
  wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*


FROM python as base_dir

RUN curl -sSL https://install.python-poetry.org | python -
RUN useradd -u 8877 django_decoupled

USER django_decoupled
WORKDIR /home/django_decoupled/app

COPY --chown=django_decoupled:django_decoupled . ./


FROM base_dir as poetry_prod

COPY --from=base_dir /home/django_decoupled/app /home/django_decoupled/app
RUN poetry install --no-interaction --no-ansi -vvv --without dev


FROM base_dir as poetry_dev

COPY --from=base_dir /home/django_decoupled/app /home/django_decoupled/app
RUN poetry install --no-interaction --no-ansi -vvv


FROM poetry_prod as django_decoupled_prod

EXPOSE 8000

ENTRYPOINT [ "/bin/sh" ]

CMD [ "./scripts/entrypoint.sh" ]


FROM poetry_dev as django_decoupled_dev

EXPOSE 8000

ENTRYPOINT [ "/bin/sh" ]

CMD [ "./scripts/entrypoint.sh" ]
