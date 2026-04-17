import re
import sys

def read_file(filepath):
    """
    Reads the content of a text file.
    
    Args:
        filepath (str): The path to the file to be read.
        
    Returns:
        str: The content of the file, or None if an error occurs.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            if not content.strip():
                print(f"[-] Warning: The file '{filepath}' is empty.")
                return None
            return content
    except FileNotFoundError:
        print(f"[-] Error: Target file '{filepath}' not found.")
        print("    Please ensure the file exists in the correct directory.")
        return None
    except PermissionError:
        print(f"[-] Error: Permission denied when accessing '{filepath}'.")
        return None
    except Exception as e:
        print(f"[-] An unexpected error occurred while reading the file: {e}")
        return None

def extract_emails(text):
    """
    Extracts valid and unique email addresses from the given text.
    
    Args:
        text (str): The text content to parse.
        
    Returns:
        list: A sorted list of unique email addresses.
    """
    if not text:
        return []

    # A comprehensive regex pattern for validating email addresses
    # This covers most standard formats (e.g., user.name+tag@domain.co.uk)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Using re.findall to extract all matching patterns
    extracted_emails = re.findall(email_pattern, text)
    
    # Remove duplicates by converting the list to a set, then back to a list
    # Convert to lowercase to ensure uniqueness (email addresses are case-insensitive)
    unique_emails = list(set([email.lower() for email in extracted_emails]))
    
    # Sort the emails alphabetically
    unique_emails.sort()
    
    return unique_emails

def save_to_file(emails, output_filepath):
    """
    Saves a list of email addresses to a text file.
    
    Args:
        emails (list): The list of email addresses to save.
        output_filepath (str): The path to the output file.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(output_filepath, 'w', encoding='utf-8') as file:
            for email in emails:
                file.write(f"{email}\n")
        return True
    except Exception as e:
        print(f"[-] Error: Failed to save emails to '{output_filepath}'.")
        print(f"    Details: {e}")
        return False

def main():
    """
    Main execution function that orchestrates the email extraction process.
    """
    input_filename = 'input.txt'
    output_filename = 'emails.txt'

    print("=" * 50)
    print("      Email Extraction Automation Script")
    print("=" * 50)
    print(f"[*] Reading data from '{input_filename}'...")

    # Step 1: Read the file content
    content = read_file(input_filename)
    
    if content is None:
        print("[-] Process terminated due to file reading error.")
        sys.exit(1)

    # Step 2 & 3: Extract and deduplicate valid emails
    print("[*] Extracting and validating email addresses...")
    emails = extract_emails(content)

    # Check if any emails were found
    if not emails:
        print("[-] No valid email addresses found in the file.")
        sys.exit(0)

    # Step 4: Display the extracted emails and their count
    total_emails = len(emails)
    print(f"\n[+] Extraction Successful! Found {total_emails} unique email(s).\n")
    
    print("-" * 30)
    print("       Extracted Emails")
    print("-" * 30)
    for idx, email in enumerate(emails, 1):
        print(f"{idx:02d}. {email}")
    print("-" * 30, "\n")

    # Step 5: Save the extracted emails to the output file
    print(f"[*] Saving extracted emails to '{output_filename}'...")
    success = save_to_file(emails, output_filename)
    
    if success:
        print(f"[+] Success! {total_emails} email(s) have been saved to '{output_filename}'.")
    else:
        print("[-] Process completed with errors during file save.")
        
    print("=" * 50)

if __name__ == '__main__':
    main()
