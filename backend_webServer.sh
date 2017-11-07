fuser -k 3000/tcp
fuser -k 4040/tcp
#fuser -k 6060/tcp
cd web_server/server
npm start &
cd ../../backend_server
python service.py

echo“====================================”
read -p "PRESS [ENTER] TO TERMINATE PROCESSES" PRESSKEY
kill $(jobs -p)
fuser -k 3000/tcp &
fuser -k 4040/tcp 
#fuser -k 5050/tcp &
#fuser -k 6060/tcp
