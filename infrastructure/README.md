# 🏗️ Infrastructure

Deployment, DevOps, and cloud infrastructure configurations.

## Structure

```
infrastructure/
├── docker/                  # Docker configurations
│   ├── web.Dockerfile      # Web app container
│   ├── mobile.Dockerfile   # Mobile build container
│   ├── backend.Dockerfile  # Backend API container
│   ├── ai.Dockerfile       # AI services container
│   └── docker-compose.yml  # Local development stack
├── kubernetes/              # K8s manifests
│   ├── deployments/        # Deployment configs
│   ├── services/           # Service configs
│   ├── ingress/            # Ingress rules
│   ├── configmaps/         # ConfigMaps
│   └── secrets/            # Secret templates
├── terraform/               # Infrastructure as Code
│   ├── modules/
│   │   ├── database/       # RDS/Cloud SQL
│   │   ├── storage/        # S3/GCS buckets
│   │   ├── compute/        # EC2/GCE instances
│   │   └── networking/     # VPC, subnets
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── production/
│   └── main.tf
└── scripts/                 # Utility scripts
    ├── deploy.sh           # Deployment script
    ├── backup.sh           # Database backup
    ├── seed.sh             # Seed data
    └── setup-local.sh      # Local env setup
```

## Quick Start

### Local Development
```bash
docker-compose -f docker/docker-compose.yml up
```

### Deploy to Production
```bash
./scripts/deploy.sh production
```

### Infrastructure Provisioning
```bash
cd terraform/environments/production
terraform init && terraform apply
```
