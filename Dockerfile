FROM debian:stable-slim

RUN apt update && apt install -y nano python3-pip unzip xvfb curl wget ca-certificates libxss1 libxtst6 libpangocairo-1.0-0 libstdc++6 libx11-6 
RUN pip3 install pillow wheel Flask requests pyppeteer

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
RUN bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
RUN apt -y update 
RUN apt -y install google-chrome-stable 

COPY ./test.py /tmp/test.py
COPY ./main.py /opt/main.py
COPY ./flaskrun.sh /opt/flaskrun.sh
COPY ./run.py /opt/run.py
COPY ./UrlScreenShot.py /opt/UrlScreenShot.py
COPY ./angular/siteScreenShot/dist/siteScreenShot /opt/static
RUN ln -s /opt/static /opt/templates

RUN python3 /tmp/test.py #downloads chrome

#DEBUG MODE
RUN chmod a+x /opt/flaskrun.sh
EXPOSE 1111
CMD ["/opt/flaskrun.sh"]

#APACHE MODE WIP
#RUN apt update \
#    && apt upgrade -y \
#    && apt install --no-install-recommends -y \
#        apache2 \
#        apache2-dev \
#        build-essential \ 
#        libapache2-mod-wsgi-py3 \
#        python3-dev \
#        python3-pip \
#        python3-setuptools\
#    && apt clean \ 
#    && apt autoremove \
#    && rm -rf /var/lib/apt/lists/* 
#
#RUN a2enmod ssl \
#    && a2dissite 000-default.conf
#
#COPY apache/* /etc/apache2/sites-available/
#RUN a2ensite apache-flask #apache-flask-ssl
#
#RUN mkdir -p /opt/log/
#
#EXPOSE 80 443
#CMD ["/usr/sbin/apache2ctl","-DFOREGROUND"]