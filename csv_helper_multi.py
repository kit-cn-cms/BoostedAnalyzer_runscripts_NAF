import imp
import json
#import das_client as dc
import GetTotalSampleNumbers_multi as gts
from collections import defaultdict
from multiprocessing import Pool
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
dc=imp.load_source("das_client", "/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/das_client/v02.17.04/bin/das_client.py")
# gets the json for a given dataset with wildcards

def get_data_(dataset):
    #print 'getting files for',dataset
    ckey=dc.x509()
    cert=dc.x509()
    dc.check_auth(ckey)
    data=dc.get_data("https://cmsweb.cern.ch","dataset dataset="+dataset+" instance=prod/global status=*",0,0,0,500,ckey,cert)
    return data
"""
def get_data_(dataset):
    host="https://cmsweb.cern.ch"
    dataset_string="dataset="
    instance=" instance=prod/phys03"
    start_number=0
    max_entries=0
    wait_time=300
    ckey=dc.x509()
    cert=dc.x509()
    dc.check_auth(ckey)
    return dc.get_data(host,dataset_string+dataset+instance,start_number,max_entries,wait_time,ckey,cert)
"""
def get_children(dataset):
    #print dataset
    ckey=dc.x509()
    cert=dc.x509()
    dc.check_auth(ckey)
    data=dc.get_data("https://cmsweb.cern.ch","child dataset="+dataset+" instance=prod/phys03",0,0,0,500,ckey,cert)
    #print data
    return data

def get_first_file(dataset_name):
    ckey=dc.x509()
    cert=dc.x509()
    dc.check_auth(ckey)
    data=dc.get_data("https://cmsweb.cern.ch","file dataset="+dataset_name,0,0,0,500,ckey,cert)
    files=[]
    for d in data['data']:
        for f in d['file']:
            if not 'nevents' in f: continue
            files.append(f['name'])
            if(len(files)>=3):
                break
        if(len(files)>=3):
            break
    return files

def get_first_files(dataset_names):
    first_files_array=[]
    number_processes=len(dataset_names)
    pool=Pool(processes=number_processes)
    first_files_array=pool.map(get_first_file,dataset_names)
    pool.close()
    pool.join()
    return first_files_array

def search_index(array,key):
    #print "length ",len(array)
    for i in range(len(array)):
        #print array[i]
        #if(str(array[i].get(key,"none"))!="none"):
        if key in array[i]:
            return i
    return "none"

def get_names(dataset_wildcard_):
    results=get_data_(dataset_wildcard_)
    nresults=results.get("nresults","none")
    status=results.get("status","notok")
    while nresults=="none" or status=="notok":
        results=get_data_(dataset_wildcard_)
        nresults=results.get("nresults","none")
        status=results.get("status","notok")
    name_array=[]
    index1="none"
    for i in range(nresults):
        index1=search_index(results.get("data","none")[i].get("dataset","none"),"name")
        if index1!="none":
            name_array.append(results.get("data","none")[i].get("dataset","none")[index1].get("name","none"))
        else:
            continue
    return name_array


def get_jsons(name_array):
    json_array=[]
    number_processes=len(name_array)
    #print name_array
    #print number_processes
    pool=Pool(processes=number_processes)
    json_array=pool.map(get_data_,name_array)
    pool.close()
    pool.join()
    status_array=[]
    for i in range(len(json_array)):
        status=json_array[i].get("status","notok")
        if status=="notok":
            status_array.append(i)
    if len(status_array)>0:
        print "something went wrong with json of a/some dataset/s"
    status_array=sorted(status_array,reverse=True)
    for i in status_array:
        del json_array[i]
        del name_array[i]
    return json_array

def get_nevents(json_array):
    nresults=len(json_array)
    nevents_array=[]
    index1="none"
    index2="none"
    for i in range(nresults):
        index1=search_index(json_array[i].get("data","none"),"dataset")
        if index1!="none":
            index2=search_index(json_array[i].get("data","none")[index1].get("dataset","none"),"nevents")
	#print index1
	#print index2
	if index1!="none" and index2!="none":
            nevents_array.append(json_array[i].get("data","none")[index1].get("dataset","none")[index2].get("nevents","none"))
        else:
            nevents_array.append(0)
    return nevents_array

def get_nfiles(json_array):
    nresults=len(json_array)
    nfiles_array=[]
    index1="none"
    index2="none"
    for i in range(nresults):
        index1=search_index(json_array[i].get("data","none"),"dataset")
        if index1!="none":
            index2=search_index(json_array[i].get("data","none")[index1].get("dataset","none"),"nfiles")
        if index1!="none" and index2!="none":
            nfiles_array.append(json_array[i].get("data","none")[index1].get("dataset","none")[index2].get("nfiles","none"))
        else:
            nfiles_array.append(0)
    return nfiles_array

def get_datatypes(json_array):
    nresults=len(json_array)
    datatype_array=[]
    index1="none"
    index2="none"
    for i in range(nresults):
      try:
        index1=search_index(json_array[i].get("data","none"),"dataset")
        index2=search_index(json_array[i].get("data","none")[index1].get("dataset","none"),"datatype")
        if index1!="none" and index2!="none":
            datatype=json_array[i].get("data","none")[index1].get("dataset","none")[index2].get("datatype","none")
            if(datatype=="mc"):
                datatype_array.append("FALSE")
            if(datatype=="data"):
                datatype_array.append("TRUE")
        else:
            datatype_array.append("look at me again")
      except AttributeError:
	datatype_array.append("look at me again")
    return datatype_array

def get_globaltags(datatype_array):
    nresults=len(datatype_array)
    globaltag_array=[]
    for i in range(nresults):
        if datatype_array[i]=="TRUE":
            globaltag_array.append("94X_dataRun2_ReReco_EOY17_v2")
        elif datatype_array[i]=="FALSE":
            globaltag_array.append("94X_mc2017_realistic_v12")
        else:
            globaltag_array.append("look at me again")
    return globaltag_array

def get_generators(name_array):
    nresults=len(name_array)
    generator_array=[]
    for i in range(nresults):
        if name_array[i].find("powheg")!=-1:
            generator_array.append("POWHEG")
        elif name_array[i].find("amc")!=-1:
            generator_array.append("aMC")
        elif name_array[i].find("madgraph")!=-1:
            generator_array.append("MadGraph")
        elif name_array[i].find("pythia")!=-1:
            generator_array.append("pythia8")
        else:
            generator_array.append("notSpecified")
    return generator_array

def get_x(name):
    if(name[0].lower().find("amc")!=-1 or name[0].lower().find("powheg")!=-1):
        x=0.
        while True:
            try:
                x=gts.GetTotalSampleNumbers(name)
            except ReferenceError:
                x=0.
            if x!=0.:
                break
    else:
        x=1.
    return x

def get_xs(name_array):
    #pool=Pool(processes=len(name_array))
    #xs=pool.map(get_x,name_array)
    xs=[]
    for name in name_array:
        xs.append(get_x(name))
    return xs

def get_weights(nevents_array,neg_fractions_array,xs):
    weights=[]
    for i in range(len(nevents_array)):
	if(neg_fractions_array[i]!=0. and nevents_array[i]!=0):
	  weights.append(xs*(10**3)/(neg_fractions_array[i]*nevents_array[i]))
	else:
	  weights.append(0.)
    return weights

def get_children_array(parent_dataset):
    results=get_children(parent_dataset)
    nresults=results.get("nresults","none")
    status=results.get("status","notok")
    #nresults=get_children(parent_dataset).get("nresults","none")
    while nresults=="none" or status=="notok":
        results=get_children(parent_dataset)
        nresults=results.get("nresults","none")
        status=results.get("status","notok")
    #print "resuuuuuuuuuuuuults",nresults
    name_array=[]
    for i in range(nresults):
        try:
            index_=search_index(results.get("data","none")[i].get("child","none"),"name")
        except TypeError:
            continue
	try:
            child_candidate=results.get("data","none")[i].get("child","none")[index_].get("name","none")
	except TypeError:
            continue
	#print "teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest",child_candidate
	if(child_candidate.find("mwassmer")!=-1):
	    name_array.append(child_candidate)
        #print "#children ",len(name_array)
    return name_array

def get_children_names_(parent_dataset_array):
  pool=Pool(processes=len(parent_dataset_array))
  children=pool.map(get_children_array,parent_dataset_array)
  pool.close()
  pool.join()
  return children

"""
def get_children_names(parent_dataset_array):
    children_array=[]
    for parent_dataset in parent_dataset_array:
        nresults=get_children(parent_dataset).get("nresults","none")-1
        name_array=[]
        for i in range(nresults):
            index_=search_index(get_children(parent_dataset).get("data","none")[i].get("child","none"),"name")
            child_candidate=get_children(parent_dataset).get("data","none")[i].get("child","none")[index_].get("name","none")
            if(child_candidate.find("mschrode")!=-1):
                name_array.append(child_candidate)
        children_array.append(name_array)
    return children_array
"""
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items()
                            if len(locs)>1)

def merge_ext(name_array):
    #ext=[]
    ext_name=[]
    n_exts=0
    for i in range(len(name_array)):
      if(name_array[i].find("_ext")!=-1):
	        pos=name_array[i].find("_ext")
	        #ext.append(i)
	        ext_str=name_array[i][pos:pos+8]
	        ext_name.append(name_array[i].replace(ext_str,""))
	        n_exts+=1
      else:
	        #ext.append(0)
	        pos=name_array[i].find("/MINIAODSIM")
	        ext_str=name_array[i][pos-3:pos]
	        ext_name.append(name_array[i].replace(ext_str,""))
    if n_exts==0:
        return []
    else:
        duplicates=list_duplicates(ext_name)
        dups=[]
        #print duplicates[0]
        for dup in duplicates:
                dups.append(dup[1])
                #print dup[1]
            #dups.append(dup[1])
        return dups
  
def get_runs(name_array):
    run_array=[]
    for i in range(len(name_array)):
        if(name_array[i].find("Run2016")!=-1):
            pos=name_array[i].find("Run2016")
            run_str=name_array[i][pos+3:pos+8]
            run_array.append(run_str)
        else:
            run_array.append("")
    return run_array


def get_reHLT(names_array):
  reHLT_array=[]
  for name in names_array:
    if(name.find("reHLT")==-1):
      reHLT_array.append("FALSE")
    else:
      reHLT_array.append("TRUE")
  return reHLT_array

def remove_duplicates(duplicates_array,names,jsons,nevents,nfiles,datatypes,globaltags,generators,boosted_datasets,is_reHLTs,neg_fractions,weights,runs,xs):
  dupls=[]
  for duplicate in duplicates_array:
    #print duplicate
    nevents_tmp=0
    nfiles_tmp=0
    neg_fractions_tmp=0
    names_tmp='"'
    globaltags_tmp=globaltags[duplicate[0]]
    datatypes_tmp=datatypes[duplicate[0]]
    generators_tmp=generators[duplicate[0]]
    jsons_tmp=jsons[duplicate[0]]
    is_reHLTs_tmp=is_reHLTs[duplicate[0]]
    boosted_datasets_tmp=boosted_datasets[duplicate[0]]
    runs_tmp=runs[duplicate[0]]
    for i in range(len(duplicate)):
      dupl_position=duplicate[i]
      dupls.append(dupl_position)
      #print dupl_position
      nevents_tmp+=nevents[dupl_position]
      nfiles_tmp+=nfiles[dupl_position]
      neg_fractions_tmp+=neg_fractions[dupl_position]
      #boosted_datasets_tmp+=boosted_datasets[dupl_position]
      if(i==0):
	names_tmp+=names[dupl_position]
      else:
	names_tmp+=","+names[dupl_position]
    names_tmp+='"'
    neg_fractions_tmp=neg_fractions_tmp/len(duplicate)
    try:
      weights_tmp=float(xs)*1000/(neg_fractions_tmp*nevents_tmp)
    except ZeroDivisionError:
      weights_tmp=0.
    #print nevents_tmp,nfiles_tmp,neg_fractions_tmp,weights_tmp,boosted_datasets_tmp,names_tmp
    names.append(names_tmp)
    jsons.append(jsons_tmp)
    nevents.append(nevents_tmp)
    nfiles.append(nfiles_tmp)
    datatypes.append(datatypes_tmp)
    globaltags.append(globaltags_tmp)
    generators.append(generators_tmp)
    is_reHLTs.append(is_reHLTs_tmp)
    boosted_datasets.append(boosted_datasets_tmp)
    #boosted_datasets=boosted_datasets_tmp
    neg_fractions.append(neg_fractions_tmp)
    weights.append(weights_tmp)
    runs.append(runs_tmp)
  dupls=sorted(dupls,reverse=True)
  #print dupls
  for i in dupls:
    del names[i]
    del jsons[i]
    del nevents[i]
    del nfiles[i]
    del datatypes[i]
    del globaltags[i]
    del generators[i]
    del boosted_datasets[i]
    del is_reHLTs[i]
    del neg_fractions[i]
    del weights[i]
    del runs[i]
  

"""
#dataset_wildcard="/TT_TuneCUETP8M1_13TeV*powheg-pythia8*/RunIIFall15MiniAODv2*76X_mcRun2_asymptotic_v12*/MINIAODSIM"
dataset_wildcard1="/ttHTobb_M125_13TeV*powheg_pythia8*/*80X*/MINIAODSIM"

#print results.get("data","none")[0]
name_array=get_names(dataset_wildcard1)
json_array=get_jsons(name_array)
print name_array
print "##########################"
print get_nevents(name_array,json_array)
print "##########################"
print get_nfiles(name_array,json_array)
print "##########################"
print get_datatypes(json_array)
print "##########################"
print get_globaltags(json_array)
print "##########################"
print get_generators(json_array)
"""

#print get_globaltags(json_array)
"""
blabla=search_index(json_array[0].get("data","none")[0].get("dataset","none"),"result")
print "Dictionary after search with full name of a dataset"
for key,value in json_array[0].iteritems():
    print key
    print value
    print "##############"
print " "
print "Dictionary of key data"
for key,value in json_array[0].get("data","none")[0].iteritems():
    print key
    print value
    print "##############"
print " "
print "Dicitonary of key dataset in data dict"
for i in range(len(json_array[0].get("data","none")[0].get("dataset","none"))):
    print "array element",i
    for key,value in json_array[0].get("data","none")[0].get("dataset","none")[i].iteritems():
        print key
        print value
        print "##############"
print " "
print "Dictionary of key result in dataset dict "
for key,value in json_array[0].get("data","none")[0].get("dataset","none")[blabla].get("result","none")[0].iteritems():
    print key
    print value
    print "##############"
    print json_array[0].get("data","none")[0].get("dataset","none")[blabla].get("result","none")[0].get(key).get("GlobalTag","none")
"""
