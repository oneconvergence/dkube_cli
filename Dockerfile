FROM python:3.8.2

RUN apt install -y git
RUN pip install git+https://github.com/oneconvergence/dkube.git@pipeline --upgrade

ADD . .

