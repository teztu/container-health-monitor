FROM ubuntu:latest
LABEL authors="nicow"

ENTRYPOINT ["top", "-b"]