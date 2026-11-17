# OpenTelemetry Observability Lab

![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Observability-425CC7?logo=opentelemetry&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Visualization-F46800?logo=grafana&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Environment-FCC624?logo=linux&logoColor=black)

An end-to-end **cloud-native observability engineering lab** built using OpenTelemetry, Prometheus, Grafana, Docker, and Kubernetes.

This project explores how modern distributed systems collect, process, expose, and visualize telemetry data to provide visibility into application and infrastructure performance.

The central component is the **OpenTelemetry Collector**, which acts as a vendor-neutral telemetry pipeline between instrumented applications and observability backends.

The objective is to build a practical monitoring foundation, understand telemetry pipelines, troubleshoot application behavior, and develop skills relevant to production DevOps and Site Reliability Engineering (SRE).

---

## Architecture

```text
             INSTRUMENTED APPLICATIONS
                         |
                         |
                  OTLP Telemetry
                   gRPC :4317
                   HTTP :4318
                         |
                         v
              +----------------------+
              | OpenTelemetry        |
              | Collector            |
              |                      |
              | Receivers            |
              | Processors           |
              | Exporters            |
              +----------------------+
                         |
               +---------+---------+
               |                   |
               v                   v
        +-------------+      +-------------+
        | Prometheus  |      | Additional  |
        |             |      | Backends    |
        | Metrics     |      |             |
        | Storage     |      | Loki/Tempo  |
        +-------------+      +-------------+
               |                   |
               +---------+---------+
                         |
                         v
                  +-------------+
                  |   Grafana   |
                  |             |
                  | Dashboards  |
                  | Exploration |
                  +-------------+
```

**Architecture note:** Prometheus is used for metrics collection and storage. Grafana provides visualization. Additional backends such as Loki for logs and Tempo for traces can be integrated to support a complete metrics, logs, and traces observability stack.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| OpenTelemetry Collector | Telemetry ingestion and processing |
| Prometheus | Metrics collection and time-series storage |
| Grafana | Monitoring dashboards and visualization |
| Docker | Containerization |
| Docker Compose | Local service orchestration |
| Kubernetes | Container orchestration |
| OTLP | Standard telemetry communication protocol |
| YAML | Collector and infrastructure configuration |
| Linux | Development and deployment environment |

---

## Repository Structure

```text
otel-observability-lab/
│
├── collector/
│   └── otel-collector-config.yaml
│
├── prometheus/
│   └── prometheus.yml
│
├── k8s/
│   └──
│
├── docker-compose.yaml
│
└── README.md
```

### Directory Overview

- `collector/` - OpenTelemetry Collector configuration, including receivers, processors, exporters, and telemetry pipelines.
- `prometheus/` - Prometheus scrape configuration and monitoring targets.
- `k8s/` - Kubernetes deployment manifests for future cluster-based deployment.
- `docker-compose.yaml` - Defines the local observability services and their networking.

---

## Understanding the Observability Pipeline

### 1. OpenTelemetry Collector

The OpenTelemetry Collector is responsible for receiving, processing, and exporting telemetry data.

Its architecture consists of three primary components:

**Receivers**

Accept telemetry from instrumented applications and services.

Examples:

- OTLP gRPC receiver.
- OTLP HTTP receiver.
- Host Metrics receiver.

**Processors**

Process telemetry before exporting it.

Examples:

- Batch processor.
- Memory limiter processor.
- Resource processor.
- Attributes processor.

**Exporters**

Send processed telemetry to configured observability backends.

Examples:

- Prometheus exporter.
- OTLP exporter.
- Debug exporter.

### 2. Prometheus

Prometheus is responsible for collecting and storing time-series metrics.

It allows engineers to monitor:

- CPU and memory utilization.
- Application request rates.
- HTTP response times.
- Error rates.
- Service availability.
- Custom application metrics.

Prometheus uses a pull-based scraping model to collect metrics from configured endpoints.

### 3. Grafana

Grafana provides a visualization layer for monitoring and observability.

It can connect to Prometheus and other supported data sources to build dashboards that help engineers:

- Monitor service health.
- Analyze application performance.
- Investigate resource utilization.
- Identify abnormal behavior.
- Track operational trends.

---

## Prerequisites

Install the following tools:

- [Docker](https://docs.docker.com/get-started/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

Optional for Kubernetes deployment:

- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Kind](https://kind.sigs.k8s.io/)

Verify installations:

```bash
docker --version
docker compose version
git --version
```

---

## Installation & Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/Remmaabde/otel-observability-lab.git

cd otel-observability-lab
```

### 2. Start the Observability Stack

Start the configured services using Docker Compose:

```bash
docker compose up -d
```

Check the running containers:

```bash
docker compose ps
```

### 3. Inspect Container Logs

Check all service logs:

```bash
docker compose logs -f
```

Inspect an individual service:

```bash
docker compose logs -f otel-collector
```

Use the actual service name defined in your Compose file if it differs.

### 4. Access Monitoring Interfaces

Once the services are running and their ports are published, access the following interfaces:

| Service | URL | Purpose |
|---|---|---|
| Grafana | http://localhost:3000 | Dashboards and visualization |
| Prometheus | http://localhost:9090 | Metrics queries and target health |
| OTLP gRPC | localhost:4317 | Telemetry ingestion |
| OTLP HTTP | localhost:4318 | Telemetry ingestion |

**Grafana:** Use the credentials configured in your Docker Compose environment.

**Prometheus:** Navigate to `Status → Targets` to inspect configured scrape targets.

**Note:** The endpoints above assume your Compose configuration publishes these ports to the host.

---

## Configuring Application Telemetry

One of the main objectives of this lab is to connect applications to a centralized telemetry pipeline.

An OpenTelemetry-instrumented application can export telemetry to the Collector using standard environment variables.

Example configuration for an application using OTLP gRPC:

```bash
export OTEL_SERVICE_NAME="finance-tracker"

export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"

export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
```

For applications running in another Docker container, use the Collector's Docker Compose service name instead of `localhost`, provided both services share a Docker network.

Example:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"
```

The actual service name must match your Compose configuration.

---

## Practical Observability Experiments

### 1. Verify Collector Connectivity

Check the Collector logs:

```bash
docker compose logs otel-collector
```

Confirm that the configured receivers and exporters start successfully.

### 2. Verify Prometheus Targets

Open:

```text
http://localhost:9090/targets
```

Check whether configured targets are reporting:

```text
UP
```

Investigate any targets reporting:

```text
DOWN
```

### 3. Query Application Metrics

Open the Prometheus expression browser:

```text
http://localhost:9090/graph
```

Execute PromQL queries against the metrics available in your environment.

Example:

```promql
up
```

This query reports the availability of Prometheus scrape targets.

### 4. Build Grafana Dashboards

Open:

```text
http://localhost:3000
```

Configure Prometheus as a Grafana data source and build dashboards for application and infrastructure monitoring.

Useful dashboard metrics include:

- CPU utilization.
- Memory consumption.
- HTTP request rate.
- HTTP error rate.
- Request latency.
- Service availability.

The actual metrics depend on the application instrumentation and configured Collector pipeline.

---

## Engineering Concepts Demonstrated

This project focuses on practical understanding of:

- Cloud-native observability architecture.
- OpenTelemetry instrumentation.
- Telemetry collection and processing.
- OTLP communication using gRPC and HTTP.
- Collector receivers, processors, and exporters.
- Prometheus metrics collection and storage.
- PromQL fundamentals.
- Grafana dashboards and visualization.
- Docker-based infrastructure deployment.
- Distributed application monitoring.
- Service health and performance investigation.
- Kubernetes observability integration.

---

## Future Improvements

The goal is to evolve this project into a production-oriented observability platform.

- [ ] Instrument a real application using OpenTelemetry SDKs.
- [ ] Integrate OpenTelemetry auto-instrumentation.
- [ ] Add Prometheus alerting rules.
- [ ] Integrate Alertmanager for alert routing.
- [ ] Add Loki for centralized log aggregation.
- [ ] Add Grafana Tempo for distributed tracing.
- [ ] Implement trace correlation with application logs.
- [ ] Create custom Grafana dashboards.
- [ ] Monitor Docker container resource utilization.
- [ ] Deploy the observability stack to Kubernetes.
- [ ] Integrate observability deployment with ArgoCD.
- [ ] Implement service-level indicators (SLIs).
- [ ] Explore service-level objectives (SLOs).
- [ ] Implement resource limits and persistent storage.
- [ ] Integrate OpenTelemetry with a real-world microservices application.

---

## Cleanup

Stop and remove the running services:

```bash
docker compose down
```

To also remove Compose-managed volumes:

```bash
docker compose down -v
```

**Warning:** The `-v` option removes the associated named and anonymous volumes and may permanently delete stored monitoring data.

---

## Learning Objective

This project is part of my hands-on journey as a **DevOps / Site Reliability Engineer (SRE)**.

My focus is on understanding how production systems are monitored, how telemetry flows across distributed services, and how engineers use observability tools to detect, investigate, and resolve operational issues.

**The goal is to build systems that are not only deployable and scalable, but also observable, measurable, and reliable.**
