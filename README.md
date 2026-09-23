# SQL Server Performance Health Check

Automated SQL Server performance assessment and reporting tool.

## Overview

This project performs a read-only SQL Server health check and generates structured evidence, assessments, findings, and an HTML performance report.

## Assessment Areas

- Environment
- Query Performance
- Wait Statistics
- Blocking
- Indexes
- Statistics

## Architecture

SQL Server  
↓  
Checks  
↓  
Evidence (JSON)  
↓  
Assessment  
↓  
Findings  
↓  
HTML Report

## Output

The generated report provides:

- Executive Summary
- Environment Assessment
- Query Performance Analysis
- Wait Statistics
- Blocking Analysis
- Index Assessment
- Statistics Assessment
- Performance Findings
- Recommendations

## Technologies

- Python
- SQL Server
- pyodbc
- Jinja2
- JSON
- HTML / CSS

## Project Goal

The goal is to provide a repeatable and evidence-based SQL Server Performance Health Check suitable for DBA and performance consulting workflows.

## Status

Active development.

## Sample Report

A generated HTML performance health check report is included in:

`reports/performance_health_check.html`

The report contains the assessment results, evidence, and actionable findings.
