#!/usr/bin/env sh

function __launch () {
    # build command line
    local cmd=`launchcmd printlaunchcmd`
    if [ ! -z $1]
    then
        cmd="$cmd -l $1"
    fi
    echo $cmd

    # run command line
    eval $cmd
}

function __land () {
    # build command line
    local cmd=`launchcmd printlandcmd`
    echo $cmd

    # run command line
    eval $cmd
}


function launch () {
    __launch

    function land () {
        __land
        unset -f land
    }

    export -f land
}

export -f launch
