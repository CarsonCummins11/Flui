pip install -r requirements.txt
#windows equivalent of curl, then run msi installer to run mongodb
bitsadmin /transfer mongodbdownloadjob /download /priority normal https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.3-signed.msi .
msiexec.exe /l*v mdbinstall.log  /qb /i mongodb-win32-x86_64-2012plus-4.2.3-signed.msi
mongod.exe --service
python dbsetup.py
python3 -m flask run