#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run FastAPI client with Uvicorn.
TODO: Run front client as well once it's implemented.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("back.api_client:app", reload=True, log_level="debug")
