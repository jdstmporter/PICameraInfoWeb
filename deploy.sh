#!/bin/bash

cd
tar czf dev.tgz developer
scp dev.tgz rpi02w.local:.
ssh rpi02w.local "rm -fr developer ; tar xf dev.tgz"





