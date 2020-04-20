#!/usr/bin/env sh

function __launch {
    # store current location
    export LCMD_START_LOCATION=`pwd`
    export LCMD_START_SHELL_PREFIX=$PS1

    # build command line
    local cmd="launchcmd printlaunchcmd"
    if [ ! -z $1 ]; then
        cmd="$cmd -l $1"

        # change directory to given location
        cd $1
    fi

    # run command line
    eval `$cmd`

    # set shell prefix
    local directory=`basename $PWD`
    export PS1="[$directory]$PS1"
}

function __land {
    # change directory back to start location
    cd $LCMD_START_LOCATION
    unset LCMD_START_LOCATION

    # reset shell prefix
    export PS1=$LCMD_START_SHELL_PREFIX
    unset LCMD_START_SHELL_PREFIX

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
