import re
import json
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from . import api
from .input import createInput
import signal
from .tools import read_file, edit_file, run_command
import random
import os

console = Console()
_last_command_cache = {}
_status_list = None
esc_abort = False


def get_random_status():
    global _status_list
    if _status_list is None:
        possible_paths = [
            "statuses.txt",
            os.path.expanduser("~/multicode/statuses.txt")
        ]
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = [line.strip() for line in f if line.strip()]
                        if lines:
                            _status_list = lines
                            break
                except:
                    pass
        
    return random.choice(_status_list)

def run_command_dedupe(command: str, console: Console) -> str:
    global _last_command_cache
    key = command.strip()
    if _last_command_cache.get(key) is not None:
        return f"Skipped repeated command: {key}\nLast output:\n{_last_command_cache[key]}"
    output = run_command(command, console)
    _last_command_cache = {key: output}
    return output

def parse_and_execute(response: str, console: Console) -> str:
    results = []

    minimax_pattern = re.compile(r'minimax:tool_call\s+(.*?)\s*</minimax:tool_call>', re.DOTALL | re.IGNORECASE)
    def handle_minimax(m):
        content = m.group(1).strip()
        if not content:
            return ""
        try:
            data = json.loads(content)
            tool = data.get("name", "").upper()
            args = data.get("arguments", {})
            if tool == "RUN" and "command" in args:
                output = run_command_dedupe(args["command"], console)
                results.append(f"RUN result:\n{output}")
            elif tool == "READ" and "filename" in args:
                content = read_file(args["filename"], console)
                results.append(f"READ result:\n{content}")
            elif tool == "EDIT" and "filename" in args and "content" in args:
                success = edit_file(args["filename"], args["content"], console)
                results.append(f"EDIT result: {'success' if success else 'failed'}")
            else:
                output = run_command_dedupe(content, console)
                results.append(f"RUN result:\n{output}")
        except (json.JSONDecodeError, KeyError):
            output = run_command_dedupe(content, console)
            results.append(f"RUN result:\n{output}")
        return ""
    processed_response = minimax_pattern.sub(handle_minimax, response)

    generic_xml = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL)
    def handle_generic(m):
        content = m.group(1).strip()
        try:
            data = json.loads(content)
            if "command" in data:
                output = run_command_dedupe(data["command"], console)
                results.append(f"RUN result:\n{output}")
            elif "filename" in data:
                content = read_file(data["filename"], console)
                results.append(f"READ result:\n{content}")
            else:
                output = run_command_dedupe(content, console)
                results.append(f"RUN result:\n{output}")
        except:
            output = run_command_dedupe(content, console)
            results.append(f"RUN result:\n{output}")
        return ""
    processed_response = generic_xml.sub(handle_generic, processed_response)

    processed_response = re.sub(r'<[^>]+>', '', processed_response)

    lines = processed_response.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("READ "):
            filename = line[5:].strip()
            content = read_file(filename, console)
            results.append(f"READ result:\n{content}")
            i += 1

        elif line.startswith("EDIT "):
            filename = line[5:].strip()
            i += 1
            if i < len(lines) and lines[i].strip() == "```file":
                i += 1
                content_lines = []
                while i < len(lines) and lines[i].strip() != "```":
                    content_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    i += 1
                content = "\n".join(content_lines)
            else:
                content_lines = []
                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith(("READ ", "EDIT ", "RUN ", "THOUGHT:", "NEXT:")):
                        break
                    content_lines.append(lines[i])
                    i += 1
                content = "\n".join(content_lines)
            success = edit_file(filename, content, console)
            results.append(f"EDIT result: {'success' if success else 'failed'}")

        elif line.startswith("RUN "):
            command = line[4:].strip()
            if any(p in command for p in ['.', ',', '?', '!']) or len(command.split()) == 1 and command.lower() in {'echo', 'ls', 'pwd', 'cat', 'git', 'python', 'pip', 'npm', 'node'}:
                output = run_command_dedupe(command, console)
                results.append(f"RUN result:\n{output}")
            else:
                results.append(line)
            i += 1

        elif line.startswith("THOUGHT:") or line.startswith("NEXT:"):
            results.append(line)
            i += 1

        else:
            if re.match(r'^\s*(?:ls|pwd|cd|cat|echo|git|python|pip|npm|node|mkdir|rm|cp|mv|find|grep)\b', line):
                if not re.search(r'\brm\s+-rf\s+/\b', line):
                    if not any(p in line for p in ['.', ',', '?', '!']) and len(line.split()) <= 5:
                        output = run_command_dedupe(line, console)
                        results.append(f"RUN result:\n{output}")
                    else:
                        results.append(line)
                else:
                    results.append("Skipped dangerous command: " + line)
            else:
                results.append(line)
            i += 1

    return "\n".join(results)

def init():
    console.print("[italic grey50]Initializing...")
    api.load_config()
    if not api.apiKey:
        console.print("[yellow] No API key found. Use /key YOUR_KEY to set it.[/yellow]")
    if not api.modelName:
        console.print("[yellow] No model set. Use /model MODEL_NAME to set it.[/yellow]")
    start()

def start():
    conversation = []
    maxToolCycle = 10

    while True:
        prompt = createInput()
        if not prompt:
            continue

        if prompt == "/exit":
            console.print("[bold grey50]Bye.\n")
            break
        if prompt == "/clear":
            console.clear()
            continue
        if prompt.startswith("/key "):
            new_key = prompt.split(" ", 1)[1]
            api.changeApiKey(new_key)
            console.print("[bold light_green] API Key updated successfully.")
            continue
        if prompt.startswith("/model "):
            new_model = prompt.split(" ", 1)[1]
            api.changeModel(new_model)
            console.print(f"[bold light_green] Model changed to [sky_blue2]{new_model}[/sky_blue2] successfully.")
            continue

        conversation.append({"role": "user", "content": prompt})

        toolCycle = 0
        while True:
            full_prompt = "\n\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in conversation
            ])

            with console.status(f"[bold sky_blue2]{get_random_status()}[/bold sky_blue2]", spinner="line", spinner_style="violet"):
                try:
                    ai_response = api.askModel(full_prompt)
                    
                except Exception as e:
                    console.print(f"[red] API error: {e}[/red]")
                    break

            console.print(Panel(
                Markdown(ai_response),
                border_style="violet",
                title="[bold violet]MultiCode[/bold violet]",
                title_align="left",
            ))

            if any(phrase in ai_response.lower() for phrase in [
                "thought: task completed",
                "next: none",
                "thought: done",
                "thought: finished"
            ]):
                console.print("[green]✓ Task completed. Ready for next request.[/green]")
                conversation.append({"role": "assistant", "content": ai_response})
                break

            tool_output = parse_and_execute(ai_response, console)
            toolCycle += 1

            if tool_output.strip():
                conversation.append({"role": "assistant", "content": ai_response})
                conversation.append({"role": "user", "content": f"Tool output:\n{tool_output}"})
                console.print("[grey50]Continuing with tool results...[/grey50]")
                if toolCycle >= maxToolCycle:
                    console.print("[red] Reached maximum tool cycles. Stopping to prevent loop.[/red]")
                    break
            else:
                conversation.append({"role": "assistant", "content": ai_response})
                break
