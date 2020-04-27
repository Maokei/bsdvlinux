#!/usr/bin/env bash

num=10

removeAllContainers () {
	echo "Removing all containers!"
	docker rm $(docker ps -a -q)
}

countExitedContainers () {
	return $(docker ps -a | grep "maokeibox/iobench" | grep "Exited" | wc -l)
}

countUpContainers () {
	return $(docker ps -a | grep "maokeibox/iobench" | grep "Up" | wc -l)
}

docker pull maokeibox/iobench:latest
for (( i=1; i <= num; i++ ))
do
  docker run -d --name iobench$i maokeibox/iobench &
done

#remove all containers
exited="0"
while [ $num -gt $exited ]; do
  #echo "exited $exited $num"
	sleep 2;
	countExitedContainers
	exited=$?
done
echo "All containers exited $exited"
mkdir -p ~/iobench_results
for (( i=1; i <= num; i++ ))
do
  docker logs iobench$i > ~/iobench_results/iobench$i.txt
done
removeAllContainers
