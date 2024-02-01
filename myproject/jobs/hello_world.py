#!/usr/bin/env python3

import sys
import anyio
import dagger


async def test():
    config = dagger.Config(log_output=sys.stderr)
    async with dagger.Connection(config) as client:
        python = (
            client.container()
            .from_("python:3.12-slim")
            .with_exec(["python", "--version"])
        )

        version = await python.stdout()

    print(f"Hello from Dagger and {version}")


anyio.run(test)
