#!/bin/bash

HOST=$1
file_path=$2

curl -X POST http://${HOST}/CamelCase/  -H 'accept: application/json' -H 'Content-Type: application/json' -d @${file_path} 
