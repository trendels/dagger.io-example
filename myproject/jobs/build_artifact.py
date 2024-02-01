#!/usr/bin/env python3

import sys
import anyio
import dagger


async def test():
    config = dagger.Config(log_output=sys.stderr)
    async with dagger.Connection(config) as client:
        build = (
            client.container()
            .from_("python:3.11-slim")
            .with_directory("/src", client.host().directory("."))
            .with_workdir("/src")
            .with_mounted_cache(
                "/root/.cache/pip", client.cache_volume("pip-cache-python-3.11")
            )
            .with_exec(["pip", "install", "-r", "requirements.txt"])
            .with_exec(["pip", "wheel", "-w", "wheels", "."])
        )

        await build.directory("wheels").export("./wheels")


anyio.run(test)
