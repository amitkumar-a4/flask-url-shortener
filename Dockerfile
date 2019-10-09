FROM ubuntu:latest

RUN apt-get update -y && apt-get install \
  -y locales python3 python3-setuptools python3-pip python3-dev libffi6 libffi-dev
COPY . /my_app
WORKDIR /my_app
# fix UnicodeDecodeError: 'ascii'
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

RUN pip3 install -r requirements.txt
ENV FLASK_ENV=development
EXPOSE 5000

CMD flask run --host=0.0.0.0