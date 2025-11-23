# Serverless LangChain Agent

A serverless LangChain agent built with AWS Lambda, FastAPI, and AWS CDK.

## Features

- FastAPI-based REST API with streaming support
- LangChain agent using `create_agent()` paradigm
- Deployed on AWS Lambda with Docker containers
- AWS Lambda Web Adapter for running FastAPI
- SSM Parameter Store for API key management
- Infrastructure as Code using AWS CDK

## Architecture

- **Agent Framework**: LangChain with LangGraph streaming
- **Web Framework**: FastAPI with async support
- **Runtime**: AWS Lambda with Docker container images
- **Infrastructure**: AWS CDK (Python)
- **Package Manager**: uv for fast Python dependency management

## API Endpoints

### Health Check
```
GET /healthz
```

### Research Agent (Non-streaming)
```
POST /agents/research
```

Returns complete agent response.

### Research Agent (Streaming)
```
POST /agents/research/stream
```

Returns Server-Sent Events (SSE) stream with agent steps.

## Local Development

### Prerequisites

- Python 3.13+
- uv package manager
- Docker
- Docker Compose with watch support

### Setup

1. Install dependencies:
```bash
uv sync
```

2. Set OpenAI API key:
```bash
export OPENAI_API_KEY=your-api-key
```

### Development Commands

The project uses [poethepoet](https://poethepoet.natn.io/) as a task runner. All commands are prefixed with `uv run poe`:

#### `uv run poe dev`
**Hot-reloading development mode** - Best for active development
- Starts the container with file watching enabled
- Automatically syncs code changes from `./agent` to the container
- Uvicorn auto-reloads on file changes
- No need to rebuild or restart manually
```bash
uv run poe dev
```

#### `uv run poe start`
**Quick start** - When you just want to run the existing image
- Starts containers in detached mode
- Uses the last built image
- Useful for testing without code changes
```bash
uv run poe start
```

#### `uv run poe build`
**Build only** - When you want to build without starting
- Builds the Docker image
- Doesn't start any containers
- Useful for CI/CD or pre-building images
```bash
uv run poe build
```

#### `uv run poe restart`
**Rebuild and start** - When you've changed dependencies or Dockerfile
- Rebuilds the image and starts containers
- Useful after changing `pyproject.toml` or `Dockerfile`
- Runs in detached mode
```bash
uv run poe restart
```

#### `uv run poe logs`
**Follow logs** - Monitor running containers
- Tails logs from all running services
- Useful when running in detached mode
```bash
uv run poe logs
```

#### `uv run poe down`
**Stop and cleanup** - Stop all containers
- Stops and removes containers
- Keeps built images
```bash
uv run poe down
```

### Typical Development Workflow

1. **Starting development**:
   ```bash
   uv run poe dev
   ```
   Edit code in `./agent` and see changes instantly.

2. **After changing dependencies**:
   ```bash
   uv run poe down
   uv run poe restart
   ```

3. **Testing production build locally**:
   ```bash
   uv run poe build
   uv run poe start
   uv run poe logs
   ```

The API will be available at `http://localhost:8080`.

## Deployment

### Prerequisites

- AWS CLI configured
- AWS CDK installed (`npm install -g aws-cdk`)

### Deploy to AWS

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your-api-key
```

2. Create SSM parameter:
```bash
uv run poe setup-ssm
```

3. Deploy with CDK:
```bash
cdk deploy
```

The stack will output the Lambda function URL and create:
- Lambda function with FastAPI
- DynamoDB table for LangGraph checkpoints
- SSM parameter access permissions

## What This Tutorial Doesn't Cover

This is a starting template to get you up and running quickly. For production, you'll likely want to add:

- Application monitoring and observability (CloudWatch, Datadog, OpenTelemetry)
- LLM ops observability (token tracking, latency monitoring, offline evaluations)
- Strict typing with FastAPI
- Authentication and authorization
- Rate limiting
- Error handling and retry strategies
- Testing (unit, integration, e2e)
- CI/CD pipeline infrastructure
- Multi-environment deployments
- Cost management and budgeting
- API versioning
- CORS configuration
- Custom domains and SSL certificates
- Secrets rotation
- Caching strategies

## License

MIT
