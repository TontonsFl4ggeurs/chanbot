#!/bin/bash

if [ $# -lt 1 ]
then
    msg="sauvegarde automatique"
    echo $msg
else
    msg="$@"
fi

git add .
if ! git commit --message="$msg"
then
    echo 'usage:' $0 '"message de commit"'
    exit 0
fi

git pull && git push

exit 0
