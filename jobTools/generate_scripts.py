#!/usr/bin/env python
# usage: ./generate_scripts.py
# need to configure user_config.py

#import das_client
import csv
import os
import stat
import sys
import datetime
import imp
import ssl
import glob
import ROOT
ssl._create_default_https_context = ssl._create_unverified_context
#das_client=imp.load_source("das_client", "/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/das_client/v02.17.04/bin/das_client.py")
import Utilities.General.cmssw_das_client as das_client
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../configs")
basepath=os.path.dirname(os.path.realpath(__file__))+"/../"

def get_metainfo(path,nevents_in_job,jobconfig):
    meta='#meta nevents : '+str(nevents_in_job)+'\n'
    meta+='#meta cutflow : '+path+'_nominal_Cutflow.txt\n'
#    if user_config.systematics and not jobconfig['isData']:
#        meta+='#meta check : '+path+'_JESUP_Cutflow.txt\n'
#        meta+='#meta check : '+path+'_JESDOWN_Cutflow.txt\n'
#        meta+='#meta check : '+path+'_JERUP_Cutflow.txt\n'
#        meta+='#meta check : '+path+'_JERDOWN_Cutflow.txt\n'
    meta+='#meta check : '+path+'_nominal_Tree.root\n'
#    if user_config.systematics and not jobconfig['isData']:
#        meta+='#meta check : '+path+'_JESUP_Tree.root\n'
#        meta+='#meta check : '+path+'_JESDOWN_Tree.root\n'
#        meta+='#meta check : '+path+'_JERUP_Tree.root\n'
#        meta+='#meta check : '+path+'_JERDOWN_Tree.root\n'
    return meta

def get_vars(jobconfig):
    argument=""
    argument+=" outName="+str(jobconfig["outName"])
    argument+=" weight="+str(jobconfig["weight"])
    argument+=" isData="+str(jobconfig["isData"])
    #argument+=" isBoostedMiniAOD="+str(jobconfig["isBoostedMiniAOD"])
    argument+=" inputFiles="+str(jobconfig["inputFiles"])
    argument+=" maxEvents="+str(jobconfig["maxEvents"])
    argument+=" globalTag="+str(jobconfig["globalTag"])
    #argument+=" generatorName="+str(jobconfig['generatorName'])
    #argument+=" additionalSelection="+str(jobconfig['additionalSelection'])
    argument+=" systematicVariations="+str(jobconfig['systematicVariations'])
    argument+=" ProduceMemNtuples="+str(jobconfig['ProduceMemNtuples'])
    argument+=" dataEra="+str(jobconfig['dataEra'])
    #argument+=" dataset="+str(jobconfig['dataTrigger'])
    argument+="\n"
    return argument


def get_list_of_systematics(filename):
    systs=[]
    with open(filename,"r") as f:
        systs=f.readlines()
    systs=[s.rstrip('\n') for s in systs]
    systs=[s.rstrip('\t') for s in systs]
    good_systs=[s for s in systs if not (s.startswith("#") or len(s)==0)]
    if len(good_systs) != len(set(good_systs)):
        print "ERROR specifying list of systematics: DUPLICATE ENTRIES"
        sys.exit()
    if not "nominal" in good_systs:
        print "WARNING: no 'nominal' variation specified...adding it"
        good_systs.insert(0,"nominal")

    print "Systematic variations:"
    for syst in good_systs:
        print "  '"+syst+"'"

    return good_systs


def split_for_systematic_variations(jobconfig):
    jobconfigs=[]
    
    if jobconfig['isData']:
        cfg=jobconfig.copy()
        cfg['systematicVariations']="nominal"
        cfg['nSystematicVariationsPerJob']=1
        jobconfigs.append(cfg)
    else:
        systs_str=""
        isyst=1
        for syst in jobconfig['systematicVariations']:
            if syst == "nominal":
                cfg = jobconfig.copy()
                cfg["systematicVariations"] = "nominal"
                jobconfigs.append(cfg)
                continue
            if len(systs_str)>0:
                systs_str+=","
            systs_str+=str(syst)
            if isyst < jobconfig['nSystematicVariationsPerJob']:
                isyst+=1
            else:
                cfg=jobconfig.copy()
                cfg['systematicVariations']=systs_str
                jobconfigs.append(cfg)
                systs_str=""
                isyst=1
        if len(systs_str)>0:
            cfg=jobconfig.copy()
            cfg['systematicVariations']=systs_str
            jobconfigs.append(cfg)
    return jobconfigs    
    

def create_script(name,ijob,isyst,files_in_job,nevents_in_job,eventsinsample,jobconfig):
    dirname = name
    if "nominal" in jobconfig["systematicVariations"]:
        dirname+="_nominal"
        if not os.path.exists(current_scriptpath+'/'+dirname):
            os.makedirs(current_scriptpath+'/'+dirname)

    outfilename=user_config.outpath+'/'+name+'/'+name+'_'+str(ijob)
    jobconfig['inputFiles']=','.join(files_in_job)
    jobconfig['outName']=outfilename

    script='#!/bin/bash\n'
    script+='export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n'
    script+='source $VO_CMS_SW_DIR/cmsset_default.sh\n'
    script+='# check release\n'
    script+='OS="`uname -r`"\n'

    script+='if [[ $OS == *"el7"* ]]; then\n'
    script+='  echo detected SL7, running ' + user_config.cmsswpathSL7 + '\n'
    script+='  cd '+user_config.cmsswpathSL7+'/src\neval `scram runtime -sh`\n'
    script+='  cmsRun '+user_config.cmsswcfgpathSL7+get_vars(jobconfig)
    script+='fi\n'

    script+=get_metainfo(outfilename,nevents_in_job,jobconfig)
    filename=current_scriptpath+'/'+dirname+'/'+name+'_'+str(ijob)+'_'+str(isyst)+'.sh'
    f=open(filename,'w')
    f.write(script)
    f.close()
    f_list.write(filename+'\n')
    print 'created script',filename
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)
    

def create_scripts(name,ijob,files_in_job,nevents_in_job,eventsinsample,jobconfig):
    jobconfigs=split_for_systematic_variations(jobconfig)
    for isyst,cfg in enumerate(jobconfigs):
        print "copying jobs for systematic variations "+str(isyst+1)+": "+str(cfg['systematicVariations'])
        create_script(name,ijob,isyst+1,files_in_job,nevents_in_job,eventsinsample,cfg)


def get_dataset_files(dataset):
    print 'getting files for',dataset
    datasets=[x.strip("'") for x in dataset.split(',')]
    print datasets
    #ckey=das_client.x509()
    #cert=das_client.x509()
    #das_client.check_auth(ckey)
    nevents=0
    size=0
    nfiles=0
    files=[]
    events_in_files=[]
    is_dataset_string = True
    for dataset in datasets:
        if "pnfs" in dataset:
            is_dataset_string = False
            break
    
    if is_dataset_string:
        for dataset in datasets:
                    store_prefix = ""
                    if "USER" in dataset:
                        store_prefix = "file:/pnfs/desy.de/cms/tier2/"
                    else:
                        store_prefix = "root://xrootd-cms.infn.it//"
                    data=das_client.get_data("file dataset="+dataset+" instance="+user_config.dbs)
                    # print data
                    for d in data['data']:
                        for f in d['file']:
                            if not 'nevents' in f: continue
                            # hack to avoid problem with new_pmx samples and same child dataset name ...
                            if "ttHTobb" in f['name'] and "180617_091548" in f['name']:
                                print "skipping ttHTobb new pmx file"
                                continue
                            if "ST_t-channel" in f['name'] and "180618_081310" in f['name']:
                                print "skipping single top new_pmx file"
                                continue
                            if "SingleMuon" in f['name'] and "Run2017C" in f['name'] and "180617_220957" in f['name']:
                                print "skiping single muon files from job which was killed"
                                continue
                            ###
                            files.append(store_prefix+f['name'])
                            events_in_files.append(f['nevents'])
                            nevents+=f['nevents']
                            size+=f['size']
                            nfiles+=1
    else:
        store_prefix = "file:"
        for dataset in datasets:
            directory = dataset
            print directory+"/Skim_*.root"
            files+=glob.glob(directory+"/Skim_*.root")
        
        nfiles=len(files)
        chain=ROOT.TChain("Events","Events")
        nevents_tmp=0
        for f in files:
            print f
            chain.Add(f)
            events_in_files.append(chain.GetEntries()-nevents_tmp)
            nevents_tmp=chain.GetEntries()
        nevents=chain.GetEntries()
    
        #adding missing store_prefix
        files_without_prefix=files
        files=[]
        for f in files_without_prefix:
            files.append(store_prefix+f)
            
    print nfiles,'files with total size',size/(1024*1024),'MB containing',nevents,'events'
    return files,events_in_files

def create_jobs(name,dataset,jobconfig):
    files,events=get_dataset_files(dataset)
    nevents_in_job=0
    files_in_job=[]
    ijob=0
    eventsinsample=sum(events)
    folder=current_scriptpath+'/'+name
    if not os.path.exists(folder):
        os.makedirs(folder)       
    if not os.path.exists(user_config.outpath+'/'+name):
        os.makedirs(user_config.outpath+'/'+name)       
    
    
    total_events = 0
    for f,nev in zip(files,events):
        nevents_in_job+=nev
        total_events += nev
        files_in_job.append(f)
        if nevents_in_job>user_config.min_events_per_job or f==files[-1] or len(files_in_job)==100:
            ijob+=1
            create_scripts(name,ijob,files_in_job,nevents_in_job,eventsinsample,jobconfig)
            nevents_in_job=0
            files_in_job=[]

            if not jobconfig["maxEventsTotal"] == -1 and jobconfig["maxEventsTotal"] < total_events:
                print("max number of entries {} reached for this sample".format(jobconfig["maxEventsTotal"]))
                break


#-------------------------------    
#import user_config
if len(sys.argv) > 1:
    cfgname=os.path.basename(sys.argv[1])
    assert cfgname[-3:]=='.py'
    user_config=__import__(cfgname[:-3])
else:
    print 'usage: ./generate_scripts.py user_config.py'
   
    

print 'outpath',user_config.outpath
print 'scriptpath',user_config.scriptpath
print 'cmsswcfgpathSL7',user_config.cmsswcfgpathSL7
print 'cmsswpathSL7',user_config.cmsswpathSL7
print 'samplelist',user_config.samplelist
print 'systematicVariations',user_config.systematicVariations

# check paths
current_scriptpath=basepath+"workdir/"+user_config.scriptpath
if not os.path.exists(current_scriptpath):
    os.makedirs(current_scriptpath)
else:
    current_scriptpath+=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    os.makedirs(current_scriptpath)
    
if not os.path.exists(user_config.outpath):
    os.makedirs(user_config.outpath)
if not os.path.exists(user_config.outpath):
    print 'COULD NOT CREATE OUTPATH!'
    print user_config.outpath
    sys.exit()
if not os.path.exists(current_scriptpath):
    print 'COULD NOT CREATE SCRIPTPATH!'
    print current_scriptpath
    sys.exit()
if not os.path.exists(user_config.cmsswpathSL7):
    print 'WRONG CMSSW PATH SL7!'
    print user_config.cmsswpathSL7
    sys.exit()
if not os.path.exists(user_config.cmsswcfgpathSL7):
    print 'WRONG CMSSW CONFIG PATH! SL7'
    print user_config.cmsswcfgpathSL7
    sys.exit()  
if user_config.dataset_column == "dataset" and not user_config.dbs == "prod/global":
    print "If you use the dataset column which is for global samples, you have to you prod/global as dbs instance"
    print "You used ",user_config.dbs
    sys.exit()
    
if user_config.dataset_column == "boosted_dataset" and not user_config.dbs == "prod/phys03":
    print "If you use the boosted_dataset column which is for user samples, you have to you prod/phys03 as dbs instance"
    print "You used ",user_config.dbs
    sys.exit()

# read list with samples

csvpath=basepath+"samplelists/"+user_config.samplelist
csvfile=open(csvpath,'r') 
reader = csv.DictReader(csvfile, delimiter=',')
# create job list
f_list=open(current_scriptpath+'/joblist.txt','w')

for row in reader:
    dataset="'"+row[user_config.dataset_column]+"'"
    name=row['name']
    if 'weight' in reader.fieldnames:
        weight=row['weight']
    else:
        weight='1'
    if name=='' or name.startswith("#"): continue
    print 'creating jobs for', name
    jobconfig={}
    jobconfig['weight']=weight
    jobconfig['isData']=False
    if 'isData' in reader.fieldnames:
        if 'true' in row['isData'].lower():
            jobconfig['isData']=True
    #if 'generator' in reader.fieldnames:
        #if row['generator'] != '':
            #jobconfig['generatorName']=row['generator']
    #if 'additionalSelection' in reader.fieldnames:
        #if row['additionalSelection'] != '':
            #jobconfig['additionalSelection']=row['additionalSelection']
    jobconfig['globalTag']=row['globalTag']
    #jobconfig['isBoostedMiniAOD']=user_config.isBoostedMiniAOD
    jobconfig['maxEvents']=999999999
    jobconfig['systematicVariations']=get_list_of_systematics(basepath+"configs/"+user_config.systematicVariations)
    jobconfig['nSystematicVariationsPerJob']=user_config.nSystematicVariationsPerJob
    jobconfig['dataEra']=row['run']
    jobconfig['ProduceMemNtuples']=user_config.ProduceMemNtuples
    
    try:
        jobconfig["maxEventsTotal"] = user_config.max_events_total
    except:
        jobconfig["maxEventsTotal"] = -1

    #jobconfig['dataTrigger']=row['dataTrigger']
    if dataset=="''":
        continue
    create_jobs(name,dataset,jobconfig)

f_list.close()

