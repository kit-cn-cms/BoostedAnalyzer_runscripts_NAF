#!/usr/bin/env python

import das_client
import os
import subprocess

def get_datasets(dataset_wildcard):
    tmp = os.popen("python das_client.py --limit=20 --query="+dataset_wildcard).read()
    #print tmp.rstrip().split('\n')[3:]
    return tmp.rstrip().split('\n')[3:]

def get_datafiles(dataset):
    print 'getting files and counting events for',dataset
    data=das_client.get_data("https://cmsweb.cern.ch","file dataset="+dataset+" instance="+"prod/global",0,0,0)
    nevents=0
    for d in data['data']:
        #print d
        for f in d['file']:
            if not 'nevents' in f: continue
            #print store_prefix+f['name']
            nevents+=f['nevents']
	    
    return nevents


samples = {'category': {'ttbar': {'name' : 'ttbar' , 'dataset_wildcard': '/TT_TuneCUETP8M1_13TeV*powheg-pythia8*/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' ,        					  'XS': 831.76, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'POWHEG'},
			'ttHbb': {'name' : 'ttHbb' , 'dataset_wildcard': '/ttHTobb_M125_13TeV*powheg_pythia8*/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' , 
                                  'XS': 0.2934, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'POWHEG'},
                        'ttHnonbb' : {'name' : 'ttHnonbb' , 'dataset_wildcard': '/ttHToNonbb_M125_13TeV*powheg_pythia8*/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' , 
                                  'XS': 0.2151, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'POWHEG'},
                        'ZZ' : {'name' : 'ZZ' , 'dataset_wildcard':  '/ZZ_TuneCUETP8M1_13TeV*pythia8/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM',
                                  'XS': 16.523, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'pythia8'},
                        'WZ' : {'name' : 'WZ' , 'dataset_wildcard':  '/WZ_TuneCUETP8M1_13TeV*pythia8/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM',
                                  'XS': 47.13, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'pythia8'},
                        'WW' : {'name' : 'WW' , 'dataset_wildcard':  '/WW_TuneCUETP8M1_13TeV*pythia8/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM',
                                  'XS': 118.7, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'pythia8'},
                        'st_tchan': {'name' : 'st_chan' , 'dataset_wildcard': '/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' ,'XS': 45.3, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'POWHEG'},
                        'stbar_tchan': {'name' : 'stbar_chan' , 'dataset_wildcard': '/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' ,'XS': 27.0, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'POWHEG'},
                        'st_tWchan': {'name' : 'st_tWchan' , 'dataset_wildcard': '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM', 'XS': 35.6, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'POWHEG'},
                        'stbar_tWchan': {'name' : 'st_tbarWchan' , 'dataset_wildcard': '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM', 'XS': 35.6, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '?' , 'generator' : 'POWHEG'},
                        'DYJetsToLL': {'name' : 'DYJetsToLL' , 'dataset_wildcard': '/DYJetsToLL*TuneCUETP8M1_13TeV*pythia8/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM',                     'XS': 0, 'NposmNnegoNtot' : 0, 'boosted_dataset' : '?' , 'generator' : 'aMC'},
                        'WJets': {'name' : 'WJets' , 'dataset_wildcard': '/WJetsToLNu*TuneCUETP8M1_13TeV*pythia8/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' ,        					 'XS': 0, 'NposmNnegoNtot' : 0, 'boosted_dataset' : '?' , 'generator' : 'notSpecified'}}}#,
                        #'QCD':   {'name' : 'QCD' , 'dataset_wildcard': '/QCD_HT*TuneCUETP8M1_13TeV*pythia8/RunIISpring15MiniAOD*76X_mcRun2_asymptotic_v12*/MINIAODSIM' ,        	                         'XS': 0, 'NposmNnegoNtot' : 0, 'boosted_dataset' : '?'}}}




globalTag='76X_mcRun2_asymptotic_v12'
#categorys=samples['category']
#print categorys
#category=categorys['ttbar']
#print category
fobj_out = open("mc_samples.csv","w")
for c in samples['category']:
    categorys=samples['category']
    category=categorys[c]
    dataset=get_datasets(category['dataset_wildcard'])
    XS=category['XS'] #in pb
    NposmNnegoNtot=category['NposmNnegoNtot']
    boosted_dataset=category['boosted_dataset']
    generator=category['generator']
    for s in dataset:
        nevents=get_datafiles(s)
        if(NposmNnegoNtot==0):
             weights=XS/(nevents*1)*1000
        else:
             weights=XS/(nevents*NposmNnegoNtot)*1000
        print 'writing to file'
        fobj_out.write(c+','+str(s)+','+str(nevents)+','+str(NposmNnegoNtot)+','+str(XS)+','+str(weights)+','+boosted_dataset+','+globalTag+',FALSE'+','+generator+'\n')
        #print c+','+str(s)+','+str(nevents)+',Npos-Nneg/Ntotal,'+str(XS)+','+str(weights)+',boosted_dataset,'+globalTag+',FALSE'
fobj_out.close()


