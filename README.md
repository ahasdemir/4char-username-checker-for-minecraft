# Minecraft Username Availability Checker

A Python tool to check the availability of 4-character Minecraft usernames using the official Minecraft API. Find rare, available usernames and export them to CSV files for easy management.

## Features

### 🎯 **Multiple Checking Methods**
- **Specific usernames**: Check usernames you're interested in
- **Random generation**: Generate and check random 4-character combinations
- **Letters-only mode**: Check usernames without numbers for a cleaner look
- **Pattern matching**: Use patterns like "axxx" to check systematic variations

### 📊 **Export & Management**
- **CSV Export**: All results saved to organized CSV files
- **Auto-save**: Emergency save with Ctrl+C to never lose progress
- **Session tracking**: Keep track of all findings across multiple checks
- **Organized storage**: All exports saved to `/export` directory

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup
1. **Clone or download** this repository
2. **Navigate** to the project directory:
   ```bash
   cd 4char-username-checker-for-minecraft
   ```
3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```
4. **Activate the virtual environment**:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application
```bash
python check.py
```

### Menu Options

#### 1. Check Specific Usernames
Enter a comma-separated list of usernames to check:
```
Usernames: test, game, cool, play
```

#### 2. Random 4-Character Usernames (Letters + Numbers)
Generates random combinations using `a-z` and `0-9`:
- Example results: `a3dx`, `m9k2`, `7abc`

#### 3. Random 4-Character Usernames (Letters Only)
Generates random combinations using only `a-z`:
- Example results: `abcd`, `help`, `game`, `cool`

#### 4. Pattern-Based Checking
Use 'x' as wildcards in patterns:
- `axxx` checks: `a000`, `a001`, `a002`, etc.
- `xaxx` checks: `0a00`, `1a01`, `2a02`, etc.

#### 5. Export to CSV
Manually export all found usernames from the current session.

#### 6. View Session Statistics
See all available usernames found in the current session.

#### 7. Exit
Exit the application with optional save prompt.

### Keyboard Shortcuts
- **Ctrl+C**: Emergency save and exit
  - Automatically saves all found usernames to CSV
  - Creates timestamped emergency save file

## Output Files

All CSV files are saved to the `export/` directory:

### File Types
- **Regular exports**: `available_usernames_YYYYMMDD_HHMMSS.csv`
- **Emergency saves**: `emergency_save_YYYYMMDD_HHMMSS.csv`

### CSV Format
```csv
Username,Date_Checked,Status
cool,2025-07-11 18:30:45,Available
game,2025-07-11 18:30:47,Available
```

## API Information

This tool uses the official Minecraft APIs:
- **Primary**: `https://api.minecraftservices.com/minecraft/profile/lookup/name/{username}`
- **Backup**: `https://api.mojang.com/users/profiles/minecraft/{username}`

### Response Codes
- **HTTP 404**: Username is available ✅
- **HTTP 200**: Username is taken ❌
- **Other codes**: API error or rate limiting

## Configuration

### Rate Limiting
- Default delay: 0.5 seconds between requests
- Pattern checking limit: 500 usernames per session
- Modify `time.sleep(0.5)` in the code to adjust

### Character Sets
- **Letters + Numbers**: `abcdefghijklmnopqrstuvwxyz0123456789` (36 chars)
- **Letters Only**: `abcdefghijklmnopqrstuvwxyz` (26 chars)

## Project Structure

```
username-checker/
├── check.py              # Main application
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── README.md            # This documentation
├── .venv/               # Virtual environment (ignored)
└── export/              # CSV exports directory (ignored)
    ├── available_usernames_*.csv
    └── emergency_save_*.csv
```

## Example Session

```
=== Minecraft Username Availability Checker ===
💡 Tip: Press Ctrl+C at any time to save found usernames and exit

Options:
1. Check specific usernames
2. Check random 4-character usernames (letters + numbers)
3. Check random 4-character usernames (letters only)
4. Check usernames with pattern
5. Export all available usernames to CSV
6. View current session statistics
7. Exit

Enter your choice (1-7): 3
How many random usernames to check? (default 20): 10

Checking 10 random 4-character usernames (letters only)...
----------------------------------------
abcd - not available ✗
help - not available ✗
cool - available ✓
game - not available ✗
test - not available ✗
...
----------------------------------------
Summary: 1 available, 9 taken

Available usernames found:
  cool

Export available usernames to CSV? (y/n): y
✓ Exported 1 available usernames to 'export/available_usernames_20250711_183045.csv'
```
## License

This project is provided as-is for educational and personal use. Please respect Minecraft's Terms of Service and API usage guidelines.

## Disclaimer

- This tool is for checking username availability only
- Respect Minecraft's API rate limits
- Available usernames may be claimed by others quickly
- No guarantee that "available" usernames can actually be claimed

---

**Happy username hunting!** 🎮✨
