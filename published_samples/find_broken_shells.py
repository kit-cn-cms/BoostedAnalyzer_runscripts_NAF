import os
import optparse
import NAFSubmit

parser = optparse.OptionParser()
parser.add_option("-j","--joblist",dest="joblist",default="joblist.txt",
    help = "joblist file which contains paths to all shell scripts")
parser.add_option("-p","--path",dest="jobpath",default="../",
    help = "path to shell scripts in joblist relative to current location or absolute")
parser.add_option("-b","--brokenfiles",dest="brokenfiles",default="broken_files.txt",
    help = "broken files file which contains paths to all broken root files")
parser.add_option("--submit", "-s", dest = "submit", default = False, action = "store_true",
    help = "activate submissin of shell files")
parser.add_option("-d","--dir",dest="dir",default="./",
    help = "path to directory where logs for submit should be created")
parser.add_option("-n", "--name", dest = "name", default="resubmit",
    help = "name of submit")
(opts, args) = parser.parse_args()

# set abspaths
if not os.path.isabs(opts.jobpath):
    opts.jobpath = os.path.abspath(opts.jobpath)
if not os.path.isabs(opts.dir):
    opts.dir = os.path.abspath(opts.dir)

# loading jobs
with open(opts.joblist, "r") as f:
    jobs = f.readlines()
jobs = [opts.jobpath+"/"+j.replace("\n","") for j in jobs]

# loading broken files
with open(opts.brokenfiles, "r") as f:
    broken = f.readlines()
#print("number of unique broken files: {}".format(len(broken)))

# gather nominal root files
brokenfiles = []
for b in broken:
    b = b.replace("\n","")
    if not b.endswith("_Tree.root"):
        print("{} not a valid root file name - skip".format(b))
        continue
    brokenfiles.append(b)

# remove doubles
brokenfiles = list(set(brokenfiles))
print("number of broken files: {}".format(len(brokenfiles)))

# loop over jobs
job_translation = {}
print("looping over jobs")
for i,job in enumerate(jobs):
    if i%1000 == 0: print("job #{}/{}".format(i, len(jobs)))

    # open shell file
    with open(job, "r") as sf:
        lines = sf.readlines()
    rootfile = None
    for l in lines:
        if "#meta check" in l:
            rootfile = l.split(" : ")[-1].replace("\n","")
        if "systematicVariations" in l:
            variations = l.split("systematicVariations=")[-1].split(" ")[0].split(",")
            #print(variations)
    if not rootfile:
        print("shell file {} does not contain 'meta check' line".format(job))
        continue
    elif not rootfile.endswith(".root"):
        print("{} is not a rootfile in shellscript {}".format(rootfile, job))
        continue

    while "//" in rootfile:
        rootfile = rootfile.replace("//","/")

    for var in variations:
        if var == "nominal":
            names = [rootfile]
        else:
            key = rootfile.split("_")[-2]
            names = [rootfile.replace("_"+key+"_","_"+var+"up_"), rootfile.replace("_"+key+"_","_"+var+"down_")]
        for n in names:
            if n in job_translation:
                print("already in file list: {}".format(n))
                
            job_translation[n] = job

failed_jobs = []
missing = []
for b in brokenfiles:
    if b in job_translation:
        failed_jobs.append(job_translation[b])
    else:
        print("could not find {} in job_translation map".format(b))
        missing.append(b)


print("\n\n\nall failed jobs were identified:")
print("\n".join(list(set(failed_jobs))))

if len(missing) > 0:
    print("\n\n\nnot all broken root files found a corresponding shell script...")
    print("\n".join(missing))

print("\n\n\ntotal failed: {}".format(len(brokenfiles)))
print("failed indentified: {}".format(len(failed_jobs)))
print("unique shell scripts: {}".format(len(list(set(failed_jobs)))))
print("still missing: {}".format(len(missing)))
failed_jobs = list(set(failed_jobs))

if opts.submit:
    new_logdir = opts.dir
    new_logdir = new_logdir+"/{}/".format(opts.name)
    print(new_logdir)
    if not os.path.exists(new_logdir):
        os.makedirs(new_logdir)
    NAFSubmit.submitToBatch(new_logdir, failed_jobs, name_ = opts.name)

