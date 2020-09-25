FROM tensorflow/serving:latest

RUN apt-get update && apt-get install -y dirmngr gnupg
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 561F9B9CAC40B2F7
RUN apt-get install -y apt-transport-https ca-certificates
RUN sh -c 'echo deb https://oss-binaries.phusionpassenger.com/apt/passenger bionic main > /etc/apt/sources.list.d/passenger.list'
RUN apt-get update && apt-get install -y libnginx-mod-http-passenger

RUN rm /etc/nginx/sites-enabled/default
RUN rm -f /etc/service/nginx/down

ADD ./server/nginx.app.conf /etc/nginx/sites-enabled/app.conf

RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log
CMD ["nginx", "-g", "daemon off;"]

RUN apt-get install -y python3-opencv

RUN apt-get install -y wget python3-distutils

ENV PATH="/root/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py --user && rm get-pip.py
RUN pip install --user flask numpy requests tensorflow opencv-python