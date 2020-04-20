#!/usr/bin/env sh

function __launch {
    echo "LAUNCHING ..."
    # build command line
    local cmd="launchcmd printlaunchcmd"
    if [ ! -z $1 ]; then
        cmd="$cmd -l $1"
    fi

    # run command line
    echo $cmd
    eval `$cmd`
}

function __land {
    echo "LANDING ..."
    # build command line
    local cmd="launchcmd printlandcmd"

    # run command line
    echo $cmd
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
