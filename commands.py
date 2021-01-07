import re

def compile_command(command, *flags):
    return re.compile(f"^[/]*{command}$", *flags)

VISTE = compile_command("viste", re.I)
