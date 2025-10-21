module.exports = {
  apps: [
    {
      name: 'mesh-api',
      script: '/home/appuser/.local/bin/uv',
      args: 'run python -m uvicorn mesh.mesh_api:app --host 0.0.0.0 --port 8800',
      cwd: '/home/appuser/heurist-agent-framework',
      interpreter: 'none',
      autorestart: true,
      max_memory_restart: '2G',
      max_restarts: 10,
      min_uptime: '10s',
      error_file: '/home/appuser/heurist-agent-framework/mesh/logs/mesh-api-error.log',
      out_file: '/home/appuser/heurist-agent-framework/mesh/logs/mesh-api-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      env: {
        NODE_ENV: 'production',
        PYTHONUNBUFFERED: '1'
      },
      merge_logs: true,
      listen_timeout: 5000,
      kill_timeout: 5000
    }
  ]
};
