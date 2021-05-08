#!/bin/bash

# Get the value of a variable set in the file `.env`
function get_env() {
    grep "^$1=" .env | sed "s/$1=//;s/\s*#.*//"
}

# Run a docker-compose command configured with the project and environment
function d-c() {
    project=$(basename $(pwd))
    docker-compose -p ${project} -f etc/compose-dev.yml "$@"
}

case "$1" in
    "django")
        d-c exec django ./manage.py ${@:2}
        ;;

    "fmt")
        d-c exec django black .
        ;;

    "logs")
        shift
        d-c logs -f "$@"
        ;;

    "run")
        d-c stop -t 0
        d-c build
        d-c up -d
        ;;
esac
