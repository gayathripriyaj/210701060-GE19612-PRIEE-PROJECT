import pandas as pd
import tkinter as tk
from tkinter import scrolledtext

# Load the government schemes dataset
def load_dataset():
    try:
        dataset = pd.read_csv('schemes.csv')
        return dataset
    except FileNotFoundError:
        print("Error: Dataset file not found.")
        return None

# Recommend schemes based on user query
def recommend_schemes(user_query):
    dataset = load_dataset()
    if dataset is not None:
        matching_schemes = dataset[dataset['Scheme Name'].str.lower().str.contains(user_query.lower())]
        return matching_schemes['Scheme Name'].tolist()
    else:
        return []

# Process user query and display matching scheme names
def process_query():
    user_query = query_entry.get()
    scheme_names = recommend_schemes(user_query)
    output_text.delete('1.0', tk.END)
    if scheme_names:
        output_text.insert(tk.END, "Matching Scheme Names:\n\n")
        for scheme_name in scheme_names:
            output_text.insert(tk.END, f"- {scheme_name}\n")
        output_text.insert(tk.END, "\n\nEnter scheme name for more details:")
    else:
        output_text.insert(tk.END, "No matching scheme names found.\n\n")

# Process user input for scheme details
def process_scheme_details():
    scheme_name = scheme_entry.get()
    dataset = load_dataset()
    if dataset is not None:
        matching_scheme = dataset[dataset['Scheme Name'].str.lower() == scheme_name.lower()]
        output_text.delete('1.0', tk.END)
        if not matching_scheme.empty:
            scheme_details = matching_scheme.iloc[0]
            output_text.insert(tk.END, f"\nDetails for Scheme '{scheme_name}':\n\n")
            output_text.insert(tk.END, f"Description: {scheme_details['Description']}\n\n")
            output_text.insert(tk.END, f"Eligibility Criteria: {scheme_details['Eligibility Criteria']}\n\n")
            output_text.insert(tk.END, f"Benefits: {scheme_details['Benefits']}\n\n")
        else:
            output_text.insert(tk.END, f"Scheme '{scheme_name}' not found.\n\n")
    else:
        output_text.insert(tk.END, "Error: Dataset file not found.\n\n")

# Create GUI
root = tk.Tk()
root.title("Government Scheme Chatbot")

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size and position
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

intro_message = "Hi, I am the Government Scheme Chatbot. \nI can help you find information about government schemes. \nPlease enter your query below."

intro_label = tk.Label(root, text=intro_message, wraplength=window_width-20)
intro_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

query_label = tk.Label(root, text="Enter the scheme domain which you want to fetch:")
query_label.grid(row=1, column=0, padx=10, pady=10)

query_entry = tk.Entry(root, width=50)
query_entry.grid(row=1, column=1, padx=10, pady=10)

search_button = tk.Button(root, text="Search", command=process_query)
search_button.grid(row=1, column=2, padx=10, pady=10)

output_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

scheme_label = tk.Label(root, text="Enter scheme name for more details:")
scheme_label.grid(row=3, column=0, padx=10, pady=10)

scheme_entry = tk.Entry(root, width=50)
scheme_entry.grid(row=3, column=1, padx=10, pady=10)

details_button = tk.Button(root, text="Show Details", command=process_scheme_details)
details_button.grid(row=3, column=2, padx=10, pady=10)

root.mainloop()
