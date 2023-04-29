# Filebeat

Filebeat is a lightweight data shipping agent that is used for forwarding and centralizing log data. It is part of the Elastic Stack, which also includes Elasticsearch, Logstash, and Kibana, and it is designed to work seamlessly with the other components of the stack. Filebeat is used to collect log data from various sources and forward it to a central location, such as Elasticsearch, where it can be indexed and analyzed.

Filebeat supports a variety of input types, including log files, system logs, and application logs, and it can be configured to tail and forward logs in real-time. It also supports a range of output destinations, including Elasticsearch, Logstash, Kafka, and Redis.

Filebeat has a small footprint and low resource utilization, making it ideal for use in distributed architectures where resources are limited. It also provides powerful filtering and processing capabilities, allowing users to selectively collect and transform log data before it is sent to its final destination. Overall, Filebeat is a powerful tool for collecting and forwarding log data and is widely used in large-scale distributed environments to gain insights into system performance, troubleshooting issues, and detecting anomalies.

We configured Filebeat to collect logs from all Docker containers in the /var/lib/docker/containers directory, and to enrich the log events with metadata about the Docker containers they came from using the add_docker_metadata processor. We have also included a decode_json_fields processor to decode any JSON-encoded log messages and store the resulting objects in a new json field.

Additionally, we configured the output destination to send the processed logs to Elasticsearch running at elasticsearch:9200. We have defined three index templates based on the container image names: one for the Filebeat container itself, one for two specific container images (API and APP), and one for an Nginx container.

We also enabled JSON logging format for Filebeat logs and disabled metrics logging for Filebeat.

Finally, the following volumes are mounted to the Filebeat container:

/var/lib/docker:/var/lib/docker:ro - mounts the Docker host's /var/lib/docker directory to allow Filebeat to collect logs from Docker containers.
/var/run/docker.sock:/var/run/docker.sock - mounts the Docker host's Docker socket to allow Filebeat to communicate with the Docker API.

Overall, this configuration will allow us to collect and centralize log data from multiple Docker containers in a structured and organized way, making it easier to analyze and troubleshoot issues in our system.

In the next section we explain the steps in more details.

## Dockerfile

1. We are using the official Docker image for Filebeat version 7.2.0 from Elastic.co.
2. we are using root user to allow copying of the filebeat.yml file to the appropriate directory.
3. Then we copy the filebeat.yml file from the host system to the appropriate directory inside the Docker container.
4. FInally, with CMD ["filebeat", "-e"] command we set the default command to execute when the Docker container starts. In this case, it is the "filebeat" binary with the "-e" flag, which tells Filebeat to log output to the standard error.

## filebeat.yml

1. filebeat.inputs: This section specifies the input sources for Filebeat to collect logs from.
2. processors: This section specifies the processing steps to apply to the collected logs.
3. output.elasticsearch: This section specifies the output destination for the processed logs.
4. logging.json: true: This setting enables JSON logging format for Filebeat logs.
5. logging.metrics.enabled: false: This setting disables metrics logging for Filebeat.
