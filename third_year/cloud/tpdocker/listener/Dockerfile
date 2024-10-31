FROM debian:latest
RUN apt update && apt upgrade
RUN apt-get -y install netcat-traditional
COPY listener.sh .
RUN chmod u+x listener.sh
cmd ["bash", "-c", "./listener.sh"] # listen on the port 5000 and writes a string if connection
EXPOSE 5000
