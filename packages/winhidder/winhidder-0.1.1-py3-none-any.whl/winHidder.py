import os
import subprocess



def run():
    print("starting winHidder")
    dirname = os.path.dirname(__file__)
    p = os.path.join(dirname, "winHidder.exe")
    subprocess.Popen([p])
    #os.system(p)
    #input()
    print("started winHidder")
    