FROM ubuntu:latest

COPY crontab.txt /crontab.txt
COPY script.sh /script.sh
COPY entry.sh /entry.sh
RUN chmod 755 /script.sh /entry.sh

RUN mkdir /var/scraper
COPY . /var/scraper


#Install Cron
RUN apt-get update
RUN apt-get -y install python3-pip build-essential libssl-dev libffi-dev python3-dev
RUN apt-get -y install cron

RUN /usr/bin/crontab /crontab.txt

CMD ["/entry.sh"]


# Add crontab file in the cron directory
# ADD crontab /etc/cron.d/hello-cron

# # Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/hello-cron

# # Create the log file to be able to run tail
# RUN touch /var/log/cron.log

# RUN pip3 install -r requirements.txt

# Run the command on container startup
# CMD cron && tail -f /var/log/cron.log