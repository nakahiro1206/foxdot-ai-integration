# build docker image
docker build -t midi-to-sonicpi .

# run model (start container in /data so relative paths work)
docker run --rm -v "$(pwd)":/data -w /data midi-to-sonicpi data/input.mid data/out.rb

# debug mode (start shell in /data so `ls` shows mounted files)
docker run --rm -it -v "$(pwd)":/data -w /data --entrypoint /bin/bash midi-to-sonicpi