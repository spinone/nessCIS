#!/usr/bin/env python

#python 3.9.5

"""NessCIS.py - a program to convert a Nessus Policy Audit compliance issues (CIS) export into a compact 5 column csv spreadsheet """

__author__ = 'Chris Rundle'
__version__ = '0.1'
__last_modification__ = '2021.10.05'

import re, sys, os.path

def usage(msg):
    print("[!] " + msg + "\n    Usage: nessCIS.py <raw_CIS_export_file.csv>\n")
    print("[>] Use nessCIS.py -help  for more help.")
 
def chkargs():
    global fn1
    if len(sys.argv)==1:
        usage("No filename supplied.")
        sys.exit()
    fn1=" ".join(sys.argv[1:])# handle filenames with spaces
    if fn1 in ('-help','--help','-h','--h'):
        showhelp()
    if fn1.find(".csv")<0:
        usage("File does not end '.csv'.")
        sys.exit()
    if not os.path.isfile(fn1):
        usage("File '" + fn1 + "' can't be found (check for typos).")
        sys.exit()
        
def logo():
    print("                              _________ .___  _________")
    print("    ____   ____   ______ _____\_   ___ \|   |/   _____/")
    print("   /    \_/ __ \ /  ___//  ___/    \  \/|   |\_____  \ ")
    print("  |   |  \\  ___/ \\___ \\ \\___\\ \\     \\___|   |/        \\")
    print("  |___|  /\___  >____  >____  >\______  /___/_______  /")
    print("       \/     \/     \/     \/        \/            \/ ")
    print(" >=- Nessus Policy Audit - Compliance Issues Filter -=<")
    print()

def showhelp():
    logo()
    print("[1] Run a (Credentialled) Nessus Policy Compliance Audit scan against the target(s).\n[2] (Optional) Select the Compliance Tab in the scan report and set a filter of 'Audit Severity' + 'is equal to' + 'FAILED' and click Apply.\n    Alternatively, set a filter of 'Audit Severity' + 'is not equal to' + 'PASSED' to extract all potential issues.\n[3] Select Report -> CSV from the menu bar. In the report settings, clear all checkboxes except 'Host' and 'Description' and click 'Generate Report'.\n[4] The file to be processed by nessCIS will be downloaded. Run Python nessCIS.py <path to file>")
    print("[5] Open the nessCIS output file in Excel and check it, then save it as .xlsx.\n[6] Import the Excel spreadsheet into an appendix in the report.\n[7] Add a vulnerability in the report called 'CIS Failures' and point the details to 'See Appendix X'\n")
    sys.exit()
       
def main():   
    global fn1
    if sys.version_info.major == 2:
        print("\n[!] Python v%s.%s detected."%(sys.version_info.major,sys.version_info.minor))
        print("[!] This script must be run using Python v3.7.x or higher.\n")
        sys.exit()
    chkargs()
    dt=fn1.replace('.csv','') + '-nessCIS.csv'
    logo()
    cm=","; dq='"'; vc=0; y2=-1
    h1="Host,Description,Status,Policy Value,Value Found\r\n"
    c=open(dt,"w", newline='\r\n') # End each output line with CRLF to mark CSV line end.
    c.write(h1.rstrip("\n"))
    print("[>] Scanning " + fn1 + "...")
    with open(fn1,mode='r',encoding='utf8',newline='\r\n') as f:
        for line in f:
            y=line.find("[FAILED]") # Set flag that a reportable issue has been found          
            y2=line.find("[WARNING]") # Comment these 3 lines out if  WARNINGS are not required
            if y2>y:
                y=y2 # Only going to happen if it's a WARNING, & not a FAILED

            # Only report flagged records
            if (y)>0:
                # isolate first and second fields (t1 & t2)
                t=line[0:y+10]
                z=t.find(cm)
                t1=(t[0:z].replace(cm," [comma]")).rstrip('\n')
                t2=(t[z+1:].replace(cm," [comma]")).rstrip('\n')
                t2=t2.replace(":",",") # split status off from t2               
                # Extract last two fields, including line breaks
                t=re.search(r'Policy Value:\n.*?\r\n', line, re.DOTALL).group()

                # Split into fields t3 & t4 
                # replace ',' with [comma] in each
                # and strip trailing line feeds & quotes
                z=t.find("Actual Value")
                t3=(t[0:z].replace(cm," [comma] ")).rstrip('\n')
                t4=(t[z:].replace(cm," [comma] ").rstrip('\n')).rstrip('"')
                
                # Assemble this record, prefacing t4 with a quote to retain line breaks
                text=t1+cm+t2+cm+t3+cm+dq+t4
                
                # Format record
                text=text.replace("\n\n","\n")          # Remove sequential line breaks
                text=text.replace("Policy Value:\n","") # Trim front of t3
                text=text.replace("Actual Value:\n",'') # Separate t3 & t4
                text=text.replace('"""','"')            # Remove triple quotes
                text=text.replace('""','"')             # Remove double quotes
                #text=text.replace("''","[not defined]")
                vc+=1 # increment record count
                y=0;y2=0 # reset flags
                c.write(text.rstrip("\n"))   
                
    print("[>] ...done.")
#   print("\nLast record:\n" + text) # [Console-based sanity check, if required]
    print("\n[*] Output saved as '" + dt + "' (" + str(vc) + " failures found)")

    f.close()
    c.close()
    
main()