# LiteLLM Proxy Setup Guide

A containerized LiteLLM proxy server with PostgreSQL database for managing multiple AI model endpoints.

## Prerequisites

- Docker and Docker Compose installed
- API keys for the AI services you want to use (OpenAI, Anthropic, etc.)

## Quick Start

### 1. Clone or Navigate to Project

```bash
cd /path/to/litellm
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit the `.env` file and update the values with your configuration:

```bash
# Database Configuration
POSTGRES_USER=litellm
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=litellm_db

# LiteLLM Master API Key (Must start with sk-)
LITELLM_MASTER_KEY=sk-your-secure-key

# Unique encryption key (Required for storing models/keys safely)
LITELLM_SALT_KEY=sk-your-salt-key

# External AI Provider Keys (Add whatever you use)
OPENAI_API_KEY=sk-proj-your-actual-api-key
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key
```

**Important:** 
- Generate secure keys instead of using the examples
- Add your actual API keys for the services you want to use
- Never commit `.env` to version control (use `.env.example` as a template)

### 3. Configure Models

Edit `litellm-config.yaml` to add or modify the models you want to expose:

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: "os.environ/OPENAI_API_KEY"

  - model_name: claude-3-5-sonnet
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20240620
      api_key: "os.environ/ANTHROPIC_API_KEY"

litellm_settings:
  store_model_in_db: True
```

### 4. Start the Containers

```bash
docker compose up -d
```

This will:
- Create and start the PostgreSQL database container (`litellm-db`)
- Create and start the LiteLLM proxy container (`litellm-proxy`)
- Initialize the database with required tables
- Apply all database migrations

### 5. Verify the Setup

Check that both containers are running:

```bash
docker compose ps
```

Expected output:
```
NAME            STATUS
litellm-db      Up
litellm-proxy   Up
```

Test the proxy health endpoint:

```bash
curl http://localhost:4000/health
```

## Service Access

| Service | URL | Description |
|---------|-----|-------------|
| LiteLLM Proxy | http://localhost:4000 | Main proxy API |
| PostgreSQL | localhost:5432 | Database (internal) |

## Common Operations

### View Logs

View proxy logs:
```bash
docker compose logs litellm-proxy -f
```

View database logs:
```bash
docker compose logs litellm-db -f
```

View all logs:
```bash
docker compose logs -f
```

### Stop Containers

```bash
docker compose down
```

### Stop and Remove All Data

```bash
docker compose down -v
```

**Warning:** This will delete all data in the database!

### Restart Containers

```bash
docker compose restart
```

## Using the LiteLLM Proxy

Once running, you can make requests to the proxy:

```bash
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d {
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }
```

## Troubleshooting

### "Role does not exist" Error

If you see database errors about missing users:

```bash
docker compose down -v
docker compose up -d
```

This completely resets the database with fresh initialization.

### Port Already in Use

If port 4000 or 5432 is already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "4001:4000"  # Change 4001 to your desired port
```

### Container Won't Start

Check the logs:
```bash
docker compose logs litellm-proxy
```

Common issues:
- Invalid `.env` variables
- Missing config file `litellm-config.yaml`
- Database connection issues

### Migrations Failing

Clear everything and reinitialize:

```bash
docker compose down -v
docker compose up -d
```

## Project Structure

```
.
├── .env                      # Environment variables (local, not in git)
├── .env.example              # Environment template (commit to git)
├── docker-compose.yml        # Docker Compose configuration
├── litellm-config.yaml       # LiteLLM proxy configuration
├── litellm_config.yaml/      # (empty folder - can be deleted)
└── README.md                 # This file
```

### Setup with `.env.example`

1. Copy `.env.example` to `.env` when first setting up
2. Edit `.env` with your credentials and API keys
3. `.env` is ignored by git (add to `.gitignore`)
4. `.env.example` is committed to git so others can see required variables

## Security Best Practices

### Git Setup

Ensure `.env` is not tracked by git:

```bash
# Add .env to .gitignore
echo ".env" >> .gitignore

# If .env was already committed, remove it
git rm --cached .env
git commit -m "Remove .env from tracking"
```

### Environment and Keys

1. **Never commit `.env` to git** - it contains sensitive API keys
2. **Use strong passwords** - Change `POSTGRES_PASSWORD` and generate secure keys
3. **Change default keys** - Replace `LITELLM_MASTER_KEY` and `LITELLM_SALT_KEY` with unique values
4. **Restrict network access** - Don't expose ports 4000 and 5432 to the internet without proper authentication
5. **Use secrets management** - Consider using Docker Secrets or external secret managers in production

Generate secure keys with:
```bash
# Linux/Mac
openssl rand -hex 16

# Windows PowerShell
[System.Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 } | ForEach-Object { [byte]$_ })) -replace '=+$'
```

## Additional Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Support

For issues or questions:
- Check the [LiteLLM GitHub Issues](https://github.com/BerriAI/litellm/issues)
- Review container logs: `docker compose logs`
- Verify configuration files are correct
