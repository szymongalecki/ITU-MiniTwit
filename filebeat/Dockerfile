FROM docker.elastic.co/beats/filebeat:7.2.0
USER root
COPY filebeat.yml /usr/share/filebeat/filebeat.yml
CMD ["filebeat", "-e"]