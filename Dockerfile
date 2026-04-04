# Multi-stage build for DevSecOps Blueprints
FROM python:3.10-slim AS builder

WORKDIR /app
COPY pyproject.toml ./

# Install poetry and dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi || echo "No poetry deps fallback"

COPY . .
RUN pip install .

# Final stage
FROM python:3.10-slim

WORKDIR /app

# Install Trivy & Gitleaks dependencies
RUN apt-get update && apt-get install -y curl ca-certificates git && \
    rm -rf /var/lib/apt/lists/*

# Install Trivy
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Install Gitleaks
RUN curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/install.sh | sh -s -- -b /usr/local/bin

# Copy python dependencies from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/devsecops-blueprints /usr/local/bin/devsecops-blueprints
COPY . .

ENTRYPOINT ["devsecops-blueprints"]
CMD ["--help"]
