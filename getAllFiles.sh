#!/bin/bash

# samples without FatJets
#./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/mc/RunIISpring15DR74/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/*" /nfs/dust/cms/user/kelmorab/Spring15_Base20thJuly/ttbar MC_powheg_TTbar 2500 832.0 19899500 5 nominal
#./get-filenames.sh "/nfs/dust/cms/user/kelmorab/MINIAOD/RunIISpring15DR74/ttHTobb_M125_13TeV_powheg_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/" /nfs/dust/cms/user/kelmorab/Spring15_Base20thJuly/tthbb MC_powheg_tthbb 9125 0.2934 3933404 1 nominal



# samples WITH FatJets
#./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/TT_TuneCUETP8M1_13TeV-powheg-pythia8/BoostedTTH_MiniAOD/*/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/ttbar MC_powheg_TTbar 2500 831.76 115091972 10 nominal

#./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/ttHTobb_M125_13TeV_powheg_pythia8/BoostedTTH_MiniAOD/150924_124753/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/tthbb MC_powheg_tthbb 9125 0.2934 3933404 1 nominal
#./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/ttHToNonbb_M125_13TeV_powheg_pythia8/BoostedTTH_MiniAOD/150922_132156/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/tthNonbb MC_powheg_tthNonbb 9125 0.2151 3800598 1 nominal

#rest of backgrounds
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/BoostedTTH_MiniAOD/150922_095835/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/SingleT STttop 2500 136.02 3299800 10 nominal
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/BoostedTTH_MiniAOD/150922_095901/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/SingleT STtantitop 2500 80.95 1695400 10 nominal
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/BoostedTTH_MiniAOD/150922_095938/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/SingleT STtWtop 2500 35.9 995600 5 nominal
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/BoostedTTH_MiniAOD/150922_100000/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/SingleT STtWantitop 2500 35.9 1000000 5 nominal
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/BoostedTTH_MiniAOD/150922_095524/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/SingleT STs 2500 10.32 613384 5 nominal

./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/BoostedTTH_MiniAOD/150922_082805/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/ttZ ttZtollnunu 2500 0.263 184990 5 nominal
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/BoostedTTH_MiniAOD/150922_082457/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/ttZ ttZtoQQ 2500 0.611 351398 5 nominal

./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/BoostedTTH_MiniAOD/150922_092727/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/ttW ttWtoQQ 2500 0.435 430330 5 nominal
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/BoostedTTH_MiniAOD/150922_092809/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/ttW ttWtoLNu 2500 0.21 129850 5 nominal

./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/BoostedTTH_MiniAOD/150922_110334/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/ZJets ZJetsM50 2500 6025.2 19310834 10 nominal
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/BoostedTTH_MiniAOD/150922_110355/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/ZJets ZJetsM10 2500 22635.09 22217467 10 nominal

./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/BoostedTTH_MiniAOD/150922_110306/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/WJets WJets 2500 61526.7 16518218 10 nominal

./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/WW_TuneCUETP8M1_13TeV-pythia8/BoostedTTH_MiniAOD/150922_120605/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/DiBoson WW 2500 118.7 994416 10 nominal
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/WZ_TuneCUETP8M1_13TeV-pythia8/BoostedTTH_MiniAOD/150922_120921/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/DiBoson WZ 2500 44.9 991232 10 nominal
./get-filenames.sh "/pnfs/desy.de/cms/tier2/store/user/kelmorab/ZZ_TuneCUETP8M1_13TeV-pythia8/BoostedTTH_MiniAOD/150922_120944/*" /nfs/dust/cms/user/kelmorab/ThesisSamples/DiBoson ZZ 2500 15.4 996168 10 nominal



