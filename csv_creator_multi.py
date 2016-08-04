#usage type: python csv_creator_multi.py dataset.csv
import csv
import sys
import csv_helper_multi as chm

fobj = open(sys.argv[1],"rb")

reader=csv.reader(fobj)
csv_array=[]
for row in reader:
    csv_array.append(row)
fobj.close()


fobj_out=open("auto_samples.csv","w")
fobj_out.write('name,dataset,nGen,Npos-Nneg/Ntotal,XS,weight,boosted_dataset,globalTag,IsData,generator,additionalSelection,isreHLT'+'\n')

for row in csv_array:
    print "getting names for ...",row[1]
    names=chm.get_names(row[1])
    if(len(names)==0):
      continue
    #print "############################ names ################################"
    #print names
    print "getting jsons for corresponding datasets ..."
    jsons=chm.get_jsons(names)
    #print "############################ jsons ################################"
    #print jsons
    print "getting event numbers ..."
    nevents=chm.get_nevents(jsons)
    #print "############################ nevents ################################"
    #print nevents
    print "getting number of files ..."
    nfiles=chm.get_nfiles(jsons)
    """
    n_toosmall=0
    for i in range(len(nfiles)):
        if(nfiles[i]<100):
	    n_toosmall+=1
    for k in range(n_toosmall):
	for l in range(len(nfiles)):
	    if(nfiles[l]<100):
		nfiles.pop(l)
		jsons.pop(l)
		nevents.pop(l)
		names.pop(l)
		break
    """
    #print "############################ nfiles ################################"
    #print nfiles
    print "getting datatype mc or data ..."
    datatypes=chm.get_datatypes(jsons)
    #print "############################ datatypes ################################"
    #print datatypes
    print "getting globaltags ..."
    globaltags=chm.get_globaltags(jsons)
    #print "############################ globaltags ################################"
    #print globaltags
    print "getting generators ..."
    generators=chm.get_generators(jsons)
    #print "############################ generators ################################"
    #print generators
    print "getting boosted datasets ..."
    boosted_datasets=chm.get_children_names_(names)
    #print "############################ boosted datasets ################################"
    #print boosted_datasets
    print "getting negative event fractions ..."
    neg_fractions=chm.get_xs(names)
    #print "########################### neg event fractions #########################"
    #print neg_fractions
    print "getting weights ..."
    weights=chm.get_weights(nevents,neg_fractions,float(row[2]))
    #print "############################ weights ################################"
    #print weights
    duplicates_array=chm.merge_ext(names)
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
      boosted_datasets_tmp=[]
      for i in range(len(duplicate)):
	dupl_position=duplicate[i]
	dupls.append(dupl_position)
	#print dupl_position
	nevents_tmp+=nevents[dupl_position]
	nfiles_tmp+=nfiles[dupl_position]
	neg_fractions_tmp+=neg_fractions[dupl_position]
	boosted_datasets_tmp+=boosted_datasets[dupl_position]
	if(i==0):
	  names_tmp+=names[dupl_position]
	else:
	  names_tmp+=","+names[dupl_position]
      names_tmp+='"'
      neg_fractions_tmp=neg_fractions_tmp/len(duplicate)
      weights_tmp=float(row[2])*1000/(neg_fractions_tmp*nevents_tmp)
      #print nevents_tmp,nfiles_tmp,neg_fractions_tmp,weights_tmp,boosted_datasets_tmp,names_tmp
      names.append(names_tmp)
      jsons.append(jsons_tmp)
      nevents.append(nevents_tmp)
      nfiles.append(nfiles_tmp)
      datatypes.append(datatypes_tmp)
      globaltags.append(globaltags_tmp)
      generators.append(generators_tmp)
      boosted_datasets.append(boosted_datasets_tmp)
      neg_fractions.append(neg_fractions_tmp)
      weights.append(weights_tmp)
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
      del neg_fractions[i]
      del weights[i]
    #print "names new "
    #print names

    xs=float(row[2])
    print "writing found datasets and their information ..."
    fobj_out.write(",,,,,,,,,,,"+'\n')
    # loop over all the datasets which fit to the dataset with wildcards
    for i in range(len(jsons)):
	#concatenate the found boosted datasets to get them in one column
        boosted_datasets_string='"'
        for k in range(len(boosted_datasets[i])):
            if(k!=0):
                boosted_datasets_string+=','
            boosted_datasets_string+=boosted_datasets[i][k]
        boosted_datasets_string+='"'
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
        #print "test"
        fobj_out.write(str(row[0])+','+str(names[i])+','+str(nevents[i])+','+str(neg_fractions[i])+','+str(xs)+','+str(weights[i])+','+boosted_datasets_string+','+str(globaltags[i])+','+str(datatypes[i])+','+str(generators[i][0])+','+'none'+','+'isreHLT'+'\n')

fobj_out.close
