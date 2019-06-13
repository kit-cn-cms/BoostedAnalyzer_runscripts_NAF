import optparse
import glob
import os
import NAFSubmit

parser = optparse.OptionParser()
parser.add_option("-l", "--logdir", dest = "logdir",
    help = "path to directory with logfiles")
parser.add_option("-d", "--dir", dest = "dir",
    help = "directory of shell files as written in .out files")
parser.add_option("--submit", "-s", dest = "submit", default = False, action = "store_true",
    help = "activate submissin of shell files")
parser.add_option("-n", "--name", dest = "name",
    help = "name of submit")
(opts, args) = parser.parse_args()


errorfiles = glob.glob(opts.logdir+"/*.err")



def grep_segval(logfile):
    with open(logfile, "r") as f:
        if "segmentation violation" in f.read():
            return True
    return False

def grep_shellscript(logfile):
    with open(logfile.replace(".err",".out")) as f:
        shell_line = f.readlines()[1]
    return shell_line.replace("\n","")

resubmit_shells = []
for f in errorfiles:
    if grep_segval(f):
        resubmit_shells.append(grep_shellscript(f))

unique_files = list(set(resubmit_shells))
print("NUMBER OF SHELLS WITH SEGMENTATION VIOLATION: {}".format(len(unique_files)))

unique_files = [opts.dir+"/"+f for f in unique_files]
for f in unique_files: print(f)


if opts.submit:
    new_logdir = opts.dir
    new_logdir = new_logdir+"/resubmit/"
    print(new_logdir)
    if not os.path.exists(new_logdir):
        os.makedirs(new_logdir)
    NAFSubmit.submitToBatch(new_logdir, unique_files, name_ = opts.name)
