import os
import sys
import json
import subprocess

dir_name = os.path.dirname(os.path.abspath(__file__))

# hard code some default applications
applications = [
    "Google Chrome",
    "iTerm2",
    "Discord",
    "Slack",
    "WhatsApp",
    "Safari",
    "app_mode_loader",  # this is the PWA laucher for chrome
]

# parse apps.txt if exists
apps_filename = f"{dir_name}/apps.txt"
if os.path.exists(apps_filename):
    with open(apps_filename, "r") as f:
        applications = f.read().split("\n")


def run_apple_script(cmd):
    # fun a given script, return result
    proc = subprocess.Popen(
        ["osascript", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate(input=cmd.encode("utf-8"))
    return out.decode("utf-8").strip()


def get_screen_resolution():
    # get resolutoin in wxh format
    cmd = """
        tell application "Finder"
            set screen_resolution to bounds of window of desktop
        end tell
    """
    output = run_apple_script(cmd)
    return output.replace(", ", "x").replace("0x0x", "")


resolution = get_screen_resolution()
config_dir_name = f"{dir_name}/layout-configs/{resolution}/"


def save_config(config_id):
    current_state = {}
    for app in applications:
        app = app.strip()
        if not app:
            continue
        cmd = f"""
            tell application "System Events" to tell process "{app}"
                {{position, size}} of window 1
            end tell
        """
        output = run_apple_script(cmd)
        if output:
            x, y, w, h = output.split(", ")
            # TODO only keeping track of the first window for now
            current_state[app] = [{"x": x, "y": y, "w": w, "h": h}]
        else:
            print(f"Failed to detect window state for {app}")
    # save the state to the config file
    filename = config_dir_name + config_id
    os.makedirs(config_dir_name, exist_ok=True)
    if os.path.exists(filename):
        res = input(
            f"Config {config_id} for {resolution} already exists. Overwrite? [y/n]"
        )
        if not res.lower().startswith("y"):
            return False
    with open(filename, "w+") as f:
        json.dump(current_state, f, indent=2)


def apply_config(config_id):
    # apply the state from config file
    filename = config_dir_name + config_id
    if not os.path.exists(filename):
        print(f"Config {config_id} for {resolution} doesn't exist.")
        return False
    with open(filename, "r") as f:
        state = json.load(f)
    for app in applications:
        app = app.strip()
        if not app:
            continue
        if app not in state or not state[app]:
            print(f"No state found for {app}")
            continue
        # TODO only care about the first window for now
        app_state = state[app][0]
        if (
            "x" not in app_state
            or "y" not in app_state
            or "w" not in app_state
            or "h" not in app_state
        ):
            print(f"Invalid state for {app} found in {filename}")
            continue
        cmd = f"""
            tell application "System Events" to tell process "{app}"
                tell window 1
                    set size to {{{app_state['w']}, {app_state['h']}}}
                    set position to {{{app_state['x']}, {app_state['y']}}}
                end tell
            end tell
        """
        output = run_apple_script(cmd)
        print(f"Applied layout for {app}")


def main():
    if len(sys.argv) < 2:
        print("Usage:\n  python main.py [apply | save | windows ] <config_id>")
        return
    config_id = sys.argv[2] if len(sys.argv) == 3 else "default"

    # apply state
    if sys.argv[1].lower().startswith("a"):
        apply_config(config_id)
        return

    # save state
    if sys.argv[1].lower().startswith("s"):
        save_config(current_state, config_id)
        return

    # list all windows
    if sys.argv[1].lower().startswith("w"):
        cmd = """
            tell application "System Events" to get the name of every process where background only is false
        """
        print(run_apple_script(cmd).replace(", ", "\n"))
        return


if __name__ == "__main__":
    main()
