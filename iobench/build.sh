#!/usr/bin/env bash
mvn clean package
docker build -t maokeibox/iobench  .
# docker run -it --name iobench1 maokeibox/iobench
