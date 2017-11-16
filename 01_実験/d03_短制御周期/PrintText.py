#win32guiをインストールのこと

import tempfile
import win32api
import win32print
import time

#filename = tempfile.mktemp ("test.txt")
filename = r"C:\Users\p000495138\Desktop\GriC3_短制御周期\test_text.txt"

def print_Gri(filename):
    open (filename, "r")
    #open (filename, "w").write ("This is a test")
    win32api.ShellExecute (
      0,
      "print",
      filename,
      #
      # If this is None, the default printer will
      # be used anyway.
      #
      '/d:"%s"' % win32print.GetDefaultPrinter (),
      ".",
      0
    )

def planepaper():
    #%JOB1
    print("JOB1")
    for i in range(15):
        print_Gri(filename)
    
    #%JOB2
    time.sleep(35)
    print("JOB2")    
    for i in range(15):
        print_Gri(filename)
    
    #%JOB3
    time.sleep(39)
    print("JOB3")    
    for i in range(15):
        print_Gri(filename)
    
    #%JOB4
    time.sleep(60)
    print("JOB4")    
    for i in range(15):
        print_Gri(filename)
        
    #%JOB5
    time.sleep(300)
    print("JOB5")    
    for i in range(15):
        print_Gri(filename)
#%%
def thickpaper():
    #%JOB1
    print("JOB1")
    for i in range(15):
        print_Gri(filename)
    
    #%JOB2
    time.sleep(70)
    print("JOB2")    
    for i in range(15):
        print_Gri(filename)
    
    #%JOB3
    time.sleep(100)
    print("JOB3")    
    for i in range(15):
        print_Gri(filename)
    
    #%JOB4
    time.sleep(300)
    print("JOB4")    
    for i in range(15):
        print_Gri(filename)
#%%
planepaper()