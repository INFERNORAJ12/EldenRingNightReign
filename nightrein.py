import os
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# Path for persistent config
CONFIG_DIR = r"C:\LETTHENIGGAKNOW"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Ensure folder exists
os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def select_ini_file():
    messagebox.showinfo("Step 1: Select INI File", "Select 'nrsc_settings.ini' inside SeamlessCoop folder.")
    return filedialog.askopenfilename(
        title="Select nrsc_settings.ini",
        filetypes=[("INI files", "*.ini")]
    )

def update_player_count(ini_path, player_count):
    try:
        with open(ini_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        found = False
        updated_lines = []
        for line in lines:
            if line.strip().startswith("player_count ="):
                updated_lines.append(f"player_count = {player_count}\n")
                found = True
            else:
                updated_lines.append(line)

        if not found:
            messagebox.showerror("Error", "Could not find 'player_count =' in the INI file.")
            return False

        with open(ini_path, 'w', encoding='utf-8') as file:
            file.writelines(updated_lines)

        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update INI:\n{e}")
        return False

def get_launcher_and_dll(ini_path):
    seamless_dir = os.path.dirname(ini_path)  # SeamlessCoop/
    game_dir = os.path.dirname(seamless_dir)  # Game/
    launcher = os.path.join(game_dir, "nrsc_launcher.exe")
    dll = os.path.join(seamless_dir, "nrsc.dll")
    return launcher, dll

def run_as_admin(exe_path):
    try:
        subprocess.run([
            "powershell", "-Command",
            f'Start-Process \"{exe_path}\" -WorkingDirectory \"{os.path.dirname(exe_path)}\" -Verb RunAs'
        ], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch launcher:\n{e}")

def handle_player_count(player_count):
    config = load_config()
    ini_path = config.get("ini_path")

    if not ini_path or not os.path.exists(ini_path):
        ini_path = select_ini_file()
        if not ini_path:
            messagebox.showwarning("Cancelled", "No INI file selected.")
            return
        config["ini_path"] = ini_path
        save_config(config)

    launcher_path, dll_path = get_launcher_and_dll(ini_path)

    if not os.path.exists(launcher_path):
        messagebox.showerror("Missing", f"Launcher not found at:\n{launcher_path}")
        return

    if not os.path.exists(dll_path):
        messagebox.showerror("Missing", f"nrsc.dll not found at:\n{dll_path}")
        return

    if update_player_count(ini_path, player_count):
        messagebox.showinfo("Success", f"Player count set to {player_count}. Launching...")
        run_as_admin(launcher_path)

def main():
    root = tk.Tk()
    root.title("Elden Ring Coop Launcher")
    root.geometry("320x250")
    root.configure(bg="#1e1e1e")
    root.resizable(False, False)

    label = tk.Label(
        root,
        text="Choose Player Count",
        font=("Segoe UI", 14, "bold"),
        bg="#1e1e1e",
        fg="white"
    )
    label.pack(pady=20)

    def styled_button(text, count, color):
        return tk.Button(
            root,
            text=text,
            font=("Segoe UI", 12),
            width=20,
            bg=color,
            fg="white",
            activebackground="#444",
            activeforeground="white",
            relief="raised",
            bd=2,
            command=lambda: handle_player_count(count)
        )

    styled_button("1 Player", 1, "#0078D7").pack(pady=5)
    styled_button("2 Players", 2, "#28a745").pack(pady=5)
    styled_button("3 Players", 3, "#e69500").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
