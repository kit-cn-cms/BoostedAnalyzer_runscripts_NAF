import das_client
import csv
import os
import stat
import sys
import datetime
import user_config
store_prefix='file:/pnfs/desy.de/cms/tier2/'

def get_metainfo(path,nevents_in_job):
    meta='#meta nevents : '+str(nevents_in_job)+'\n'
    meta+='#meta cutflow : '+path+'_nominal_Cutflow.txt\n'
    if user_config.systematics:
        meta+='#meta check : '+path+'_JESUP_Cutflow.txt\n'
        meta+='#meta check : '+path+'_JESDOWN_Cutflow.txt\n'
        meta+='#meta check : '+path+'_JERUP_Cutflow.txt\n'
        meta+='#meta check : '+path+'_JERDOWN_Cutflow.txt\n'
    meta+='#meta check : '+path+'_nominal_Tree.root\n'
    if user_config.systematics:
        meta+='#meta check : '+path+'_JESUP_Tree.root\n'
        meta+='#meta check : '+path+'_JESDOWN_Tree.root\n'
        meta+='#meta check : '+path+'_JERUP_Tree.root\n'
        meta+='#meta check : '+path+'_JERDOWN_Tree.root\n'
    return meta

def get_vars(jobconfig):
    argument=""
    argument+=" outName="+str(jobconfig["outName"])
    argument+=" weight="+str(jobconfig["weight"])
    argument+=" isData="+str(jobconfig["isData"])
    argument+=" isBoostedMiniAOD="+str(jobconfig["isBoostedMiniAOD"])
    argument+=" makeSystematicsTrees="+str(jobconfig["makeSystematicsTrees"])
    argument+=" analysisType="+str(jobconfig["analysisType"])
    argument+=" inputFiles="+str(jobconfig["inputFiles"])
    argument+=" maxEvents="+str(jobconfig["maxEvents"])
    argument+=" globalTag="+str(jobconfig["globalTag"])
    argument+="\n"
    return argument
    

def create_script(name,ijob,files_in_job,nevents_in_job,eventsinsample,jobconfig):
    outfilename=user_config.outpath+'/'+name+'/'+name+'_'+str(ijob)
    jobconfig['inputFiles']=','.join(files_in_job)
    jobconfig['outName']=outfilename

    script='#!/bin/bash\n'
    script+='export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n'
    script+='source $VO_CMS_SW_DIR/cmsset_default.sh\n'
    script+='cd '+user_config.cmsswpath+'/src\neval `scram runtime -sh`\n'
    script+='cmsRun '+user_config.cmsswcfgpath+get_vars(jobconfig)
    script+=get_metainfo(outfilename,nevents_in_job)
    filename=current_scriptpath+'/'+name+'/'+name+'_'+str(ijob)+'.sh'
    f=open(filename,'w')
    f.write(script)
    f.close()
    f_list.write(filename+'\n')
    print 'created script',filename
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)



def get_dataset_files(dataset):
    print 'getting files for',dataset
    data=das_client.get_data("https://cmsweb.cern.ch","file dataset="+dataset+" instance="+user_config.dbs,0,0,0)
    nevents=0
    size=0
    nfiles=0
    files=[]
    events_in_files=[]
    for d in data['data']:
#        print d
        for f in d['file']:
            if not 'nevents' in f: continue
            files.append(store_prefix+f['name'])
            events_in_files.append(f['nevents'])
            nevents+=f['nevents']
            size+=f['size']
            nfiles+=1

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

    
    for f,nev in zip(files,events):
        nevents_in_job+=nev
        files_in_job.append(f)
        if nevents_in_job>user_config.min_events_per_job:
            ijob+=1
            create_script(name,ijob,files_in_job,nevents_in_job,eventsinsample,jobconfig)
            nevents_in_job=0
            files_in_job=[]


#-------------------------------    
print 'outpath',user_config.outpath
print 'scriptpath',user_config.scriptpath
print 'cmsswcfgpath',user_config.cmsswcfgpath
print 'cmsswpath',user_config.cmsswpath
print 'samplelist',user_config.samplelist

# check paths
current_scriptpath=user_config.scriptpath
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
if not os.path.exists(user_config.cmsswpath):
    print 'WRONG CMSSW PATH!'
    print user_config.cmsswpath
    sys.exit()
if not os.path.exists(user_config.cmsswcfgpath):
    print 'WRONG CMSSW CONFIG PATH!'
    print user_config.cmsswcfgpath
    sys.exit()

# read list with samples
csvfile=open(user_config.samplelist,'r') 
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
    if name=='': continue
    print 'creating jobs for', name
    jobconfig={}
    jobconfig['weight']=weight
    jobconfig['isData']=False
    if 'isData' in reader.fieldnames:
        if 'true' in row['isData'].lower():
            jobconfig['isData']=True            
    jobconfig['analysisType']=user_config.analysisType
    jobconfig['globalTag']=row['globalTag']
    jobconfig['isBoostedMiniAOD']=user_config.isBoostedMiniAOD
    jobconfig['makeSystematicsTrees']=user_config.systematics and not jobconfig['isData']
    jobconfig['maxEvents']=999999999
    
    create_jobs(name,dataset,jobconfig)

f_list.close()
