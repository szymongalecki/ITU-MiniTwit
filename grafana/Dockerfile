FROM grafana/grafana:latest
COPY datasource.yml /etc/grafana/provisioning/datasources/datasource.yml
COPY dashboard.json /etc/grafana/provisioning/dashboards/dashboard.json
ARG GRAFANA_USERNAME
ARG GRAFANA_PASSWORD
ENV GF_DASHBOARDS_DEFAULT_HOME_DASHBOARD_PATH="/etc/grafana/provisioning/dashboards/dashboard.json"
ENV GF_SECURITY_ADMIN_USER=$GRAFANA_USERNAME
ENV GF_SECURITY_ADMIN_PASSWORD=$GRAFANA_PASSWORD
EXPOSE 3000
USER 1000