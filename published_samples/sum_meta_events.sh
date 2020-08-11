grep "meta nevents" ZJetsToNuNu_HT-*/*.sh | cut -d':' -f3 | awk '{s+=$1} END {print s}'
