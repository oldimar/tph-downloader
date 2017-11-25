#!/usr/bin/python3

import os
import sys
import re
import subprocess as sp

def getNumericValue(s):
  return (float(re.sub('\.full.pdf','',s)))

for ano in sys.argv[1:]:
  edicoes=os.listdir(ano)
  for edicao in edicoes:
    volume=int(ano)
    if volume>2:
      ano_i = volume+1978
    else:
      ano_i = volume+1977
      if volume == 2 and int(edicao)>1:
        ano_i = 1980
      if volume == 1 and int(edicao)>1:
        ano_i = 1979

    files=os.listdir(os.path.join(ano,edicao))
    files.sort(key=getNumericValue)
    files = [ os.path.join(ano,edicao,f) for f in files]
    command = ['pdfunite']
    command.extend(files)
    command.append(str(ano_i)+"-"+str(volume)+"-"+edicao+".pdf")
    print(str(ano_i)+"-"+str(volume)+"-"+edicao+".pdf")
#    print(command)
    sp.run(command)
