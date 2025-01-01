# Monitoring Strategy for the Product Similarity API

## Table of Contents

- [Monitoring Strategy for the Product Similarity API](#monitoring-strategy-for-the-product-similarity-api)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [1. Model Metrics](#1-model-metrics)
    - [1.1. Relevance Score Distribution](#11-relevance-score-distribution)
    - [1.2. False Positives](#12-false-positives)
  - [2. Data Quality](#2-data-quality)
    - [2.1. Query Drift](#21-query-drift)
    - [2.2. Product Embedding Drift](#22-product-embedding-drift)
    - [2.3. Number of input tokens](#23-number-of-input-tokens)
  - [3. Performance Metrics](#3-performance-metrics)
    - [3.1. Response Time (Latency)](#31-response-time-latency)
    - [3.2. Error Rate](#32-error-rate)
  - [4. Infrastructure](#4-infrastructure)
    - [4.1. Monitor the Health of the API](#41-monitor-the-health-of-the-api)
    - [4.2. Resource Utilization](#42-resource-utilization)
  - [4. Implementation Steps](#4-implementation-steps)
    - [4.1. Metrics Collection](#41-metrics-collection)
    - [4.2. Alerting](#42-alerting)
    - [4.3. Setup Autoscaling](#43-setup-autoscaling)

## Introduction
Machine Learning models in production environment, unlike the traditional software, interact with the changing datasets and without proper monitoring solutions, their performance can degrade. This can lead to slower response times, inaccurate predictions, and also potential system outages if we lack infrastructure health monitoring. Having a proper monitoring strategy will help us to detect these issues early and take appropriate actions to maintain the model's performance and system's health.

This document outlines the comprehensive monitoring strategy for the Product Similarity API. This monitoring system is mainly split into three main categories:
- Model metrics
- Data quality
- Performance metrics
- Infrastructure metrics

## 1. Model Metrics

### 1.1. Relevance Score Distribution
Relevance score distribution helps us to understand the model's performance over time. Track the shift in the distribution to detect if the model's performance is degrading. This would help us to decide if further fine-tuning is needed.
- Use a histogram to visualize the distribution of the relevance scores.
- Conduct statistical tests like `Chi-square test` or `Kolmogorov-Smirnov test` to detect if the distribution of the relevance scores shifts significantly.
- Alert if the distribution of the relevance scores shifts significantly.

### 1.2. False Positives
False positives are matches that are not relevant to the query. Track the percentage of false positives in the recommendations. Reducing false positives improves the overall trustworthiness of the model.
- Collect user feedback on incorrect product matches
- Log flagged results and retrain the model to minimize false positives.

## 2. Data Quality

### 2.1. Query Drift
Query drift happens when the type of queries change over time and deviate from what the model was trained on. For example, if the model was trained on product descriptions, but the queries start to include non-descriptive queries, the model may return irrelevant results.
- Track embeddings of incoming queries.
- Use cosine similarity to measure the similarity between the new query and the past queries.
- Alert if the average cosine similarity of new queries vs. past queries drops below a threshold (e.g. 0.8). This will help us to decide if the model needs to be fine-tuned.

### 2.2. Product Embedding Drift

Product embedding drift occurs when the embeddings of product descriptions change significantly over time. This can happen due to product catalog updates, description modifications, or changes in the embedding model itself.
- Recompute and compare embeddings of products at regular intervals.
- Track cosine similarity between old and new embeddings.
- Trigger drift alerts if similarity drops below a defined threshold (e.g., 0.90). This will help us to decide if the model needs to be fine-tuned.

### 2.3. Number of input tokens
According to the model `hkunlp/instructor-base`, the maximum number of input tokens is 512.
- Initially set a threshold of 512 tokens.
- Log and count the number of times the number of input tokens exceeds 512.
- Alert if the number of times the number of input tokens exceeds 512 exceeds a threshold (e.g., 100 times). This will help us to decide if the model needs to be fine-tuned or change the embedding model.

## 3. Performance Metrics

### 3.1. Response Time (Latency)
Measure how long the model takes to process the query and return the results. Spikes could indicate resource bottlenecks or inefficient processing.
- Track latency percentiles like p50, p90, p99 latency.
- Set thresholds for p95 and p99 (e.g., p95 > 500ms triggers an alert).

### 3.2. Error Rate
Track the percentage of requests that result in errors. High error rates could indicate model instability or data issues.
- Log errors and count failed requests.
- Calculate error rate as a percentage of total requests.
- Set thresholds for error rate (e.g., >2% triggers an alert).

## 4. Infrastructure

### 4.1. Monitor the Health of the API
Continuously monitor the `/health` endpoint to ensure the API is running smoothly.
- Set up a job to run this check every 5 minutes.
- Alert if the status code is `5xx`.

### 4.2. Resource Utilization
Monitor the CPU, memory, and disk usage of the API. This will help us to detect if the application is running out of resources.
- Alert if any resource is running out of capacity.


## 4. Implementation Steps
Choose the proper infrastructure for setting up the monitoring system.
- If we are using AWS, we can use CloudWatch to monitor the resources and logs. We can use SNS to send alerts.
- If we want to use a self-hosted solution, we can use Prometheus and Grafana to monitor the resources and logs.
- Store embeddings and request logs in a database (PostgreSQL) for long-term analysis.

### 4.1. Metrics Collection
- Implement a middleware to collect the metrics from the API.
  - Integrate `prometheus-fastapi-instrumentator` to collect key application metrics (response time, throughput, error rates).
- Log incoming query payloads, model outputs, and match scores to PostgreSQL for drift analysis.

### 4.2. Alerting
As described in the previous sections on metrics we monitor, alert when something fails.

### 4.3. Setup Autoscaling
Set up autoscaling for the API based on the metrics we monitor. For example:
- CPU > 80% for 5 minutes
- Throughput > 1000 requests per second
