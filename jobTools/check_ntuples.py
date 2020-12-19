import ROOT
import os
import sys
import optparse

parser = optparse.OptionParser()
parser.add_option("-j", "--joblist", dest = "joblist",
    help = "file with list of jobs to be checked")
parser.add_option("-o", "--outfile", dest = "outfile",
    default = "jobsToRerun.txt",
    help = "output file where jobs to rerun should be written")
(opts, args) = parser.parse_args()


with open(opts.joblist, "r") as jf:
    jobs = jf.readlines()

jobs=[x.replace("\n","") for x in jobs]
#print(jobs)


brokenFiles = []
emptyFiles = []
missingFiles = []
filesWithError = []

class JobInfo(object):
    brokenFiles = []
    emptyFiles  = []
    missingFiles = []
    def __init__(self, job):
        job = job.replace("\n","")
        with open(job, "r") as j:
            lines = j.readlines()
	#print(lines)
        for l in lines:
            l = l.replace("\n","").lstrip(' ')
            if l.startswith("cmsRun"):
                runCommand = l.split(" ")
                for command in runCommand:
                    if command.startswith("systematicVariations"):
                        self.variations = command.split("=")[1]
            if l.startswith("#meta"):
                l = l.replace("#meta ","")
                if l.startswith("nevents"):
                    self.nevents = l.split(" : ")[1]
                if l.startswith("cutflow"):
                    self.cutflow = l.split(" : ")[1]
                if l.startswith("check"):
                    self.outfile = l.split(" : ")[1]

        self.checkAttributes()
        self.treeEntries = []

    def checkAttributes(self):
        for attr in ["variations", "nevents", "cutflow", "outfile"]:
            if not hasattr(self, attr):
                print("error")
                print(attr)
                sys.exit()


    @property
    def variations(self):
        return self.__variations
    @variations.setter
    def variations(self, v):
        names = v.split(",")
        variations = []
        for n in names:
            if n == "nominal":
                variations.append(n)
            else:
                variations.append(n+"Up")
                variations.append(n+"Down")
        self.__variations = variations

    @property
    def nevents(self):
        return self.__nevents
    @nevents.setter
    def nevents(self, n):
        self.__nevents = int(n)

    @property
    def cutflow(self):
        cutflow = []
        for v in self.variations:
            cutflow.append(self.__cutflow.replace("_nominal_","_{}_".format(v)))
        return cutflow
    @cutflow.setter
    def cutflow(self, c):
        self.__cutflow = str(c)

    @property
    def outfile(self):
        outfile = []
        for v in self.variations:
            outfile.append(self.__outfile.replace("_nominal_","_{}_".format(v)))
        return outfile
    @outfile.setter
    def outfile(self, f):
        self.__outfile = str(f)

    def checkFiles(self):
        isGood = True
        rf = None
        for f in self.outfile:
            if not rf is None:
                rf.Close()

            if not os.path.exists(f):
                isGood = False
                print("missing file {}".format(f))
                missingFiles.append(f)
                continue

            rf = ROOT.TFile.Open(f)
            if rf is None or len(rf.GetListOfKeys()) == 0 or rf.TestBit(ROOT.TFile.kZombie):
                isGood = False
                print("broken file {}".format(f))
                brokenFiles.append(f)   
                continue

            if rf.TestBit(ROOT.TFile.kRecovered):
                isGood = False
                print("broken file {}".format(f))
                brokenFiles.append(f)
                continue
            
            tree = rf.Get("MVATree")
            if tree is None:
                isGood = False
                print("broken file {}".format(f))
                brokenFiles.append(f)
                continue

            nevts = tree.GetEntries()
            rf.Close()
            if nevts < 0:
                isGood = False
                print("broken file {}".format(f))
                brokenFiles.append(f)
                continue
            if nevts == 0:
                print("empty file {}".format(f))
                emptyFiles.append(f)

            self.treeEntries.append(int(nevts))

        if not rf is None:
            rf.Close()
        return isGood

    def checkEntries(self):
        isGood = True
        for c, treeEntry in zip(self.cutflow, self.treeEntries):
            if not os.path.exists(c):
                print("missing cutflow {}".format(c))
                isGood = False
                continue
            
            with open(c, "r") as cf:
                lines = cf.readlines()
            step, name, entries, integral = lines[0].split(" : ")
            if not int(entries) == self.nevents:
                isGood = False
                print("not the right number of entries in cutflow {}".format(c))
                print(int(entries), self.nevents)
                filesWithError.append(c.replace("Cutflow.txt", "Tree.root"))
                continue
            step, name, entries, integral = lines[-1].split(" : ")
            if not int(entries) == treeEntry:
                isGood = False
                print("not the right number of entries at the end of cutflow {}".format(c))
                print(int(entries), treeEntry)
                filesWithError.append(c.replace("Cutflow.txt", "Tree.root"))
                continue

        return isGood
            
            
             

jobsToRerun = []
for i, job in enumerate(jobs):
    job = job.replace("\n","")
    if i%100==0: print("{}/{} jobs checked".format(i, len(jobs)))
    j = JobInfo(job)
    if not j.checkFiles():
        jobsToRerun.append(job)
        print("need to rerun job {}".format(job))
        continue
    if not j.checkEntries():
        jobsToRerun.append(job)
        print("need to rerun job {}".format(job))
        continue

with open("brokenFiles.txt", "w") as f:
    f.write("\n".join(brokenFiles))
print("wrote brokenFiles.txt with {} entries".format(len(brokenFiles)))

with open("emptyFiles.txt", "w") as f:
    f.write("\n".join(emptyFiles))
print("wrote emptyFiles.txt with {} entries".format(len(emptyFiles)))

with open("errorFiles.txt", "w") as f:
    f.write("\n".join(filesWithError))
print("wrote errorFiles.txt with {} entries".format(len(filesWithError)))

with open(opts.outfile, "w") as f:
    f.write("\n".join(jobsToRerun))
print("wrote {} with {} entries".format(opts.outfile, len(jobsToRerun)))

