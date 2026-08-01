"""
Vercel build script.

Runs automatically during every Vercel deployment (after dependencies are
installed, before the app goes live). We use it to apply database
migrations so a fresh Postgres database is always up to date -- static
files are collected by Vercel itself and don't need to be handled here.

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
