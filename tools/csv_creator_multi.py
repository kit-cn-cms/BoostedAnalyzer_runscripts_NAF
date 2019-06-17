import csv
import sys
import csv_helper_multi as chm
import os

fobj = open(sys.argv[1],"rb")

reader=csv.reader(fobj)
csv_array=[]
for row in reader:
    print row[0]
    if row[0].find("#")!=-1:
        continue
    csv_array.append(row)
fobj.close()

output = os.path.basename(sys.argv[1])
fobj_out=open("../samplelists/auto_samples_"+output,"w")

# header for the csv file
fobj_out.write('name,dataset,nGen,Npos-Nneg/Ntotal,XS,weight,boosted_dataset,globalTag,isData,generator,additionalSelection,run'+'\n')

for row in csv_array:
    # search for datasets in DAS with the given DAS dataset containing wildcards (*) in general
    print "getting names for ...",row[1]
    names=chm.get_names(row[1])
    
    # search for duplicates in the found dataset names (fail-safe)
    name_duplicates=chm.list_duplicates(names)
    if len(names)==0 or next(name_duplicates,0)!=0:
        print "no datasets have been found for this query or there are duplicate datasets in the response" 
        continue
    
    print "############################ dataset names ################################"
    print names
    
    jsons=[]
    nevents=[]
    n_tried=0
    while True:
        if n_tried>5:
            break
        print "getting jsons for corresponding datasets ..."
        # if there are too many datasets there are some problems retriving information about all of them -> make bunches of datasets and treat each bunch separately
        if len(names)<10:
            jsons=chm.get_jsons(names)
        else:
            for i in range((len(names)//10)+1):
                jsons+=chm.get_jsons(names[i*10:(i+1)*10])
        #print "############################ jsons ################################"
        #print jsons
        print "getting event numbers ..."
        nevents=chm.get_nevents(jsons)
        print nevents
        # check if all datasets have a number of events differently from zero
        if not 0 in nevents:
            break
        n_tried+=1
    if n_tried>5:
        print "somehow the event numbers could not be determined"
        continue
    #print "############################ nevents ################################"
    #print nevents
    print "getting number of files ..."
    nfiles=chm.get_nfiles(jsons)
    #print "############################ nfiles ################################"
    #print nfiles
    print "getting first files ..."
    files=chm.get_first_files(names)
    #print "############################# first files ################################"
    #print files
    print "getting datatype mc (FALSE) or data (TRUE) ..."
    datatypes=chm.get_datatypes(jsons)
    print "############################ datatypes ################################"
    #print datatypes
    print "getting globaltags ..."
    globaltags=chm.get_globaltags(datatypes)
    #print "############################ globaltags ################################"
    #print globaltags
    print "getting generators ..."
    generators=chm.get_generators(names)
    #print "############################ generators ################################"
    #print generators
    print "getting boosted/skimmed datasets ..."
    boosted_datasets=chm.get_children_names_(names)
    print "############################ boosted datasets ################################"
    print boosted_datasets
    print "getting negative event fractions ..."
    neg_fractions=chm.get_xs(files)
    #print "########################### neg event fractions #########################"
    #print neg_fractions
    print "getting weights ..."
    weights=chm.get_weights(nevents,neg_fractions,float(row[2]))
    #print "############################ weights ################################"
    #print weights
    #print "getting is_reHLT ..."
    print "getting runs ..."
    runs=chm.get_runs(names)
    is_reHLTs=chm.get_reHLT(names)
    
    #################### this section deals with finding extensions and putting them together in the csv file ##########################
    duplicates_ext_array=chm.merge_ext(names)
    chm.remove_duplicates(duplicates_ext_array,names,jsons,nevents,nfiles,datatypes,globaltags,generators,boosted_datasets,is_reHLTs,neg_fractions,weights,runs,row[2])
    #duplicates_Run_array=chm.merge_run(names)
    #chm.remove_duplicates(duplicates_Run_array,names,jsons,nevents,nfiles,datatypes,globaltags,generators,boosted_datasets,is_reHLTs,neg_fractions,weights,row[2])
    
    xs=float(row[2])
    print "writing found datasets and their information ..."
    fobj_out.write(",,,,,,,,,,,"+'\n')
    # loop over all the datasets which fit to the dataset with wildcards
    for i in range(len(jsons)):
	#concatenate the found boosted datasets to get them in one column
        #boosted_datasets_string='"'
        #for k in range(len(boosted_datasets[i])):
        #    if(k!=0):
        #        boosted_datasets_string+=','
        #    boosted_datasets_string+=boosted_datasets[i][k]
        #boosted_datasets_string+='"'
        if len(boosted_datasets[i])>0:
            boosted_datasets_string=str(boosted_datasets[i][0])
        else:
           boosted_datasets_string=""
        name = str(names[i]).split("/")[1]
        if "new_pmx" in names[i]:
            name = name+"_new_pmx"
        if "-v2" in names[i]:
            name = name+"_v2"
        #write the csv entry
        #print names[i]
        #print nevents[i]
        #print neg_fractions[i]
        #print xs
        #print weights[i]
        #print boosted_datasets_string
        #print globaltags[i]
        #print datatypes[i]
        #print generators[i]
        fobj_out.write(name+','+str(names[i])+','+str(nevents[i])+','+str(neg_fractions[i])+','+str(xs)+','+str(weights[i])+','+boosted_datasets_string+','+str(globaltags[i])+','+str(datatypes[i])+','+str(generators[i])+','+'NONE'+','+str(runs[i])+'\n')
        fobj_out.flush()

fobj_out.close
