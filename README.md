# nessCIS
A Python 3 program to convert a CSV export from a Nessus Policy Audit's compliance issues (CIS) into a compact 5 column csv spreadsheet

NessCIS.py - a Python 3 program to convert a CSV export from a Nessus Policy Audit's compliance issues (CIS) into a compact 5 column csv spreadsheet

[!] Usage: nessCIS.py <raw_CIS_export_file.csv>
[>] Use nessCIS.py --help  for more help.

nessCIS.py --help
                              _________ .___  _________
    ____   ____   ______ _____\_   ___ \|   |/   _____/
   /    \_/ __ \ /  ___//  ___/    \  \/|   |\_____  \
  |   |  \  ___/ \___ \ \___\ \     \___|   |/        \
  |___|  /\___  >____  >____  >\______  /___/_______  /
       \/     \/     \/     \/        \/            \/
 >=- Nessus Policy Audit - Compliance Issues Filter -=<

[1] Run a (Credentialled) Nessus Policy Compliance Audit scan against the target(s).
[2] (Optional) Select the Compliance Tab in the scan report and set a filter of 'Audit Severity' + 'is equal to' + 'FAILED' and click Apply.
    Alternatively, set a filter of 'Audit Severity' + 'is not equal to' + 'PASSED' to extract all potential issues.
[3] Select Report -> CSV from the menu bar. In the report settings, clear all checkboxes except 'Host' and 'Description' and click 'Generate Report'.
[4] The file to be processed by nessCIS will be downloaded. Run Python nessCIS.py <path to file>
[5] Open the nessCIS output file in Excel and check it, then save it as .xlsx.
[6] Import the Excel spreadsheet into an appendix in the report.
[7] Add a vulnerability in the report called 'CIS Failures' and point the details to 'See Appendix X'
