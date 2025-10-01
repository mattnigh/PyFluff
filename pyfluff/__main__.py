"""
Main entry point for PyFluff server module.

Run with: python -m pyfluff.server
"""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "pyfluff.server:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=False,
    )
