import optparse
import os
import sys
import glob
import ROOT

pnfs = "/pnfs/desy.de/cms/tier2/store/user/"
naming = "ntuples_{syst}_Tree*.root"
local_naming = "{dataset}_*_{syst}_Tree.root"

parser = optparse.OptionParser()
parser.add_option("--local",dest="local",default=False,action="store_true",
    help = "activate if origin is not at pnfs but local directory")
parser.add_option("-i",dest="local_path",
    help = "path to local files if '--local' is used")
parser.add_option("-u","--username",dest="username",default="vanderli",
    help = "username directory at pnfs (cern username)")
parser.add_option("-t","--tag",dest="tag",default="KIT_ttzbb_sl_private_ntuples_2018",
    help = "output dataset tag given in crab config")
parser.add_option("-d","--dataset",dest="dataset",
    help = "dataset names (comma separated) as given in pnfs directories or local directory")
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
    systematics = [s.replace(" ","").replace("\n","") for s in systematics if not s == ""]
# add nominal
if not "nominal" in systematics:
    systematics = ["nominal"]+systematics


def getEntries(f):
    rf = ROOT.TFile(f,"READ")
    tree = rf.Get("MVATree")
    entries = int(tree.GetEntries())
    rf.Close()
    return entries


for dataset in opts.dataset.split(","):
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
                    continue

                # append file and number of entries to current list
                currentFiles.append(f)
                currentEntries+=entries

                # if number of events large enough write copy/hadd command
                if currentEntries >= int(opts.hadd_entries) or f == ntuplefiles[-1]:
                    currentOutName = outDataPath+"/"+outName.format(number=n, syst=systname)
                    # copying/hadding new file
                    if len(currentFiles) == 1:
                        cmd = "cp {} {}".format(currentFiles[-1], currentOutName)
                    else:
                        cmd = "hadd {} {}".format(currentOutName, " ".join(currentFiles))
                    
                    print("\n\033[1;31m{}\033[0m\n".format(cmd))
                    text = "1 : nevents : {} :".format(currentEntries)
                    if opts.do: 
                        os.system(cmd)
                        with open(currentOutName.replace(".root","_Cutflow.txt"), "w") as txtf:
                            txtf.write(text)
                    print("\n\t"+text+"\n")
                    currentFiles = []
                    currentEntries = 0
                    n+= 1
                    

                    



            
