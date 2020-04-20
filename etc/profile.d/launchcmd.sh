#!/usr/bin/env sh

function __launch {
    # store current location
    export LCMD_START_LOCATION=`pwd`

    # build command line
    local cmd="launchcmd printlaunchcmd"
    if [ ! -z $1 ]; then
        cmd="$cmd -l $1"
        cd $1
    fi

    # run command line
    eval `$cmd`
}

function __land {
    cd $LCMD_START_LOCATION
    unset LCMD_START_LOCATION

    # build command line
    local cmd="launchcmd printlandcmd"

    # run command line
    eval `$cmd`
}


function launch {
    if [ "$(type -t land)" = 'function' ]; then
        land
    fi

    __launch "$@"

    function land () {
        __land
        unset -f land
    }

    export -f land
}

export -f launch
