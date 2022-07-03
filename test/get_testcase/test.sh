#!/bin/bash

HOST=$1
JOB_ID=$2

curl -X 'GET' 'http://${HOST}/job/${JOB_ID}' -H 'accept: application/json'
