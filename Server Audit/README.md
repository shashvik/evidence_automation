# 🛡️ Server Audit Tool

This tool allows you to SSH into a Linux server using a `.pem` key, elevate to `sudo`, execute a series of predefined security audit commands, and capture the terminal output as timestamped images.

---

## 📂 Project Structure

```
Server Audit/
│
├── server_commands.py        # Main script for SSH, sudo execution, and screenshot generation
├── commands.json             # JSON file with key-value pairs of audit commands
├── screenshots/              # Output folder where images are saved
└── mypem.pem                 # (User-provided) SSH private key file
```

---

## 🚀 Features

- Secure SSH connection using `.pem` key
- Automatic sudo elevation for privileged commands
- Executes custom commands from a JSON config
- Captures terminal output and renders it into images
- Adds a real-time timestamp with a black background
- Saves results as `.png` images, one per command

---

## 📋 Requirements

- Python 3.6+
- `paramiko`
- `Pillow`
- `opencv-python`
- `numpy`

Install dependencies:
```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```txt
paramiko
Pillow
opencv-python
numpy
```

---

## ⚙️ Usage

1. **Prepare your files:**
   - Ensure `mypem.pem` (your SSH key) is accessible.
   - Modify `commands.json` with the Linux audit commands you want to run.

2. **Run the tool:**
   ```bash
   python server_commands.py
   ```

3. **Output:**
   - Each command output is saved as a `.png` file in the `screenshots/` directory.
   - Images include the command run, its output, and a timestamp.

---

## 🛠️ Example `commands.json`

```json
{
    "etc_user": "TERM=dumb grep '^' /etc/passwd",
    "shadow": "TERM=dumb grep '^' /etc/shadow",
    "Current OS Version": "TERM=dumb cat /etc/os-release",
    "Max 90 Days Policy": "TERM=dumb grep 'PASS_MAX_DAYS' /etc/login.defs",
    "ClientAliveInterval": "TERM=dumb grep -i 'ClientAliveInterval' /etc/ssh/sshd_config"
}
```

> Commands are prefixed with `TERM=dumb` to avoid formatting issues caused by terminal capabilities.

---

## 📸 Screenshot Example

Each image contains:
- Simulated terminal prompt: `root@<hostname>:~# <command>`
- Command output (with `[Output Truncated]` if too long)
- Timestamp (bottom right)

---

## 🔐 Notes

- Make sure your SSH key has the correct permissions (`chmod 400 mypem.pem`).
- For security reasons, be cautious with the commands listed in `commands.json`.
- Ensure you have `sudo` privileges on the target server.

---

## ✅ Use Cases

- Automated server auditing
- Baseline configuration capture
- Evidence collection for compliance
- Snapshotting before/after security hardening
