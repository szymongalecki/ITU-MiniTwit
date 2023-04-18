FROM grafana/grafana:latest
COPY ./provisioning /etc/grafana/provisioning
#RUN mkdir /var/lib/grafana/dashboards
COPY ./dashboards/exported_dashboard.json /etc/grafana/provisioning/dashboards/exported_dashboard.json
COPY ./provisioning/datasources/ /etc/grafana/provisioning/datasources
COPY ./provisioning/dashboards/ /etc/grafana/provisioning/dashboards
