#!/usr/bin/env python3

import sys
import time
import anyio
import dagger


async def main():
    config = dagger.Config(log_output=sys.stderr)
    async with dagger.Connection(config) as client:
        db_server = (
            client.container()
            .from_("postgres:16")
            .with_env_variable("POSTGRES_USER", "my_user")
            .with_env_variable("POSTGRES_PASSWORD", "my_password")
            .with_env_variable("POSTGRES_DB", "my_db")
            .with_exposed_port(5432)
            .as_service()
        )

        http_server = (
            client.container()
            .from_("python:3.11-slim")
            .with_directory("/server", client.host().directory("server"))
            .with_workdir("/server")
            .with_exec(["./run.sh"])
            .with_exposed_port(8080)
            .as_service()
        )

        python = (
            client.container()
            .from_("python:3.11-slim")
            .with_service_binding("db", db_server)
            .with_service_binding("server", http_server)
            .with_directory("/src", client.host().directory("."))
            .with_workdir("/src")
            .with_mounted_cache(
                "/root/.cache/pip", client.cache_volume("pip-cache-python-3.11")
            )
            .with_env_variable("FORCE_COLOR", "1")
            .with_exec(["pip", "install", "-r", "requirements.txt"])
            .with_env_variable("CACHE_BUSTER", str(time.time()))
            .with_exec(["pytest", "-v", "tests/test_integration.py"])
        )

        await python.sync()


anyio.run(main)
