#!/bin/bash
# USAGE: bash setup.sh -p port -u user -w password -h host -v vhost
# run this script to setup the Rabbitmq cli client

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -h|--host)
    AMQP_HOST="$2"
    shift # past argument
    ;;
    -v|--vhost)
    AMQP_VHOST="$2"
    shift # past argument
    ;;
    -p|--port)
    AMQP_PORT="$2"
    shift # past argument
    ;;
    -u|--user)
    AMQP_USER="$2"
    shift # past argument
    ;;
    -w|--password)
    AMQP_PASSWORD="$2"
    shift # past argument
    ;;
esac
shift # past argument or value
done

# configure the rabbitmq.profile
echo AMQP_HOST     = "${AMQP_HOST}"
echo AMQP_VHOST    = "${AMQP_VHOST}"
echo AMQP_PORT     = "${AMQP_PORT}"
echo AMQP_USER     = "${AMQP_USER}"
echo AMQP_PASSWORD = "${AMQP_PASSWORD}"

sed -e "s/\${amqp_host}/`echo ${AMQP_HOST}`/" -e "s/\${amqp_vhost}/`echo ${AMQP_VHOST}`/" \
    -e "s/\${amqp_port}/`echo ${AMQP_PORT}`/" -e "s/\${amqp_user}/`echo ${AMQP_USER}`/" \
    -e "s/\${amqp_password}/`echo ${AMQP_PASSWORD}`/" rabbitmq.profile.in | tee rabbitmq.profile 

#build rabbitmq-c
cd rabbitmq-c
mkdir -p build
cd build
cmake ..
cmake --build .
cd ../../

# build amqptools
export AMQPTOOLS_RABBITHOME=$PWD/rabbitmq-c
cd amqptools
make
cd ..
