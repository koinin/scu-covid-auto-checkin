FROM python:3-alpine

ENV maintainer hugh
ENV version 1.0

WORKDIR /checkin/

COPY ./DockerRes/ .

RUN pip install -r requirements.txt --no-cache-dir

RUN echo "0	0	*	*	*	python /checkin/checkin.py" >> /var/spool/cron/crontabs/root

ENTRYPOINT [ "/bin/ash" ]