# Phone Orientation Viewer

### Build
docker build -t phone-orientation-viewer . -f Dockerfile

### Run
docker run -dt -p 80:80 -p 6000:6000/udp -e UDP_IP=<PHONE_IP> phone-orientation-viewer
