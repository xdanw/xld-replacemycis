
import xml;
import requests;
import xml.etree.ElementTree as ET

# Prompt
# Comment out if you want to code it into the script 

xldUrl = input("XL Deploy URL: ") 

if (str(xldUrl[len(xldUrl)-1:]) != '/') : 
    xldUrl = xldUrl + '/';

base_url = xldUrl + 'deployit/repository/ci/'
uri_get_ci = xldUrl + 'deployit/repository/v3/query?resultsPerPage=-1';

xldUser = input("Username: ") 
xldPass = input("Password: ") 

# Use values coded into the script

# base_url = 'http://127.0.0.1:4516/deployit/repository/ci/'
# uri_get_ci = 'http://127.0.0.1:4516/deployit/repository/v3/query?resultsPerPage=-1';
# xldUser = 'admin'
# xldPass = 'admin'

xmlHeader = {"Content-Type":"application/xml"};

get_ci_response = requests.get(uri_get_ci, headers=xmlHeader, auth=(xldUser, xldPass))

if str(get_ci_response.status_code) != '200' : 
    print(str(get_ci_response.status_code))
    raise Exception;

root = ET.fromstring(get_ci_response.content)

# Unused
# 
# deployment_package_list = []
# 
# for c in root: 
#    if c.attrib['type'] == 'udm.DeploymentPackage': 
#       print c.attrib['ref']
#       deployment_package_list.append(c.attrib['ref'])
      
# This list will only run on file.File (basic file) types. It's useful for testing, 
# and you can explicitly add other types if you want -->  'file.File' or c.attrib['type'] == 'sql.SqlScripts'

# fileuri_list = []

# for c in root: 
#    if c.attrib['type'] == 'file.File': 
#       print c.attrib['ref']
#       fileuri_list.append(c.attrib['ref'])

everything_artifacts_list = []

for c in root: 
   if str(c.attrib['ref']).find("Applications/") > -1 and \
   str(c.attrib['type']).find("udm.") == -1 and \
   str(c.attrib['type']).find("core.") == -1 and \
   str(c.attrib['type']).find("internal.") == -1 : 
      print(str(c.attrib['type']) + ": " + str(c.attrib['ref']));
      everything_artifacts_list.append(c.attrib['ref'])
      
# We're replacing www.example.com with www.example.net

# Note that there could be unexpected behavior. If the old IP address is present 
# inside a name, tag or comment field, it will also be replaced.

print("");
print("This script won't back up your data. A backup using xl generate or a database snapshot is required to continue.")
print("To acknowledge that you have the required backup, type yes.")
print("");

confirmTest = input("Continue? (YES/no): ") 
if(str.upper(confirmTest) != "YES"): 
    exit();

# To scan only for file.File artifacts ---> for f in fileuri_list: 

for f in everything_artifacts_list: 
   print("Checking CI: " + str(f));
   ci_response = requests.get(base_url + str(f), headers=xmlHeader, auth=(xldUser, xldPass))
   new_ci_data = ci_response.text.replace("example.com", "example.net")
   if ci_response.text.find("example.com") > -1 : 
      print("Replacing CI: " + str(f))
      delete_response = requests.delete(base_url + f, headers=xmlHeader, auth=(xldUser, xldPass))
      print("Delete: " + str(delete_response.status_code))
      add_response = requests.post(base_url + f, data=new_ci_data, headers=xmlHeader, auth=(xldUser, xldPass))
      print("Create: " + str(add_response.status_code))

   






