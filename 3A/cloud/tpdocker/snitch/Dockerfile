FROM debian:latest
RUN apt update && apt upgrade
RUN apt-get -y install netcat-traditional
COPY snitcher.sh .
RUN chmod u+x snitcher.sh
cmd ["bash", "-c", "./snitcher.sh"]
EXPOSE 5000 6000
