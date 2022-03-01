#!/bin/sh

BACKEND=backend
run() {
    pipenv run python main.py --logic FirstDiamond --email=$1 --name=$2 --password=$3 --team=$4 --host=$URL &
}

echo Waiting for server to start...
#while [ 1 ]; do
#    nc -z $BACKEND 5000
#    if [ $? -eq 0 ]; then
#        break
#    fi
#    sleep 1
#done
echo Starting

tokens=$(ls -la .token* | wc -l)
if [ $tokens != "0" ]; then
    # Existing tokens, use them
    echo Found $tokens existing tokens, use them
    for f in $(ls .token*); do
        token=$(cat $f)
        pipenv run python main.py --logic ClosestDiamond --token=$token &
        sleep 10
    done
else
    # Create new bots
    for bot in etimo1 etimo2; do
        pipenv run python main.py --logic RandomDiamond --email=erdem@alvalabs.io --name=bango --password=password123 --team bng &
        sleep 10
    done
    cp .token* /bot-data
fi

wait
sleep 5
