import requests
import string
import itertools
import time
import json
import csv
import os
import signal
import sys
from datetime import datetime
from typing import List, Tuple

class MinecraftUsernameChecker:
    def __init__(self):
        # Primary API endpoint (more reliable)
        self.api_url = "https://api.minecraftservices.com/minecraft/profile/lookup/name/{}"
        # Backup API endpoint (from your screenshot)
        self.backup_api_url = "https://api.mojang.com/users/profiles/minecraft/{}"
        # Track all available usernames found during session
        self.available_usernames = []
        
        # Set up keyboard interrupt handler
        signal.signal(signal.SIGINT, self.handle_interrupt)
        
    def handle_interrupt(self, signum, frame):
        """Handle Ctrl+C interrupt - save usernames and exit gracefully"""
        print("\n\n🛑 Interrupted! Saving available usernames before exit...")
        
        if self.available_usernames:
            print(f"Found {len(self.available_usernames)} available usernames in this session:")
            for username in self.available_usernames:
                print(f"  {username}")
            
            # Auto-save to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"emergency_save_{timestamp}.csv"
            
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Username', 'Date_Checked', 'Status', 'Save_Type'])
                    
                    for username in self.available_usernames:
                        writer.writerow([username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Available', 'Emergency_Save'])
                
                print(f"✓ Emergency save completed: '{filename}'")
            except Exception as e:
                print(f"❌ Error during emergency save: {e}")
        else:
            print("No available usernames found in this session.")
        
        print("Goodbye! 👋")
        sys.exit(0)
        
    def export_to_csv(self, filename: str = None):
        """Export all available usernames found to a CSV file"""
        if not self.available_usernames:
            print("No available usernames to export.")
            return
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"available_usernames_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Username', 'Date_Checked', 'Status'])
                
                for username in self.available_usernames:
                    writer.writerow([username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Available'])
            
            print(f"✓ Exported {len(self.available_usernames)} available usernames to '{filename}'")
            return filename
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None
        
    def check_username(self, username: str) -> Tuple[str, bool]:
        """
        Check if a username is available.
        Returns tuple of (username, is_available)
        """
        try:
            # Try primary API first
            response = requests.get(self.api_url.format(username), timeout=5)
            
            if response.status_code == 404:
                return (username, True)  # Available
            elif response.status_code == 200:
                return (username, False)  # Not available
            else:
                # Try backup API if primary fails
                backup_response = requests.get(self.backup_api_url.format(username), timeout=5)
                if backup_response.status_code == 404:
                    return (username, True)  # Available
                elif backup_response.status_code == 200:
                    return (username, False)  # Not available
                else:
                    print(f"Error checking {username}: HTTP {response.status_code}")
                    return (username, None)  # Error
                    
        except requests.exceptions.RequestException as e:
            print(f"Network error checking {username}: {e}")
            return (username, None)  # Error
    
    def generate_4char_usernames(self, use_numbers=True, use_lowercase=True, use_uppercase=False) -> List[str]:
        """
        Generate all possible 4-character combinations.
        This will generate a LOT of combinations, so use carefully!
        """
        chars = ""
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        
        # Generate all 4-character combinations
        combinations = [''.join(combo) for combo in itertools.product(chars, repeat=4)]
        return combinations
    
    def check_specific_usernames(self, usernames: List[str]):
        """Check a specific list of usernames"""
        print("Checking specific usernames...")
        print("-" * 40)
        
        available_count = 0
        taken_count = 0
        session_available = []
        
        for username in usernames:
            result = self.check_username(username)
            username, is_available = result
            
            if is_available is True:
                print(f"{username} - available ✓")
                available_count += 1
                session_available.append(username)
                self.available_usernames.append(username)
            elif is_available is False:
                print(f"{username} - not available ✗")
                taken_count += 1
            else:
                print(f"{username} - error checking")
            
            # Rate limiting - be nice to the API
            time.sleep(0.5)
        
        print("-" * 40)
        print(f"Summary: {available_count} available, {taken_count} taken")
        
        if session_available:
            print(f"\nAvailable usernames from this check:")
            for username in session_available:
                print(f"  {username}")
            
            export_choice = input("\nExport available usernames to CSV? (y/n): ").strip().lower()
            if export_choice in ['y', 'yes']:
                self.export_to_csv()
    
    def check_random_4char_usernames(self, count: int = 50):
        """Check a random sample of 4-character usernames"""
        import random
        
        print(f"Checking {count} random 4-character usernames...")
        print("-" * 40)
        
        # Generate characters for random selection
        chars = string.ascii_lowercase + string.digits
        available_usernames = []
        taken_usernames = []
        
        for i in range(count):
            # Generate random 4-character username
            username = ''.join(random.choices(chars, k=4))
            
            result = self.check_username(username)
            username, is_available = result
            
            if is_available is True:
                print(f"{username} - available ✓")
                available_usernames.append(username)
                self.available_usernames.append(username)
            elif is_available is False:
                print(f"{username} - not available ✗")
                taken_usernames.append(username)
            else:
                print(f"{username} - error checking")
            
            # Rate limiting
            time.sleep(0.5)
        
        print("-" * 40)
        print(f"Summary: {len(available_usernames)} available, {len(taken_usernames)} taken")
        
        if available_usernames:
            print("\nAvailable usernames found:")
            for username in available_usernames:
                print(f"  {username}")
            
            export_choice = input("\nExport available usernames to CSV? (y/n): ").strip().lower()
            if export_choice in ['y', 'yes']:
                self.export_to_csv()
    
    def check_random_4char_usernames_letters_only(self, count: int = 50):
        """Check a random sample of 4-character usernames using only letters"""
        import random
        
        print(f"Checking {count} random 4-character usernames (letters only)...")
        print("-" * 40)
        
        # Generate characters for random selection - letters only
        chars = string.ascii_lowercase
        available_usernames = []
        taken_usernames = []
        
        for i in range(count):
            # Generate random 4-character username (letters only)
            username = ''.join(random.choices(chars, k=4))
            
            result = self.check_username(username)
            username, is_available = result
            
            if is_available is True:
                print(f"{username} - available ✓")
                available_usernames.append(username)
                self.available_usernames.append(username)
            elif is_available is False:
                print(f"{username} - not available ✗")
                taken_usernames.append(username)
            else:
                print(f"{username} - error checking")
            
            # Rate limiting
            time.sleep(0.5)
        
        print("-" * 40)
        print(f"Summary: {len(available_usernames)} available, {len(taken_usernames)} taken")
        
        if available_usernames:
            print("\nAvailable usernames found:")
            for username in available_usernames:
                print(f"  {username}")
            
            export_choice = input("\nExport available usernames to CSV? (y/n): ").strip().lower()
            if export_choice in ['y', 'yes']:
                self.export_to_csv()
    
    def check_pattern_usernames(self, pattern: str):
        """
        Check usernames following a pattern.
        Use 'x' as placeholder for characters to substitute.
        Example: 'axxx' will check a000, a001, a002, etc.
        """
        if 'x' not in pattern or len(pattern) != 4:
            print("Pattern must be exactly 4 characters with 'x' as placeholders")
            return
        
        print(f"Checking usernames with pattern: {pattern}")
        print("-" * 40)
        
        chars = string.ascii_lowercase + string.digits
        x_positions = [i for i, char in enumerate(pattern) if char == 'x']
        
        available_usernames = []
        count = 0
        max_check = 500  # Limit to avoid too many requests
        
        for combo in itertools.product(chars, repeat=len(x_positions)):
            if count >= max_check:
                print(f"Reached maximum check limit of {max_check}")
                break
                
            username = list(pattern)
            for i, char in enumerate(combo):
                username[x_positions[i]] = char
            username = ''.join(username)
            
            result = self.check_username(username)
            username, is_available = result
            
            if is_available is True:
                print(f"{username} - available ✓")
                available_usernames.append(username)
                self.available_usernames.append(username)
            elif is_available is False:
                print(f"{username} - not available ✗")
            else:
                print(f"{username} - error checking")
            
            count += 1
            time.sleep(0.5)
        
        print("-" * 40)
        if available_usernames:
            print(f"Available usernames found ({len(available_usernames)}):")
            for username in available_usernames:
                print(f"  {username}")
            
            export_choice = input("\nExport available usernames to CSV? (y/n): ").strip().lower()
            if export_choice in ['y', 'yes']:
                self.export_to_csv()

def main():
    checker = MinecraftUsernameChecker()
    
    print("=== Minecraft Username Availability Checker ===")
    print("💡 Tip: Press Ctrl+C at any time to save found usernames and exit\n")
    
    try:
        while True:
            print("\nOptions:")
            print("1. Check specific usernames")
            print("2. Check random 4-character usernames (letters + numbers)")
            print("3. Check random 4-character usernames (letters only)")
            print("4. Check usernames with pattern")
            print("5. Export all available usernames to CSV")
            print("6. View current session statistics")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                print("\nEnter usernames to check (comma-separated):")
                usernames_input = input("Usernames: ").strip()
                usernames = [u.strip() for u in usernames_input.split(',') if u.strip()]
                
                if usernames:
                    checker.check_specific_usernames(usernames)
                else:
                    print("No valid usernames provided.")
            
            elif choice == "2":
                try:
                    count = int(input("How many random usernames to check? (default 20): ") or "20")
                    checker.check_random_4char_usernames(count)
                except ValueError:
                    print("Invalid number, using default of 20")
                    checker.check_random_4char_usernames(20)
            
            elif choice == "3":
                try:
                    count = int(input("How many random usernames to check? (default 20): ") or "20")
                    checker.check_random_4char_usernames_letters_only(count)
                except ValueError:
                    print("Invalid number, using default of 20")
                    checker.check_random_4char_usernames_letters_only(20)
            
            elif choice == "4":
                pattern = input("Enter pattern (use 'x' for variable chars, e.g., 'axxx'): ").strip()
                if len(pattern) == 4:
                    checker.check_pattern_usernames(pattern)
                else:
                    print("Pattern must be exactly 4 characters.")
            
            elif choice == "5":
                checker.export_to_csv()
            
            elif choice == "6":
                print(f"\n=== Session Statistics ===")
                print(f"Total available usernames found: {len(checker.available_usernames)}")
                if checker.available_usernames:
                    print("Available usernames:")
                    for username in checker.available_usernames:
                        print(f"  {username}")
                else:
                    print("No available usernames found yet.")
            
            elif choice == "7":
                if checker.available_usernames:
                    save_choice = input(f"\nYou have {len(checker.available_usernames)} available usernames. Save to CSV before exit? (y/n): ").strip().lower()
                    if save_choice in ['y', 'yes']:
                        checker.export_to_csv()
                print("Goodbye! 👋")
                break
            
            else:
                print("Invalid choice. Please try again.")
                
    except KeyboardInterrupt:
        # This will be handled by the signal handler
        pass

if __name__ == "__main__":
    # Run interactive mode
    main()