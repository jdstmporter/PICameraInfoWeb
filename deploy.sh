#!/bin/bash

# shellcheck disable=SC2164
cd "$HOME/developer"
tar czf dev.tgz src
scp dev.tgz rpi02w.local:.
ssh rpi02w.local "tar xf dev.tgz"





