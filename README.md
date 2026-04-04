# DevSecOps Blueprints

An enterprise-grade, visually stunning CLI for advanced vulnerability scanning, auto-remediation, and continuous infrastructure security (CI/CD).

## Overview
`devsecops-blueprints` is a powerful Monorepo toolkit wrapping industry-standard tools like Trivy and Gitleaks. Instead of just failing pipelines when vulnerabilities run rampant, it provides an "Actionable Solution" – letting you seamlessly pull in hardened, secure-by-default templates directly from our armory.

## Prerequisites & Installation

To use this CLI properly, you must have the required security scanning engines installed.

### Installing Dependencies (Trivy & Gitleaks)
*   **macOS**: `brew install trivy gitleaks`
*   **Windows**: `winget install Aquasecurity.Trivy` & `winget install gitleaks`
*   **Linux (Debian/Ubuntu)**: Run our `setup` command.

*(Or simply run `devsecops-blueprints setup` to view interactive instructions or automatically install them!)*

### Installing the CLI via Native Python

```bash
# If using poetry
poetry install

# Alternatively, directly via pip (PEP-621)
pip install .
```

### Docker Distribution Container (Zero-Install)
If you don't want to install Python, Trivy, or Typer locally, use our hardened Multi-Stage Docker image:
```bash
# Build the image locally
docker build -t devsecops-blueprints:latest .

# Run the Audit against your current directory instantly 
docker run -v $(pwd):/app devsecops-blueprints:latest audit
```

## Continuous Security (CI/CD Automation)
A true DevOps armory must run continuously. You can automatically inject a perfect GitHub Actions pipeline into your repository.
```bash
# Automatically generates .github/workflows/blueprints-security.yml
devsecops-blueprints inject-ci
```
This enables the tool to scan for secrets and IaC Misconfig on every Pull Request seamlessly!

## Usage Manual

```bash
# Display setup and auto-installation helpers for tooling
devsecops-blueprints setup

# Inject the perfect GitHub Actions CI/CD to secure your repository
devsecops-blueprints inject-ci

# Run a vulnerability scan against a docker image
devsecops-blueprints scan my-vulnerable-image:latest

# Fetch a secured baseline blueprint
devsecops-blueprints fetch docker-node

# Scan Infrastructure as Code (Terraform, Dockerfile, K8s) for misconfigurations
devsecops-blueprints iac .

# Audit the current directory for hardcoded secrets
devsecops-blueprints audit
```
