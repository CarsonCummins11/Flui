ps -ef | grep "flask" | awk '{print $2}' | xargs sudo kill
cd ..
sudo python3 -m flask run --host=localhost --port=5000 &
mongo [matcher] --eval "db.getCollectionNames().forEach(function(n){db[n].remove()});"
sleep 10s
cd test
python3 test_server_status.py
sleep 5s
mongo [matcher] --eval "db.getCollectionNames().forEach(function(n){db[n].remove()});"
python3 run_test_suite.py
