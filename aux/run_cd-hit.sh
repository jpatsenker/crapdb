#!/bin/bash
. /etc/profile.d/modules.sh
module load gcc/6.2.0
module load cdhit/4.6.8
cd-hit "$@"
