#!/bin/bash
# USAGE: bash test.sh -i instance_id
# Send a message to rabbitmq with the same format used for exchanging 
# messages between the wrapper and the CHIC platform

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -i|--instance)
    INSTANCE_ID="$2"
    shift # past argument
    ;;
esac
shift # past argument or value
done

TESTS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source ${TESTS_DIR}/../rabbitmq.profile 

echo WHOAMI `whoami`@`hostname`
echo TESTS_DIR ${TESTS_DIR}
echo PATH ${PATH}
echo LD_LIBRARY_PATH ${LD_LIBRARY_PATH}
echo AMQP_HOST ${AMQP_HOST}
echo AMQP_PORT ${AMQP_PORT}
echo AMQP_VHOST ${AMQP_VHOST}
echo AMQP_USER ${AMQP_USER}
echo AMQP_PASSWORD ${AMQP_PASSWORD}

INSTANCE_ID=${INSTANCE_ID:-instance_default_id}
echo INSTANCE_ID ${INSTANCE_ID}

WORKFLOW_UUID="123e4567-e89b-12d3-a456-4266554400000"
echo WORKFLOW_UUID ${WORKFLOW_UUID}

PAR_NUMBER_TEST="`cat ${TESTS_DIR}/number_test`"
echo PARAMETER_NUMBER_TEST ${PAR_NUMBER_TEST}

if [ -e ${TESTS_DIR}/number_output_test ]; then
    amqpsend --persistent vphhf workflow.`echo ${WORKFLOW_UUID}`.`echo ${INSTANCE_ID}`.snapshot "{\"hypomodel_uuid\" : \"123e4567-e89b-12d3-a456-426651440000\", \
\"status\":\"FINISHED_SUCCESSFULLY\", \"output_values\": {\"223e4567-e89b-12d3-a456-426655440000\" : \"/home/vphhf/test\", \
\"123e4561-e89b-12d3-a456-426655440000\" : \"`echo ${PAR_NUMBER_TEST}`\"}}"
else
  echo "error: some of the output files do not exist"
fi
