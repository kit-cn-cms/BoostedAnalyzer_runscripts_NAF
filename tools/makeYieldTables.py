import sys
from subprocess import call
from datetime import date

def write_syst(file,value):
    file.write(value[0]+' &')
    for val in value[1:]:
      file.write(val+" &")
    file.write('\\\\ \n')

def write_foot(file):
    file.write('\\hline\n')
    file.write('\end{tabular}\n')
    file.write('\\end{center}\n')

def write_head(file,columns):
    #print columns
    file.write('\\begin{center}\n')
    file.write('\\begin{tabular}{l')
    for entry in columns[1:]:
        file.write('c')
    file.write('}\n')
    file.write('\\hline\n')
    for entry in columns[:-1]:
        file.write(entry+' &')
    file.write(columns[-1]+' \\\\ \n')
    file.write('\\hline\n')




##begin script 
if len(sys.argv)<=2:
  print "usage:"
  print "python makeYieldTables.py OUPUTFILE_WITHOUT_EXTENSION LIST_OF_INPUT_CUTFLOWS"
  exit(0)

first=True
samples=[]
suffixes=["MC_MadGraph_","MC_aMCatNLO_"]
affixes=["_nominal_Cutflow.txt","_JESDOWN_Cutflow.txt","_JESUP_Cutflow.txt"]
outfile = sys.argv[1]
for filename in sys.argv[2:]:
  sample=[]
  steps=[]
  nGen=[]
  yields=[]
  lines=[]
  infile=open(filename,"r")
  rawlines=list(infile)
  for rawline in rawlines:
    rawline=rawline.replace("\n","")
    lines.append(rawline)
  #print filename
  samplename=filename.rsplit("/",1)[1]
  for suffix in suffixes:
    if suffix in samplename:
      samplename=samplename.replace(suffix,"")
  for affix in affixes:
    if affix in samplename:
      samplename=samplename.replace(affix,"")
  #print samplename
  sample.append(samplename)
  for line in lines:
    print line
    splitline=line.split(" : ")
    steps.append(splitline[1])
  for line in lines:
    splitline=line.split(" : ")
    nGen.append(splitline[2])
  for line in lines:
    splitline=line.split(" : ")
    yields.append(splitline[3])
  sample.append(steps)
  sample.append(nGen)
  sample.append(yields)
  print sample
  samples.append(sample)

#print samples

for sample in samples:
  if len(sample[1])!=len(samples[0][1]):
    print sample[0], " has the wrong number of cutflow steps"
    exit(1)

out=open(outfile+"_events.tex","w")
out.write( '\\documentclass{article}\n')
out.write( '\\begin{document}')
s=[]
for sample in samples:
  s.append(sample[0])
#print s
write_head(out,["cutflow steps"]+s)
for step in samples[0][1]:
  line=[]
  line.append(step)
  i=samples[0][1].index(step)
  for s in samples:
    line.append(s[2][i])
  write_syst(out,line)
write_foot(out)
out.write("\\end{document}")
out.close()

call(["pdflatex","-interaction","batchmode",outfile+"_events.tex"])
call(["pdftopng",outfile+"_events.pdf",outfile+"_events.png"])
print "did the table for the number of events"


out=open(outfile+"_yields.tex","w")
out.write( '\\documentclass{article}\n')
out.write( '\\begin{document}')
s=[]
for sample in samples:
  s.append(sample[0])
#print s
write_head(out,["cutflow steps"]+s)
for step in samples[0][1]:
  line=[]
  line.append(step)
  i=samples[0][1].index(step)
  for s in samples:
    print s
    line.append(s[3][i])
  write_syst(out,line)
write_foot(out)
out.write("\\end{document}")
out.close()

call(["pdflatex","-interaction","batchmode",outfile+"_yields.tex"])
call(["pdftopng",outfile+"_yields.pdf",outfile+"_yields.png"])
print "did the table for the yields"






















