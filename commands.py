import re

def compile_command(command:str, *flags) -> re.Pattern:
    return re.compile(f"^[/]*{command}$", *flags)

VISTE = compile_command("viste", re.I)
