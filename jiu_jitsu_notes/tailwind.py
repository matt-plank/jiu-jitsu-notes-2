import subprocess

TAILWIND_OUTPUT: str = "templates/css/tailwind.css"


def build_css():
    subprocess.Popen(
        [
            "tailwindcss",
            "-o",
            TAILWIND_OUTPUT,
        ]
    )
