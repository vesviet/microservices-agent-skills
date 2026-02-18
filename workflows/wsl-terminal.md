---
description: How to use WSL terminal instead of default PowerShell
---

# Using WSL Terminal

## Quick Command Prefix
To run any command through WSL instead of PowerShell, simply prefix with `wsl`:

```bash
wsl ls -la
wsl cd /mnt/d/microservices && git status
wsl bash script.sh
```

## VS Code Configuration
To set WSL as the default terminal in VS Code, update `.vscode/settings.json`:

```json
{
  "terminal.integrated.defaultProfile.windows": "WSL"
}
```

Or specify a specific WSL distribution:

```json
{
  "terminal.integrated.defaultProfile.windows": "Ubuntu",
  "terminal.integrated.profiles.windows": {
    "Ubuntu": {
      "path": "wsl.exe",
      "args": ["-d", "Ubuntu"]
    }
  }
}
```

## Path Mapping
Windows paths are mounted under `/mnt/` in WSL:
- `D:\microservices` → `/mnt/d/microservices`
- `C:\Users\vesvi` → `/mnt/c/Users/vesvi`

## Common Use Cases

### 1. Run bash scripts
```bash
wsl bash git-all.sh
```

### 2. Use Linux commands
```bash
wsl grep -r "pattern" .
wsl find . -name "*.js"
wsl chmod +x script.sh
```

### 3. Access Linux environment
```bash
wsl
# Now you're in Linux shell, can run any Linux commands
```

### 4. Run with specific distribution
```bash
wsl -d Ubuntu bash script.sh
wsl -d Debian ls
```

## Tips
- Use `wsl --list` to see all installed distributions
- Use `wsl --set-default <DistroName>` to set default distribution
- Use `wsl ~` to start in Linux home directory
- Use `exit` to return to PowerShell from WSL
