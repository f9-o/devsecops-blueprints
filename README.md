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

# Inject a Zero-Trust GitHub Actions CI/CD workflow to secure your repository pushes
devsecops-blueprints inject-ci

# Explore the interactive F9 Armory Catalog for available secure templates
devsecops-blueprints catalog

# Fetch a secured baseline blueprint (Run without arguments for an interactive prompt)
devsecops-blueprints fetch [template_name]

# Run a vulnerability scan against a container image
devsecops-blueprints scan my-vulnerable-image:latest

# Scan Infrastructure as Code (Terraform, Dockerfile, K8s) for misconfigurations
devsecops-blueprints iac .

# Audit the current directory for hardcoded secrets
devsecops-blueprints audit

# Generate a visually stunning HTML Executive Security Report based on silent analysis
devsecops-blueprints report .

# Auto-Remediate: Let the AI-Ready patcher rewrite your insecure configurations securely
devsecops-blueprints fix .
```
