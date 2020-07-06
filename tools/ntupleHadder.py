import optparse
import os
import sys
import glob
import ROOT
import pprint

pnfs = "/pnfs/desy.de/cms/tier2/store/user/"
naming = "ntuples_{syst}_Tree*.root"
local_naming = "{dataset}_*_{syst}_Tree.root"

usage = "\n\nExample:\npython ntupleHadder.py --local -i /ABSOLUTE/PATH/TO/INPUT/DIRECTORY -o /ABSOLUTE/PATH/TO/OUTPUT/DIRECTORY -s RELATIVE/PATH/TO/SYSTEMATIC/FILE.txt --hadd 10000 --do DATASETS\n"

parser = optparse.OptionParser(usage=usage)
pnfsOpts = optparse.OptionGroup(parser, "PNFS options", "Options to set path to pnfs as 'PNFSBASEDIR/USERNAME/DATASET/TAG/*/*/NAMING'. NAMING is set in file.")
pnfsOpts.add_option("-u","--username",dest="username",default="vanderli",
    help = "username directory at pnfs (cern username)")
pnfsOpts.add_option("-t","--tag",dest="tag",default="KIT_ttzbb_sl_private_ntuples_2018",
    help = "output dataset tag given in crab config")
parser.add_option_group(pnfsOpts)

parser.add_option("--local",dest="local",default=False,action="store_true",
    help = "activate if origin is not at pnfs but local dust directory")
parser.add_option("-i",dest="local_path",
    help = "path to local files if '--local' is used")

parser.add_option("-o","--output",dest="outPath",
    help = "output path to where ntuples are written")
parser.add_option("-s","--systematics",dest="systematics",
    help = "file with systematics listed")
parser.add_option("--hadd",dest="hadd_entries",default=-1,
    help = "minimum number of entries per file")
parser.add_option("--do",dest="do",default=False,action="store_true",
    help = "start")
(opts, args) = parser.parse_args()

# check output directory
if not os.path.exists(opts.outPath):
    sys.exit("output path does not exist")

# managing systematics
with open(opts.systematics, "r") as f:
    systematics = f.readlines()
    systematics = [s.replace(" ","").replace("\n","").replace("\t","") for s in systematics]
    systematics = [s for s in systematics if not (s == "" or s.startswith("#"))]
# add nominal
if not "nominal" in systematics:
    systematics = ["nominal"]+systematics
print(systematics)


def getEntries(f):
    rf = ROOT.TFile(f,"READ")
    tree = rf.Get("MVATree")
    entries = int(tree.GetEntries())
    rf.Close()
    return entries

def mergeCutflows(files):
    first = True
    for filename in files:
        numbers=[]
        steps=[]
        nevents=[]
        yields=[]
        f = open(filename)
        lines=f.read().splitlines()
        if first:
            nlines=len(lines)
        else:
            if len(lines)!=nlines:
                print 'file', filename,'has wrong number of lines (',len(lines),')'
                break
        for line in lines:        
            linelist=line.split(' : ')
            numbers.append(linelist[0])
            steps.append(linelist[1])
            nevents.append(int(linelist[2]))
            yields.append(float(linelist[3]))
        if first:       
            sumlist=list(nevents)
            yieldlist=list(yields)
            first=False
        else:
            sumlist = [sum(x) for x in zip(sumlist, nevents)]
            yieldlist = [sum(x) for x in zip(yieldlist, yields)]
        f.close()
        text = ""
    for a,b,c,d in zip(numbers,steps,sumlist,yieldlist):
        text += str(a)+" : "+str(b)+" : "+str(c)+" : "+str(d)+"\n"
    return text

failedjobs = []
for dataset in args:
    print("\n\n"+"="*50)
    print("handling dataset {}".format(dataset))

    outDataPath = opts.outPath+"/"+dataset
    if os.path.exists(outDataPath):
        iterator = 1
        while os.path.exists(outDataPath+"_"+str(iterator)): iterator += 1
        outDataPath = outDataPath+"_"+str(iterator)
    if opts.do:
        os.makedirs(outDataPath)
        print("generated directory {}".format(outDataPath))

    if opts.local:
        localPath   = opts.local_path+"/"+dataset+"/"+local_naming
    else:
        pnfsPath    = pnfs+"/"+opts.username+"/"+dataset+"/"+opts.tag+"/*/*/"+naming
    outName     = dataset+"_{number}_{syst}_Tree.root"
   
    # loop over all systematics
    for syst in systematics:
        if syst == "nominal": systnames = ["nominal"]
        else: systnames = [syst+"up", syst+"down"]
        for systname in systnames:
            print("\n\t:::::::::::::::::::::::::::::::::::::::::::::")
            print("\tcollecting systematic {}".format(systname))
            if opts.local:
                print("\t"+localPath.format(dataset=dataset,syst=systname))
                ntuplefiles = glob.glob(localPath.format(dataset=dataset,syst=systname))
            else:
                print("\t"+pnfsPath.format(syst=systname))
                ntuplefiles = glob.glob(pnfsPath.format(syst=systname))
            print("\tnumber of files found: {}".format(len(ntuplefiles)))        

            n = 1
            currentFiles = []
            currentEntries = 0
            for f in ntuplefiles:
                entries = getEntries(f)
                if entries == 0: 
                    print("\tEMPTY: {}".format(os.path.basename(f)))
                else:
                    # append file and number of entries to current list
                    currentFiles.append(f)
                    currentEntries+=entries

                # if number of events large enough write copy/hadd command
                if currentEntries >= int(opts.hadd_entries) or f == ntuplefiles[-1]:
                    currentOutName = outDataPath+"/"+outName.format(number=n, syst=systname)
                    # copying/hadding new file
                    if len(currentFiles) == 0:
                        continue
                    elif len(currentFiles) == 1:
                        cmd = "cp {} {}".format(currentFiles[-1], currentOutName)
                    else:
                        cmd = "hadd {} {}".format(currentOutName, " ".join(currentFiles))
                    
                    print("\n\033[1;31m{}\033[0m\n".format(cmd))

                    currentCutflows=[f.replace("_Tree","_Cutflow").replace(".root",".txt") for f in currentFiles]
                    text = mergeCutflows(currentCutflows)
                    if opts.do: 
                        os.system(cmd)
                        if getEntries(currentOutName) != currentEntries:
                            print("WARNING # Events doesn't match up")
                            print("Current Entries: {0} CurrentOutname: {1}".format(currentEntries,getEntries(currentOutName)))
                            failedjobs.append({dataset:systname})
                        with open(currentOutName.replace(".root","_Cutflow.txt"), "w") as txtf:
                            txtf.write(text)
                    print("\n\t"+text+"\n")
                    # print("Current Entries {}".format(currentEntries))
                    currentFiles = []
                    currentCutflows = []
                    currentEntries = 0
                    n+= 1

print("#"*50)
print("Following hadds were problematic: ")
for i in failedjobs:
    pprint.pprint(i)                  
print("#"*50)

                    



            

