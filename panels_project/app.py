import uvicorn

from modules.sentry.sentry import run_sentry
from panels_project.admin_dashboard_app import app_admin_dashboard
from panels_project.users_dashboard import app_users_dashboard as app

app.mount('/admin', app_admin_dashboard)
run_sentry()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
