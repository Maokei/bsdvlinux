#!/usr/bin/env bash

# Set test case
nrCont=$1

docker pull maokeibox/time:latest

#START=$(docker inspect --format='{{.State.StartedAt}}' test)
#STOP=$(docker inspect --format='{{.State.FinishedAt}}' test)

echo "Start time:" >> ./timeToRun"$nrCont".txt

date +%s.%N >> ./timeToRun"$nrCont".txt
echo "Docker times:" >> ./timeToRun"$nrCont".txt
# start Docker containers
for ((i = 1; i <= nrCont; i++))
do
    docker run -d --name timer$i maokeibox/time &
done
sleep 5
for ((i = 1; i <= nrCont; i++))
do

    docker logs timer$i >> ./timeToRun"$nrCont".txt
done
docker rm $(docker ps -a -q)
exit
