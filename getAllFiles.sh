#!/bin/bash

# nonbb file
#./get-filenames.sh /pnfs/desy.de/cms/tier2/store/user/hmildner/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/BoostedTTH_MiniAOD/150509_134128/0000/ /nfs/dust/cms/user/kelmorab/ttHNonbb_loose/tth MC_aMCatNLO_TTH 9125 0.5085 93694 1 nominal

#Spring15 files
#./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/mc/RunIISpring15DR74/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/*" /nfs/dust/cms/user/kelmorab/Spring15_Base20thJuly/ttbar MC_aMCatNLO_TTbar 2500 832.0 14170485 10 nominal

./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/mc/RunIISpring15DR74/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/*" /nfs/dust/cms/user/kelmorab/Spring15_Base20thJuly/ttbar MC_powheg_TTbar 2500 832.0 19899500 5 nominal

./get-filenames.sh "/nfs/dust/cms/user/kelmorab/MINIAOD/RunIISpring15DR74/ttHTobb_M125_13TeV_powheg_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/" /nfs/dust/cms/user/kelmorab/Spring15_Base20thJuly/tthbb MC_powheg_tthbb 9125 0.2934 3933404 1 nominal

