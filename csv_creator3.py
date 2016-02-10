#!/usr/bin/env python

import das_client
import os
import subprocess

def get_datasets(dataset_wildcard):
    print 'getting datasets of ',dataset_wildcard
    tmp = os.popen("python das_client.py --limit=20 --query="+dataset_wildcard).read()
    #print tmp.rstrip().split('\n')[3:]
    return tmp.rstrip().split('\n')[3:]

def get_events(dataset):
    print 'requesting nevents'
    tmp=os.popen("python das_client.py --limit=20 --query='dataset="+dataset+" | grep dataset.nevents'"+" --format=plain").read()
    tmp1=tmp.rstrip().split('\n')[3]
    print tmp1
    return tmp1

def get_type(dataset):
    print 'looking for datatype'
    tmp=os.popen("python das_client.py --limit=20 --query='dataset="+dataset+" | grep dataset.datatype'"+" --format=plain").read()
    tmp1=tmp.rstrip().split('\n')[3]
    print tmp1
    return str(tmp1)

def get_generator(dataset):
    print 'looking for generator'
    tmp=os.popen("python das_client.py --limit=20 --query='dataset="+dataset+" | grep dataset.mcm.generators'"+" --format=plain").read()
    #print tmp
    tmp1=tmp.rstrip().split('\n')[3:]
    #print tmp1
    if not tmp1:
        print '?'
        return '?'
    else:
        print tmp1[0].replace('["','').replace('"]','').replace('", "',' ')
    #print tmp1[0][2:-2].replace('", "',' ')
    #return tmp1[0][2:-2].replace('", "',' ')
        return tmp1[0].replace('["','').replace('"]','').replace('", "',' ')

def get_boosted(parent_dataset):
    print 'looking for boosted datasets in prod/phys03'
    tmp=os.popen("python das_client.py --limit=20 --query='child dataset="+parent_dataset+" instance=prod/phys03'"+" --format=plain").read()
    tmp1=tmp.rstrip().split('\n')[3:]
    #if not tmp1:
     #   print '?'
     #   return '?'
    #else:
     #   print tmp1[0]
    #print tmp1[0].replace("'","")
    #return tmp1[0].replace("'","")
    print str(tmp1).replace("'","").replace(","," | ")
    return tmp1

samples = {'category': {'ttbar': {'name' : 'ttbar' , 'dataset_wildcard': '/TT_TuneCUETP8M1_13TeV*powheg-pythia8*/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' ,        					  'XS': 831.76, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/*Boostedv4MiniAOD*/USER' , 'generator' : 'POWHEG'},
			'ttHbb': {'name' : 'ttHbb' , 'dataset_wildcard': '/ttHTobb_M125_13TeV*powheg_pythia8*/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' , 
                                  'XS': 0.2934, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '/ttHTobb_M125_13TeV_powheg_pythia8/*Boostedv4MiniAOD*/USER' , 'generator' : 'POWHEG'},
                        'ttHnonbb' : {'name' : 'ttHnonbb' , 'dataset_wildcard': '/ttHToNonbb_M125_13TeV*powheg_pythia8*/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' , 
                                  'XS': 0.2151, 'NposmNnegoNtot' : 1, 'boosted_dataset' : '/ttHToNonbb_M125_13TeV_powheg_pythia8/*Boostedv4MiniAOD*/USER' , 'generator' : 'POWHEG'},
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
                        'DYJetsToLL': {'name' : 'DYJetsToLL' , 'dataset_wildcard': '/DYJetsToLL*50_TuneCUETP8M1_13TeV*pythia8/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM',                     'XS': 0, 'NposmNnegoNtot' : 0, 'boosted_dataset' : '?' , 'generator' : 'aMC'},
                        'WJets': {'name' : 'WJets' , 'dataset_wildcard': '/WJetsToLNu*TuneCUETP8M1_13TeV*pythia8/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM' ,        					 'XS': 0, 'NposmNnegoNtot' : 0, 'boosted_dataset' : '?' , 'generator' : 'notSpecified'},
                        'el_data': {'name' : 'el_reminiaod' , 'dataset_wildcard': '/SingleElectron/Run2015D-16Dec2015-v1/MINIAOD' , 'XS': 0, 'NposmNnegoNtot' : 0, 'boosted_dataset' : '?' , 'generator' : '?'},
                        'mu_data': {'name' : 'mu_reminiaod' , 'dataset_wildcard': '/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD' , 'XS': 0, 'NposmNnegoNtot' : 0, 'boosted_dataset' : '?' , 'generator' : '?'}}}#,
                        #'QCD':   {'name' : 'QCD' , 'dataset_wildcard': '/QCD_HT*TuneCUETP8M1_13TeV*pythia8/RunIISpring15MiniAOD*76X_mcRun2_asymptotic_v12*/MINIAODSIM' ,        	                         'XS': 0, 'NposmNnegoNtot' : 0, 'boosted_dataset' : '?'}}}



globalTag_mc='76X_mcRun2_asymptotic_v12'
globalTag_data='76X_dataRun2_v15'
#categorys=samples['category']
#print categorys
#category=categorys['ttbar']
#print category
fobj_out = open("mc_samples.csv","w")
for c in samples['category']:
    fobj_out.write(',,,,,,,,'+'\n')
    categorys=samples['category']
    category=categorys[c]
    dataset=get_datasets(category['dataset_wildcard'])
    XS=category['XS'] #in pb
    NposmNnegoNtot=category['NposmNnegoNtot']
    #boosted_dataset=category['boosted_dataset']
    #generator=category['generator']
    #boosted_dataset_wildcard=get_boosted_datasets(category['boosted_dataset'])
    for s in dataset:
        print 'looking at dataset ',s
        nevents=get_events(s)
        generator=get_generator(s)
        data_or_mc=get_type(s)
        boosted_dataset1=get_boosted(s)
        if(NposmNnegoNtot==0):
             weights=XS/(float(nevents)*1)*1000
        else:
             weights=XS/(float(nevents)*NposmNnegoNtot)*1000
        print 'writing to file'
        if(data_or_mc=='"mc"'):
             true_or_false='FALSE'
             fobj_out.write(c+','+str(s)+','+nevents+','+str(NposmNnegoNtot)+','+str(XS)+','+str(weights)+','+str(boosted_dataset1).replace("'","").replace(","," | ")	  		     +','+globalTag_mc+','+true_or_false+','+generator+'\n')
        if(data_or_mc=='"data"'):
             true_or_false='TRUE'
	     fobj_out.write(c+','+str(s)+','+nevents+',,,,'+str(boosted_dataset1).replace("'","").replace(","," | ")+','+globalTag_data+','+true_or_false+','+'\n')
        
        
        #print c+','+str(s)+','+str(nevents)+',Npos-Nneg/Ntotal,'+str(XS)+','+str(weights)+',boosted_dataset,'+globalTag+',FALSE'
fobj_out.close()


