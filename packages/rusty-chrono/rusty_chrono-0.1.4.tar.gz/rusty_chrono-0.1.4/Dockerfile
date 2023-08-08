FROM rust:slim-buster

RUN apt-get -y update && apt-get install -y sudo
RUN adduser --disabled-password --gecos '' admin
RUN adduser admin sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN chown -R admin /home/admin
USER admin

# Setting working directory
WORKDIR /home/admin

# pyenv commands
RUN sudo apt install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl \
    libncursesw5-dev xz-utils tk-dev libxml2-dev \
    libxmlsec1-dev libffi-dev liblzma-dev llvm git curl
RUN curl https://pyenv.run | bash

# ENV Setup
ENV HOME /home/admin
ENV PYENV_ROOT $HOME/.pyenv
ENV POETRY_ROOT $HOME/.poetry
ENV CARGO_ROOT /usr/local/cargo
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
ENV PATH $CARGO_ROOT/bin:$PATH


# Installing latest python using pyenv
RUN pyenv install 3.11 && \
    pyenv global 3.11

RUN pip install maturin