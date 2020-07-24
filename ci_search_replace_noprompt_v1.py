
import xml;
import requests;
import xml.etree.ElementTree as ET

base_url = 'http://127.0.0.1:4516/deployit/repository/ci/'
uri_get_ci = 'http://127.0.0.1:4516/deployit/repository/v3/query?resultsPerPage=-1';
xmlHeader = {"Content-Type":"application/xml"};

get_ci_response = requests.get(uri_get_ci, headers=xmlHeader, auth=('admin', 'admin'))

if get_ci_response.status_code != '200'
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

fileuri_list = []

for c in root: 
   if c.attrib['type'] == 'file.File': 
      print c.attrib['ref']
      fileuri_list.append(c.attrib['ref'])

everything_artifacts_list = []

for c in root: 
   if c.attrib['ref'].find("Applications/") > -1 and \
   c.attrib['type'].find("udm.") == -1 and \
   c.attrib['type'].find("core.") == -1 and \
   c.attrib['type'].find("internal.") == -1 : 
      print c.attrib['type'] + ": " + c.attrib['ref']
      everything_artifacts_list.append(c.attrib['ref'])
      
# We're replacing www.example.com with www.example.net

# Note that there could be unexpected behavior. If the old IP address is present 
# inside a name, tag or comment field, it will also be replaced.

if True: 
   print "This script won't back up your data. A backup using xl generate or a database snapshot is required to continue."
   print "To acknowledge that you have the required backup, put False in the conditional."
   raise Exception;

# To scan only for file.File artifacts ---> for f in fileuri_list: 

for f in everything_artifacts_list: 
   print "Checking CI: " + f
   ci_response = requests.get(base_url + f, headers=xmlHeader, auth=('admin', 'admin'))
   new_ci_data = ci_response.text.replace("example.com", "example.net")
   if ci_response.text.find("example.com") > -1 : 
      print "Replacing CI: " + f
      delete_response = requests.delete(base_url + f, headers=xmlHeader, auth=('admin', 'admin'))
      print "Delete: " + str(delete_response.status_code)
      add_response = requests.post(base_url + f, data=new_ci_data, headers=xmlHeader, auth=('admin', 'admin'))
      print "Create: " + str(add_response.status_code)

   






