#!/bin/bash

. /etc/profile.d/modules.sh

module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw/slc6_amd64_gcc491
#. /usr/sge/default/common/settings.sh

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
export SCRAM_ARCH=slc6_amd64_gcc491
source $VO_CMS_SW_DIR/cmsset_default.sh

cd /afs/desy.de/user/k/kelmorab/CMSSW_7_4_6_patch6/src
eval `scram runtime -sh`
cd /afs/desy.de/user/k/kelmorab/runThesisBkg
# program to execute
./$INPUTSCRIPT cmsRun /afs/desy.de/user/k/kelmorab/CMSSW_7_4_6_patch6/src/BoostedTTH/BoostedAnalyzer/test/BaseLineSel_cfg.py

