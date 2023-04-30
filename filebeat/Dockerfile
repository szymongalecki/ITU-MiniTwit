FROM docker.elastic.co/beats/filebeat:7.17.1
USER root
COPY filebeat.yml /usr/share/filebeat/filebeat.yml
CMD ["filebeat", "-e", "-strict.perms=false"]