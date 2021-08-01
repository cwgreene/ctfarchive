#!/bin/bash
mkdir -p challenges
for dir in $(ls -d */); do
    if [[ "$dir" != 'challenges/' ]] ; then
        mv $dir challenges
    fi
done
