import asyncio
import json
import os
import time
from typing import Any, Dict, Optional

from mcp import ClientSession
from mcp.client.sse import sse_client


async def call_mcp_tool(tool_name: str, payload: dict, retries=3, timeout=10):

    mcp_url = os.getenv("MCP_SERVER_URL", "http://mcp_server:8001")

    attempt = 0
    last_error: Optional[str] = None

    while attempt < retries:
        start_time = time.time()

        try:
            async with sse_client(f"{mcp_url}/sse") as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await asyncio.wait_for(
                        session.call_tool(tool_name, payload),
                        timeout=timeout,
                    )

                    latency_ms = round((time.time() - start_time) * 1000, 2)
                    raw = result.content[0].text.strip()

                    try:
                        parsed = json.loads(raw)
                    except (json.JSONDecodeError, TypeError):
                        parsed = raw

                    return {
                        "status": "success",
                        "tool": tool_name,
                        "attempt": attempt + 1,
                        "latency_ms": latency_ms,
                        "data": parsed,
                    }

        except asyncio.TimeoutError:
            last_error = f"timeout after {timeout}s"
        except Exception as exc:
            last_error = str(exc)

        attempt += 1
        await asyncio.sleep(attempt)

    return {
        "status": "failed",
        "tool": tool_name,
        "attempt": attempt,
        "error": last_error,
    }
