module.exports = {
  apps: [
    {
      name: 'trending-tokens-scraper',
      script: 'xvfb-run',
      args: '-a uv run python /home/appuser/heurist-agent-framework/mesh/cron/trending_tokens_scraper.py',
      interpreter: 'bash',
      cron_restart: '0 */6 * * *',  // Run every 6 hours
      autorestart: true,  // Auto-restart to keep process managed by PM2
      max_memory_restart: '1G',
      error_file: '/home/appuser/heurist-agent-framework/mesh/cron/logs/trending-tokens-error.log',
      out_file: '/home/appuser/heurist-agent-framework/mesh/cron/logs/trending-tokens-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      env: {
        NODE_ENV: 'production',
        PYTHONUNBUFFERED: '1'
      }
    }
  ]
};
