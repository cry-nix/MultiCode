from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import os

console = Console()
session = PromptSession()

prompt_style = Style.from_dict({
    "prompt": "bold ansicyan",
})

header = Panel(
    "[bold violet]Multi[/bold violet][bold sky_blue2]Code[/bold sky_blue2][italic grey50]  Welcome to MultiCode![/italic grey50]",
    border_style="bright_black",
)
console.print(header)
console.print("""[bold violet]███╗   ███╗██╗   ██╗██╗  ████████╗██╗[/bold violet][bold sky_blue2] ██████╗ ██████╗ ██████╗ ███████╗[/bold sky_blue2]
[bold violet]████╗ ████║██║   ██║██║  ╚══██╔══╝██║[/bold violet][bold sky_blue2]██╔════╝██╔═══██╗██╔══██╗██╔════╝[/bold sky_blue2]
[bold violet]██╔████╔██║██║   ██║██║     ██║   ██║[/bold violet][bold sky_blue2]██║     ██║   ██║██║  ██║█████╗[/bold sky_blue2]  
[bold violet]██║╚██╔╝██║██║   ██║██║     ██║   ██║[/bold violet][bold sky_blue2]██║     ██║   ██║██║  ██║██╔══╝[/bold sky_blue2]  
[bold violet]██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║[/bold violet][bold sky_blue2]╚██████╗╚██████╔╝██████╔╝███████╗[/bold sky_blue2]
[bold violet]╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝[/bold violet][bold sky_blue2] ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝[/bold sky_blue2]
""")
console.print("[bold bright_black]─────────────────────────────────────────────────────[/bold bright_black]")
console.print("  [bold sky_blue2]Tips[/bold sky_blue2]")
console.print("  [grey50]Try asking:")
console.print("  [violet]❯[/violet] [white]Read [bold sky_blue2]@filename[/bold sky_blue2] and explain what it does[/white]")
console.print("  [violet]❯[/violet] [white]Add error handling to [bold sky_blue2]@filename[/bold sky_blue2][/white]")
console.print("  [violet]❯[/violet] [white]Refactor this project to use async[/white]")
console.print("  [violet]❯[/violet] [white]Find and fix the bug in [bold sky_blue2]@filename[/bold sky_blue2][/white]")
console.print("[bold bright_black]─────────────────────────────────────────────────────[/bold bright_black]")
console.print()

console.print("[grey50]  try: [sky_blue2]read [bold violet]@filename[/bold violet] and explain it[/sky_blue2]  [grey50]•  [sky_blue2]fix the bug in [bold violet]@filename[/bold violet]  [grey50]•  [sky_blue2]add logging[/sky_blue2]\n")

console.print("  [bold bright_black]/key[/bold bright_black] [grey50]set api key   [bold bright_black]/model[/bold bright_black] [grey50]switch model   [bold bright_black]/clear[/bold bright_black] [grey50]clear screen   [bold bright_black]/exit[/bold bright_black] [grey50]quit\n")

console.print(f"[grey50]Current Directory: {os.getcwd()}[/grey50]")


def createInput():
    console.print(Panel(
        Text.assemble(("❯ ", "bold sky_blue2"), ("", "white")),
        border_style="bright_black",
        padding=(0, 1),
    ))

    print("\033[2A\033[4C", end="", flush=True)

    text = session.prompt("", style=prompt_style).strip()

    console.print(Panel(
        Text.assemble(("❯ ", "bold violet"), (text, "white")),
        border_style="bright_black",
        padding=(0, 1),
    ))

    return text
