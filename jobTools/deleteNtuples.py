import optparse
import os


parser = optparse.OptionParser("usage: %prog [options] ")

parser.add_option(
    "-f",
    "--file",
    dest="file",
    type="string",
    default="broken_files.txt",
    help="Specify an file containing all broken Ntuple to delete, default = broken_files.txt"
)

(options, args) = parser.parse_args()


with open(options.file,"r") as errorFile:
    for line in errorFile:
        print("deleting {}".format(line))
        os.remove(line.rstrip("\n")) 

