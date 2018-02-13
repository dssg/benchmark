#!/bin/bash

set -e -u

PROJECT="benchmark"
PROJECT_HOME="$( cd "$( dirname "$0" )" && pwd )"
INFRASTRUCTURE_HOME="${PROJECT_HOME}/infrastructure"

cd $INFRASTRUCTURE_HOME

function help_menu () {
cat << EOF
Usage: ${0} {start|stop|build|rebuild|run|logs|status|destroy|all|}

OPTIONS:
   -h|help             Show this message
   start
   stop
   rebuild
   status
   destroy
   -t|triage
   -a|all

EXAMPLES:
   All the infrastructure needed is turned on!
        $ ./benchmark.sh start

   Check the status of the containers:
        $ ./benchmark.sh status

   Stop the benchmark's infrastructure:
        $ ./benchmark.sh stop

   Destroy all the resources related to the benchmark:
        $ ./benchmark.sh destroy

   Infrastructure logs:
        $ ./benchmark.sh -l

   Run one experiment:
        $ ./benchmark.sh -t --config_file sample_experiment_config.yaml run

   Validate experiment configuration file:
        $ ./benchmark.sh -t --config_file sample_experiment_config.yaml validate

   Show experiment's temporal cross-validation blocks:
        $ ./benchmark.sh -t --config_file sample_experiment_config.yaml show_temporal_blocks

   Triage help:
        $ ./benchmark.sh -t --help

EOF
}

function start_infrastructure () {
    docker-compose --project-name ${PROJECT} up -d police_db
}

function stop_infrastructure () {
	docker-compose  --project-name ${PROJECT} stop
}

function build_images () {
	docker-compose  --project-name ${PROJECT} build "${@}"
}

function destroy () {
	docker-compose  --project-name ${PROJECT} down --rmi all --remove-orphans --volumes
}

function infrastructure_logs () {
    docker-compose --project-name ${PROJECT} logs -f -t
}


function status () {
	docker-compose --project-name ${PROJECT} ps
}

function triage () {
	docker-compose  --project-name ${PROJECT} run --rm --name police_triage triage  "${@}"
}

function all () {
	build_images
	start_infrastructure
	status
}


if [[ $# -eq 0 ]] ; then
	help_menu
	exit 0
fi

case "$1" in
    start)
        start_infrastructure
		shift
        ;;
    stop)
        stop_infrastructure
		shift
        ;;
    build)
        build_images
		shift
        ;;
    rebuild)
        build_images --no-cache
		shift
        ;;
    -d|destroy)
        destroy
		shift
        ;;
    -l|logs)
        infrastructure_logs	
		shift
        ;;    
    status)
        status
		shift
        ;;
    -t|triage)
	triage ${@:2}
		shift
	;;
    -a|--all)
        all
                shift
        ;;
    -h|--help)
        help_menu
        shift
        ;;
   *)
       echo "${1} is not a valid flag, try running: ${0} --help"
	   shift
       ;;
esac
shift

cd - > /dev/null
