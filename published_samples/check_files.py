import glob
import os

def get_list_of_systematics(filename):
    systs=[]
    with open(filename,"r") as f:
        systs=f.readlines()
    systs=[s.rstrip('\n') for s in systs]
    systs=[s.rstrip('\t') for s in systs]
    good_systs=[s for s in systs if not (s.startswith("#") or len(s)==0)]
    if len(good_systs) != len(set(good_systs)):
        #print "ERROR specifying list of systematics: DUPLICATE ENTRIES"
        sys.exit()
    if not "nominal" in good_systs:
        #print "WARNING: no 'nominal' variation specified...adding it"
        good_systs.insert(0,"nominal")

    #print "Systematic variations:"
    #for syst in good_systs:
        #print "  '"+syst+"'"

    return good_systs

def get_splitting_of_systematics(systematics,nvariations):
    systematics_numbers=[]
    systematics_=[]
    systematics_tmp=[]
    i=0
    k=0
    for systematic in systematics:
            systematics_tmp.append(systematic)
            i+=1
            if(i==nvariations):
                    k+=1
                    systematics_.append(systematics_tmp)
                    systematics_numbers.append(k)
                    i=0
                    systematics_tmp=[]
    systematics_.append(systematics_tmp)
    systematics_numbers.append(k+1)
    return systematics_,systematics_numbers




files_path="/nfs/dust/cms/user/mwassmer/DarkMatter/ntuples/"
scripts_path="/nfs/dust/cms/user/mwassmer/DarkMatter/BoostedAnalyzer_runscripts_NAF/published_samples/MonoJet_skims_alternative/"
nsystematicvariations=5 #specifiy how many variations one job used, needs to be the same which was used in generate scripts

#use this code snippet to find the samples in the scripts path automatically

samples=[x[0] for x in os.walk(scripts_path)]
del samples[0]
#print samples
for i in range(len(samples)):
    samples[i]=samples[i].replace(scripts_path,"")
#print samples

# or check for specific datasets
#samples=["WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]
samples=[sample for sample in samples if sample.find("MET")!=-1]
print samples
#systematics=get_list_of_systematics("systematicVariations_used.txt")
#systematics_,systematics_numbers=get_splitting_of_systematics(systematics,nsystematicvariations)	

#use in case of data since there are no systematic variations
systematics_=[["nominal"]]
systematics_numbers=[1]
		
#print systematics	
print systematics_numbers
print systematics_	
#print systematics

for sample in samples:
    print "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    print "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    print ""
    print "looking at sample ##################", sample, " ##################"
    print ""
    for systematic_number,systematics in zip(systematics_numbers,systematics_):
		sample_sh=sample+"/"+sample+"_*_"+str(systematic_number)+".sh"
		print "looking at systematics ",systematics
		scripts=glob.glob(scripts_path+sample_sh)
		#print scripts
		nscripts=len(scripts)
		#print "number of scripts is ",nscripts
		expected_nfiles=0
		sample_roots=[]
		script_numbers=[]
		for script in scripts:
			script_numbers.append(script.replace(scripts_path+sample+"/"+sample+"_","").replace("_"+str(systematic_number)+".sh",""))
		#print script_numbers
		for systematic in systematics:
			if(systematic=="nominal"):
				sample_roots.append([sample+"/"+sample+"_*_"+str(systematic)+"_Tree.root"])
				expected_nfiles+=nscripts
			else:
				sample_roots.append([sample+"/"+sample+"_*_"+str(systematic)+"up_Tree.root",sample+"/"+sample+"_*_"+str(systematic)+"down_Tree.root"])
				expected_nfiles+=nscripts*2
		print "number of expected files is ",expected_nfiles
		#print scripts
		#files=glob.glob(files_path+sample_root)
		nfiles=0
		files=[]
		for sample_root in sample_roots:
			#print files_path+sample_root
			test=[]
			for variation in sample_root:
				test+=glob.glob(files_path+variation)
			#print test
			files.append(test)
			nfiles+=len(test)
		print "number of files is ",nfiles
		#print files
		
		if(nfiles==expected_nfiles):
		    print "all files are there"
		    continue
		else:
		    print "number of scripts does not correspond to the number of files"
		    print "searching which files are missing"
		missing_files=""	
		for number in script_numbers:
			missing_file=False
			#print number
			for files_,systematic in zip(files,systematics):
				if(systematic=="nominal"):
					if not (files_path+sample+"/"+sample+"_"+number+"_"+str(systematic)+"_Tree.root" in files_):
						missing_file=True
				else:
					if not ((files_path+sample+"/"+sample+"_"+number+"_"+str(systematic)+"up_Tree.root" in files_) and (files_path+sample+"/"+sample+"_"+number+"_"+str(systematic)+"down_Tree.root" in files_)):
						missing_file=True
			if missing_file:
				#print scripts_path+sample+"/"+sample+"_"+number+"_"+str(systematic_number)+".sh"
				missing_files+=" "+scripts_path+sample+"/"+sample+"_"+number+"_"+str(systematic_number)+".sh"
                
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print " "
		print "copy this string in sup.py to resubmit the missing jobs"
		print " "
		print missing_files
		print " "
		print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		print "resubmitting ..."
		os.system("python sup.py "+missing_files)
