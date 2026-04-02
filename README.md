# MultiCode

> Your terminal AI coding buddy – reads files, edits code, runs commands.  
> Free. Works with any model via OpenRouter. Like Claude Code, but open.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)

## What it does

MultiCode is an autonomous AI agent that lives in your terminal. You give it a task (e.g., *"write a calculator app"* or *"fix the bug in auth.py"*), and it:

- **Reads** files from your project
- **Edits** files (with your permission)
- **Runs** terminal commands (you confirm each one)

It keeps working step by step until the job is done – just like a real developer.

## Why MultiCode?

- **Free** – use free models from OpenRouter (DeepSeek, Gemma, Llama, etc.)
- **Any model** – switch between GPT, Claude, Gemini, Qwen, or any OpenRouter model
- **Safe** – commands ask for confirmation, dangerous commands are blocked
- **Transparent** – you see every file read, edit, and command before it runs

## Installation

```bash
curl -sSL https://raw.githubusercontent.com/cry-nix/MultiCode/main/install.sh | bash
