ARG IMAGE=python
ARG TAG=3.12.4-slim-bullseye

FROM $IMAGE:$TAG

# create container user
ARG USER_NAME=bg_rank
ARG USER_ID=1200
USER root
RUN adduser --shell /bin/bash --uid ${USER_ID} --disabled-login ${USER_NAME}

# update apt-get and install basic apps
RUN apt-get update; \
    apt-get install --no-install-recommends -y wget git unzip openssh-client curl less
RUN pip install --upgrade pip

WORKDIR /tmp

# install python requirements
COPY deployment/local/requirements.txt ./pip/deployment/local/requirements.txt
COPY app/requirements.txt app/requirements-dev.txt ./pip/app/
RUN pip install -r ./pip/deployment/local/requirements.txt

# install aws cli
SHELL ["/bin/bash", "-cx"]
RUN wget -O awscliv2.zip "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
RUN unzip -q awscliv2.zip && ./aws/install

USER ${USER_NAME}

# set aws credentials as env vars
ARG AWS_CREDENTIALS_PATH="/tmp/credentials"
COPY ./.aws_credentials ${AWS_CREDENTIALS_PATH}
COPY ./tasks.py .
RUN invoke update-bashrc --config-path=${AWS_CREDENTIALS_PATH}/credentials; \
    invoke update-bashrc --config-path=${AWS_CREDENTIALS_PATH}/config

# install node.js
ENV NODE_VERSION 22.3.0
ENV NVM_DIR /home/${USER_NAME}/.nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
RUN . $NVM_DIR/nvm.sh && \
    nvm install ${NODE_VERSION} && \
    nvm use ${NODE_VERSION} && \
    nvm alias default ${NODE_VERSION}
ENV PATH $NVM_DIR/versions/node/v${NODE_VERSION}/bin:$PATH

# install aws cdk
RUN npm install -g aws-cdk

CMD ["sleep", "infinity"]