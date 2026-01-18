"""CLI entry point for the brief agent."""

import argparse
import sys
from datetime import datetime

from .core import Agent


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="brief-agent",
        description="AI agent that generates daily company briefs from news and IR releases.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Generate a company brief")
    run_parser.add_argument(
        "--ticker",
        "-t",
        required=True,
        help="Stock ticker symbol (e.g., NOKIA.HE)",
    )
    run_parser.add_argument(
        "--date",
        "-d",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date for the brief (YYYY-MM-DD, default: today)",
    )
    run_parser.add_argument(
        "--mode",
        "-m",
        choices=["demo", "openai", "anthropic", "gemini"],
        default="demo",
        help="LLM mode (default: demo)",
    )
    run_parser.add_argument(
        "--output-dir",
        "-o",
        default="output",
        help="Output directory (default: output)",
    )

    # UI command
    ui_parser = subparsers.add_parser("ui", help="Start the web interface")
    ui_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)",
    )
    ui_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == "run":
        return run_brief(args)

    if args.command == "ui":
        return run_ui(args)

    return 0


def run_ui(args) -> int:
    """Start the web UI."""
    try:
        import uvicorn

        print(f"🚀 Starting UI at http://{args.host}:{args.port}")
        uvicorn.run("brief_agent.api:app", host=args.host, port=args.port, reload=True)
        return 0
    except ImportError:
        print("❌ Error: 'uvicorn' not found. Please run 'pip install uvicorn'")
        return 1
    except Exception as e:
        print(f"❌ Error starting UI: {e}")
        return 1


def run_brief(args) -> int:
    """Execute the brief generation."""
    print(f"🚀 Starting brief generation for {args.ticker} on {args.date}")
    print(f"   Mode: {args.mode}")

    try:
        agent = Agent(mode=args.mode)
        result = agent.run(ticker=args.ticker, date=args.date)

        if result:
            md_path, json_path = result
            print("\n✅ Brief generated successfully!")
            print(f"   📄 Markdown: {md_path}")
            print(f"   📊 JSON: {json_path}")
            return 0
        else:
            print("\n❌ Brief generation failed. Check logs for details.")
            return 1

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
