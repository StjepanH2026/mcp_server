# Render Deployment Activity for FastAPI + FastMCP

This activity documents how to deploy the FastAPI + FastMCP server in this repository to Render.

Deploy the existing ASGI app to Render so the following endpoints are publicly reachable:

- `/`
- `/health`
- `/docs`
- `/mcp/`

## Entrypoint

This repository does **not** use `main:app`.

The correct ASGI app import path for Render is:

```bash
converter_streamable_http_server:app
```

Source file:

- `converter_streamable_http_server.py`

## Checklist

We are using:

- `converter_streamable_http_server.py`
- `requirements.txt`

Check the Python dependencies:

- `fastapi`
- `fastmcp`
- `uvicorn`

## Local test first

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the server locally:

```bash
uvicorn converter_streamable_http_server:app --host 127.0.0.1 --port 8003
```

Check the URLs locally:

```text
http://localhost:8003/
http://localhost:8003/health
http://localhost:8003/docs
http://localhost:8003/mcp/
```

Results:

- `/` returns a small JSON service document
- `/health` returns JSON with `"status": "ok"`
- `/docs` loads Swagger UI
- `/mcp/` responds as the MCP streamable HTTP endpoint

Notes:

- The MCP endpoint should be tested with `/mcp/` including the trailing slash.

## GitHub Preparation

Push the current repository state to GitHub:

```bash
git add .
git commit -m "feat: prepare FastAPI MCP app for deployment"
git push
```

Do not commit `.env`. It is already ignored by `.gitignore`.

## Render Service Setup

In Render:

1. Create a new `Web Service`
2. Connect the GitHub repository
3. Choose `Python 3`
4. Configure the service with the following values

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
uvicorn converter_streamable_http_server:app --host 0.0.0.0 --port $PORT
```

Recommended Health Check Path:

```text
/health
```

- Render requires the app to bind to `0.0.0.0`
- Render injects the app port through `$PORT`
- The ASGI app is exported from `converter_streamable_http_server.py`

## Environment Variables

Add only the environment variables your deployed service actually needs.

Optional variables used elsewhere in the repo include:

```text
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
MCP_SERVER_URL=https://your-service-name.onrender.com/mcp
```

**Important:**

- `GEMINI_API_KEY` is used by `gemini_client/simulated_gemini_client.py`, not by the FastAPI server startup path itself
- Store secrets in Render environment variables, not in the repository

## Deploy

Create the web service in Render and wait for the first build to complete.

After deployment, Render will assign a URL similar to:

```text
https://your-service-name.onrender.com
```

## Post-Deployment test

Test these URLs:

```text
https://your-service-name.onrender.com/
https://your-service-name.onrender.com/health
https://your-service-name.onrender.com/docs
https://your-service-name.onrender.com/mcp/
```

Expected results:

- `/` returns a small JSON service document
- `/health` returns a successful JSON response
- `/docs` loads successfully
- `/mcp/` is reachable for MCP clients

## Successful Deployment Record

This deployment flow was completed successfully for this repository.

### Git commands used

```bash
git status --short
git add converter_streamable_http_server.py utils/resource_utils.py render.yaml docs/activities/render_fastapi_mcp_deployment.md
git commit -m "Prepare FastAPI MCP server for Render deployment"
git push
```

Notes:

- this staged only the intended deployment files

### Render settings that worked

- Service type: `Web Service`
- Runtime: `Python`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn converter_streamable_http_server:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/health`

### Deployed endpoint checks

The following URLs were used as the post-deploy checks:

```text
https://<your-service>.onrender.com/
https://<your-service>.onrender.com/health
https://<your-service>.onrender.com/docs
https://<your-service>.onrender.com/mcp/
```

## Troubleshooting

If the deploy fails to start:

- confirm the start command uses `converter_streamable_http_server:app`
- confirm `requirements.txt` contains all required packages
- confirm the service binds with `--host 0.0.0.0 --port $PORT`

If `/docs` works but `/mcp/` does not:

- check Render logs for startup errors
- confirm the MCP app is mounted at `/mcp`
- test with a trailing slash: `/mcp/`

If logs are noisy on startup:

- confirm the latest deployment includes the resource logging cleanup described below
- check Render logs for application exceptions instead of import-time debug output

## Free Tier Notes

Render’s current free web service limitations include:

- services spin down after 15 minutes of inactivity
- cold starts can take about a minute
- free usage is limited to 750 instance hours per calendar month
- local filesystem changes are ephemeral

This is acceptable for demos, labs, and teaching activities, but not ideal for always-on production use.

## Deployment Changes

### 1. Added a root `/` route

File changed:

- `converter_streamable_http_server.py`

What changed:

- added a `GET /` endpoint that returns a small JSON response
- included links to `/docs`, `/health`, and `/mcp/`

Why:

- Render deployments are easier to sanity-check when the root URL responds successfully
- this provides a simple human-readable homepage for demos and quick smoke tests

### 2. Added a `render.yaml` blueprint

File changed:

- `render.yaml`

- added:
  - service type `web`
  - runtime `python`
  - build command `pip install -r requirements.txt`
  - start command `uvicorn converter_streamable_http_server:app --host 0.0.0.0 --port $PORT`
  - health check path `/health`

Why:

- the deployment settings now live in the repository
- this makes the Render configuration reusable and less error-prone

## Official References

- Render FastAPI deployment docs: `https://render.com/docs/deploy-fastapi`
- Render web services docs: `https://render.com/docs/web-services/`
- Render environment variables docs: `https://render.com/docs/configure-environment-variables`
- Render free tier docs: `https://render.com/docs/free`
