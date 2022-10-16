FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python3-pip &&\
    apt-get install -y python3 && \
    apt-get clean \

WORKDIR /plinic/
ADD . plinic
RUN pip3 install --upgrade pip
RUN pip3 install -r plinic/requirements/dev.txt

EXPOSE 8000
CMD ["python3", "plinic/backend/manage.py", "runserver", "0:8000"]
