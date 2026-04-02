import os
import subprocess
import re
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

def read_file(filename: str, console: Console) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        console.print(f"[green]Read {filename} ({len(content)} characters)[/green]")
        return content
    except FileNotFoundError:
        console.print(f"[red]File not found: {filename}[/red]")
        return ""
    except Exception as e:
        console.print(f"[red]Error reading {filename}: {e}[/red]")
        return ""

def edit_file(filename: str, content: str, console: Console) -> bool:
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[green]Written to {filename} ({len(content)} characters)[/green]")
        return True
    except Exception as e:
        console.print(f"[red]Error writing {filename}: {e}[/red]")
        return False

def replace_in_file(filename: str, old_str: str, new_str: str, console: Console) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        if old_str not in content:
            console.print(f"[red]Old string not found in {filename}[/red]")
            return "Failed: The exact old_str was not found in the file. Check indentation and whitespace carefully."
        
        if content.count(old_str) > 1:
            console.print(f"[yellow]Warning: old_str found multiple times in {filename}. Replace all occurrences.[/yellow]")
        
        new_content = content.replace(old_str, new_str)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        console.print(f"[green]Applied replacement in {filename}[/green]")
        return f"Successfully replaced text in {filename}."
    except FileNotFoundError:
        console.print(f"[red]File not found: {filename}[/red]")
        return f"Failed: File {filename} not found."
    except Exception as e:
        console.print(f"[red]Error in replace_in_file: {e}[/red]")
        return f"Failed: {str(e)}"

def list_dir(path: str, console: Console) -> str:
    try:
        items = os.listdir(path)
        dirs = [f"{x}/" for x in items if os.path.isdir(os.path.join(path, x))]
        files = [x for x in items if os.path.isfile(os.path.join(path, x))]
        result = "Directories: \n" + "\n".join(sorted(dirs)) if dirs else "Directories: (none)"
        result += "\nFiles: \n" + "\n".join(sorted(files)) if files else "\nFiles: (none)"
        console.print(f"[green]Listed {path}[/green]")
        return result
    except FileNotFoundError:
        console.print(f"[red]Directory not found: {path}[/red]")
        return f"Error: Path {path} not found."
    except Exception as e:
        console.print(f"[red]Error listing directory: {e}[/red]")
        return f"Error: {str(e)}"

def grep_search(pattern: str, path: str, console: Console) -> str:
    try:
        matches = []
        target_path = path if os.path.exists(path) else "."
        if os.path.isfile(target_path):
            with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    if re.search(pattern, line):
                        matches.append(f"L{i}: {line.rstrip()}")
        else:
            for root, _, files in os.walk(target_path):
                # Skip common ignored directories
                if any(d in root for d in [".git", "node_modules", "__pycache__", ".venv", "env"]):
                    continue
                for file in files:
                    if not file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.json', '.md', '.yaml', '.yml', '.txt', '.sh', '.toml')):
                        continue
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            for i, line in enumerate(f, 1):
                                if re.search(pattern, line, re.IGNORECASE):
                                    rel_path = os.path.relpath(full_path, ".")
                                    matches.append(f"{rel_path}:L{i}: {line.rstrip()}")
                    except Exception:
                        pass
        
        if not matches:
            console.print(f"[yellow]No matches found for '{pattern}' in {path}[/yellow]")
            return f"No matches found for pattern '{pattern}' in {path}."
        
        result = "\n".join(matches[:50])
        if len(matches) > 50:
            result += f"\n... ({len(matches) - 50} more matches)"
        console.print(f"[green]Found {len(matches)} matches for '{pattern}'[/green]")
        return result
    except Exception as e:
        console.print(f"[red]Error in grep search: {e}[/red]")
        return f"Error: {str(e)}"

def run_command(command: str, console: Console) -> str:
    console.print(Panel(
        f"[white]{command}[/white]",
        title="[bold yellow]RUN[/bold yellow]",
        border_style="yellow"
    ))
    if not Confirm.ask("Execute this command?", default=False):
        console.print("[grey]Command cancelled.[/grey]")
        return "Command cancelled by user."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout + result.stderr
        console.print("[green]Command executed.[/green]")
        return output
    except subprocess.TimeoutExpired:
        console.print("[red]Command timed out after 60 seconds.[/red]")
        return "Command timed out."
    except Exception as e:
        console.print(f"[red]Error running command: {e}[/red]")
        return f"Error: {e}"