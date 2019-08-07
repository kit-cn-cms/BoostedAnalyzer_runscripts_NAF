import ROOT
import sys
import glob
from multiprocessing import Pool
from tqdm import *
import os

class DevNull:
    def write(self, msg):
        pass

def checkROOTFiles(path=""):
    isGOOD=True
    isEMPTY=False
    rf=ROOT.TFile.Open(path)
    if rf==None or len(rf.GetListOfKeys())==0 or rf.TestBit(ROOT.TFile.kZombie):
        isGOOD=False
        print "BROKEN        ", path
    elif rf.TestBit(ROOT.TFile.kRecovered):
        isGOOD=False
        print "BROKEN        ", path
    else:
        tree=rf.Get("MVATree")
        if tree==None:
            isGOOD=False
            print "BROKEN        ", path
        else:    
            nevents=tree.GetEntries()
            rf.Close()
            if nevents==0:
                isEMPTY=True
                print "EMTPY        ", path
            elif nevents<0:
                isGOOD=False
		print "BROKEN        ", path
    if rf!=None:
        rf.Close()
    if isEMPTY: return "empty"
    if isGOOD:  return "good"
    else:       return "broken"
    
    return isGOOD


def checkROOTFiles_(path=""):
    isGOOD=True
    isEMPTY=False
    rf=ROOT.TFile.Open(path)
    if rf==None or len(rf.GetListOfKeys())==0 or rf.TestBit(ROOT.TFile.kZombie):
        isGOOD=False
        print "BROKEN        ", path
    elif rf.TestBit(ROOT.TFile.kRecovered):
        isGOOD=False
        print "BROKEN        ", path
    else:
        tree=rf.Get("MVATree")
        if tree==None:
            isGOOD=False
            print "BROKEN        ", path
        else:    
            nevents=tree.GetEntries()
            rf.Close()
            if nevents==0:
                isEMPTY=True
                # print "EMTPY        ", path
            elif nevents<0:
                isGOOD=False
		print "BROKEN        ", path
    if rf!=None:
        rf.Close()
    # if isEMPTY: return "empty"
    # if isGOOD:  return "good"
    if not isEMPTY and not isGOOD:
        return path
    else:
        return ""

# _stderr = sys.stderr
# null = open(os.devnull,'wb')
# sys.stderr = null

# out = io.StringIO()
# err = io.StringIO()

brokenFiles=[]
emptyFiles=[]
indirs=sys.argv[1:]
print(indirs)

fileList=[]

print("#"*40)
print("checking following directories ")
print("#"*40)
for dir_ in indirs:
    print(dir_)
    if "*" in dir_:
        fileList+=glob.glob(dir_)
    else:
        fileList+=glob.glob(dir_+"/*.root")
# print(fileList)

print("#"*40)
print("checking {0} rootfiles ".format(len(fileList)))
print("#"*40)

def imap_unordered_bar(func, args, n_processes = 8):
    p = Pool(n_processes)
    res_list = []
    # with redirect_stdout(out), redirect_stderr(err):
    with tqdm(total = len(args)) as pbar:
        for i, res in tqdm(enumerate(p.imap_unordered(func, args))):
            pbar.update()
            res_list.append(res)
    pbar.close()
    p.close()
    p.join()
    return res_list

brokenFiles = imap_unordered_bar(checkROOTFiles_, fileList)
print("{0} files broken".format(len(brokenFiles)))
brokenCounter = 0
with open("broken_files.txt", "w") as f:
    for file in brokenFiles:
        # print(file)
        if file == '':
            continue
        # f.write("\n".join(brokenFiles))
        f.write(file+"\n")
        brokenCounter+=1
with open("empty_files.txt", "w") as f:
    f.write("\n".join(emptyFiles))

print("{0} files broken".format(brokenCounter))

