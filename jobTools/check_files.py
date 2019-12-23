import glob
import os
import optparse
import sys

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
    #if not "nominal" in good_systs:
        #print "WARNING: no 'nominal' variation specified...adding it"
        #good_systs.insert(0,"nominal")

    #print "Systematic variations:"
    #for syst in good_systs:
        #print "  '"+syst+"'"

    return good_systs

def get_splitting_of_systematics(systematics,nvariations):
    systematics_numbers=[]
    systematics_=[]
    systematics_tmp=[]
    i=0
    k=1
    for systematic in systematics:
        systematics_tmp.append(systematic)
        i+=1
        if(i==nvariations):
            k+=1
            systematics_.append(systematics_tmp)
            systematics_numbers.append(k)
            i=0
            systematics_tmp=[]
    if len(systematics_tmp)>0:
        systematics_.append(systematics_tmp)
        systematics_numbers.append(k+1)
    return systematics_,systematics_numbers


parser = optparse.OptionParser("usage: %prog [options] sample1 sample2")

parser.add_option("-f", "--filespath", dest="files_path", type="string",help="Specify the base directory of the ntuples")
parser.add_option("-s", "--scriptspath", dest="scripts_path", type="string",help="Specify the base directory of the scripts")
parser.add_option("-n", "--nsysvars", dest="nsysvars", type="int",help="Number of JEC sources which were processed by the BoostedAnalyzer jobs. This has to be the same as was used during ntupling.")
parser.add_option("-j", "--jecfile", dest="jecfile",type="string",help="Specfiy the path to the txt file containing the JEC sources used for the ntupling. This has to be the same as was used during ntupling.")
parser.add_option("-d", "--data", dest="data",action="store_true",default=False,help="If this flag is given, you are looking at data, so only nominal ntuples are checked." )
parser.add_option("--nominal", dest = "nominal", action = "store_true", default = False,
    help = "activate if only nominal files")
parser.add_option("-o",dest="output",default = "scriptsToRerun.txt",
    help = "output path for resubmit file")
(options, args) = parser.parse_args()

if not options.files_path:
    parser.error('filespath not given, but is necessary')
if not options.scripts_path:
    parser.error('scriptspath not given, but is necessary')
if not options.nsysvars and not (options.data or options.nominal):
    parser.error('nsysvars not given, but is necessary')
if not options.jecfile and not (options.data or options.nominal):
    parser.error('jecfile not given, but is necessary')

files_path = os.path.abspath(options.files_path)
scripts_path = os.path.abspath(options.scripts_path)
nsystematicvariations = options.nsysvars  if not (options.data or options.nominal) else 1 #specifiy how many variations one job used, needs to be the same which was used in generate scripts
jec_file = os.path.abspath(options.jecfile) if not (options.data or options.nominal) else ""

print "\n"
print "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"
print "||| base path for ntuples: ",files_path," |||"
print "||| base path for scripts: ",scripts_path," |||"
print "||| jec sources file: ",jec_file," |||" 
print "||| number of JEC variations per boostedanalyzer job: ",nsystematicvariations," |||"
print "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"

#use this code snippet to find the samples in the scripts path automatically
print "\n"
samples = []
if len(args)==0:
    samples=[x[0] for x in os.walk(scripts_path)]
    del samples[0]
else:
    samples=args

#print samples
for i in range(len(samples)):
    samples[i]=os.path.basename(os.path.normpath(samples[i]))
print "samples: "
for sample in samples:
    print sample
print "\n"

#samples=[sample for sample in samples if sample.find("pythia")!=-1]
#use in case of jes/jer systematics in the systematicVariations file
if not (options.data or options.nominal): 
    systematics=get_list_of_systematics(jec_file)
    systematics_,systematics_numbers=get_splitting_of_systematics(systematics,nsystematicvariations)	
else:
    #use in case of data since there are no systematic variations
    systematics_=[["nominal"]]
    systematics_numbers=[1]

#use in case of you want to check slimmed ntuples
#systematics_=[["slimmed_ntuples"]]
#systematics_numbers=[1]
		
print "assignment between shell script numbering and processed systematic JEC variations"	
print systematics_numbers
print systematics_
print "\n"
#print systematics
redoList = []
for sample in samples:
    print "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    print ""
    print "looking at sample ##################", sample, " ##################"
    print ""
    for systematic_number,systematics in zip(systematics_numbers,systematics_):
        print "-----------------------------------------------------------------------------------"
        dirname = sample
        if (options.nominal or options.data): dirname += "_nominal"

        sample_sh=dirname+"/"+sample+"_*_"+str(systematic_number)+".sh"
        print "looking at systematics ",systematics
        print sample_sh
        #print "looking after ",os.path.join(scripts_path,sample_sh)
        scripts=glob.glob(os.path.join(scripts_path,sample_sh))
        #print scripts
        nscripts=len(scripts)
        #print "number of scripts is ",nscripts
        expected_nfiles=0
        sample_roots=[]
        script_numbers=[]
        for script in scripts:
            script_numbers.append(script.replace(os.path.join(scripts_path,dirname)+"/"+sample+"_","").replace("_"+str(systematic_number)+".sh",""))
        #print script_numbers
        for systematic in systematics:
            if(systematic=="nominal" or systematic=="slimmed_ntuples"):
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
            test=[]
            for variation in sample_root:
                #print "looking after ",os.path.join(files_path,variation)
                test+=glob.glob(os.path.join(files_path,variation))
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
            print "searching which files are missing ..."
            print "\n"
        missing_files=""
        n_missing_scripts = 0
        for number in script_numbers:
            missing_file=False
            #print number
            for files_,systematic in zip(files,systematics):
                if(systematic=="nominal" or systematic=="slimmed_ntuples"):
                    if not (os.path.join(files_path,sample)+"/"+sample+"_"+number+"_"+str(systematic)+"_Tree.root" in files_):
                        missing_file=True
                else:
                    if not ((os.path.join(files_path,sample)+"/"+sample+"_"+number+"_"+str(systematic)+"up_Tree.root" in files_) and (os.path.join(files_path,sample)+"/"+sample+"_"+number+"_"+str(systematic)+"down_Tree.root" in files_)):
                        missing_file=True
            if missing_file:
                n_missing_scripts+=1
                #print scripts_path+sample+"/"+sample+"_"+number+"_"+str(systematic_number)+".sh"
                missing_files+=" "+os.path.join(scripts_path,dirname)+"/"+sample+"_"+number+"_"+str(systematic_number)+".sh"
                
        print "Have to resubmit ", n_missing_scripts, " scripts."
        print(missing_files)
        for f in missing_files.split(" "):
            print(f)
            if f != "":
                redoList.append(f)

with open(options.output, "w") as f:
    f.write("\n".join(redoList))

print "#"*40
print "jobs to repeat"
print len(redoList)
print " ".join(redoList)
print ""
print "#"*40
print("wrote file to {}".format(options.output))
