import tkinter as tk

# Function to create a labeled entry field
def create_entry(parent, label_text, show_text=""):
    """Creates a label and entry widget in the given parent frame."""
    frame = tk.Frame(parent)
    
    label = tk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT)
    
    entry = tk.Entry(frame, show=show_text)
    entry.pack(side=tk.RIGHT)
    
    frame.pack()
    
    return entry  # Return entry widget for input access

# Function to clear input fields
def clear_entries(*entries):
    """Clears all given entry fields."""
    for entry in entries:
        entry.delete(0, tk.END)

# Function to switch between login & register frames
def switch_frames(current_frame, new_frame):
    """Hides the current frame and shows the new frame."""
    current_frame.pack_forget()
    new_frame.pack()
