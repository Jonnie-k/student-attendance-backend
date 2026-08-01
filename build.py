"""
Vercel build script.

Runs automatically during every Vercel deployment (after dependencies are
installed, before the app goes live). We use it to apply database
migrations -- this project's own Postgres database only needs to hold
Django's auth/session tables (login credentials for this dashboard),
separate from the backend API's database.

Requires the DATABASE_URL env var to be available at *build* time in your
Vercel project settings (Settings -> Environment Variables -> make sure it's
enabled for the environment you're deploying, e.g. Production).
"""

import subprocess
import sys


def main():
    print("Running database migrations...")
    subprocess.run(
        [sys.executable, "manage.py", "migrate", "--noinput"],
        check=True,
    )


if __name__ == "__main__":
    main()
