"""
CONSOLE-APP_CONSOLE-APP
A simple console-based typing speed tester
"""

import time
import os
from datetime import datetime

def show_menu():
    """Display the main menu"""
    print("\nTYPING SPEED TESTER")
    print("1. Start Test")
    print("2. View Results")
    print("3. Exit")

def start_test():
    """Start a typing test"""
    print("\nStarting typing test...")
    
    # Simple test text
    test_text = "The quick brown fox jumps over the lazy dog"
    print(f"\nType this text: {test_text}")
    
    # Start timer
    input("\nPress Enter to start typing...")
    start_time = time.time()
    
    # Get user input
    user_input = input("\nType here: ")
    end_time = time.time()
    
    # Calculate time taken
    time_taken = end_time - start_time
    
    # Calculate words per minute
    words = len(user_input.split())
    wpm = (words / time_taken) * 60
    
    # Calculate accuracy
    correct_words = sum(1 for a, b in zip(test_text.split(), user_input.split()) if a == b)
    accuracy = (correct_words / words) * 100 if words > 0 else 0
    
    # Save results
    results_file = os.path.join(os.path.dirname(__file__), 'CONSOLE-APP_results.txt')
    with open(results_file, 'a') as f:
        f.write(f"\nTest at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Words per minute: {wpm:.2f}\n")
        f.write(f"Accuracy: {accuracy:.2f}%\n")
        f.write("-" * 50)
    
    print("\nTest complete!")
    print(f"Words per minute: {wpm:.2f}")
    print(f"Accuracy: {accuracy:.2f}%")

def view_results():
    """View previous test results"""
    print("\nPrevious Results:")
    results_file = os.path.join(os.path.dirname(__file__), 'CONSOLE-APP_results.txt')
    try:
        with open(results_file, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("No results available yet.")

def main():
    """Main program loop"""
    print("Welcome to the Typing Speed Tester!")
    
    while True:
        show_menu()
        choice = input("\nChoose an option (1-3): ")
        
        if choice == '1':
            start_test()
        elif choice == '2':
            view_results()
        elif choice == '3':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
