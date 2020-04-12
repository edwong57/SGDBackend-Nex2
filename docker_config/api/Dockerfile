FROM python:3.5
#RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV APP /app
ENV NODE_VERSION 10.16.0
ENV NVM_DIR /root/.nvm
SHELL ["/bin/bash", "-c"]
RUN apt-get update &&  apt-get install -y \
build-essential \
gcc \
curl \
make \
apt-utils

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

RUN apt-get update &&  apt-get install -y \
python-dev \
vim \
nodejs

RUN python get-pip.py pip==19.3.1
RUN mkdir $APP $NVM_DIR

# Install nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \

    && nvm use default \
    && nvm --version 

ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN source ~/.bashrc
RUN npm --version

WORKDIR $APP

EXPOSE 6543 6545 80 443 22 

COPY . .


# CMD [ "make", "build-app"]
CMD ["/bin/bash"]