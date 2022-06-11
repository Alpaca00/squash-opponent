FROM jenkins/jenkins:latest
USER root
RUN apt-get update

RUN apt-get -y install python3-pip
RUN pip install --upgrade pip
RUN pip install pipenv

RUN apt-get update && apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list
RUN apt-get update
RUN apt-get install -y google-chrome-stable xvfb
ENV CHROME_BIN='/usr/bin/google-chrome-stable'
