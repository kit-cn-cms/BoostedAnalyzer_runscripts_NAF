#!/bin/bash

# samples without FatJets
#./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/mc/RunIISpring15DR74/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/*" /nfs/dust/cms/user/kelmorab/Spring15_Base20thJuly/ttbar MC_powheg_TTbar 2500 832.0 19899500 5 nominal
#./get-filenames.sh "/nfs/dust/cms/user/kelmorab/MINIAOD/RunIISpring15DR74/ttHTobb_M125_13TeV_powheg_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/" /nfs/dust/cms/user/kelmorab/Spring15_Base20thJuly/tthbb MC_powheg_tthbb 9125 0.2934 3933404 1 nominal



# samples WITH FatJets
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/shwillia/TT_TuneCUETP8M1_13TeV-powheg-pythia8/BoostedTTH_MiniAOD/150731_155453/0000/*" /nfs/dust/cms/user/kelmorab/Spring15_Base20thJuly/ttbar MC_powheg_TTbar 2500 832.0 19899500 5 nominal

./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/shwillia/ttHTobb_M125_13TeV_powheg_pythia8/BoostedTTH_MiniAOD/150727_223648/0000/" /nfs/dust/cms/user/kelmorab/Spring15_Base20thJuly/tthbb MC_powheg_tthbb 9125 0.2934 3933404 1 nominal

