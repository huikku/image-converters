import os
import sys
import tkinter as tk
from tkinter import messagebox, Label, Button
from PIL import Image, ImageTk
import threading

# First, we need to properly install tkinterdnd2
def ensure_tkinterdnd2():
    """Make sure tkinterdnd2 is installed"""
    try:
        import tkinterdnd2
        return True
    except ImportError:
        print("tkinterdnd2 not found. Attempting to install...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinterdnd2"])
            import tkinterdnd2
            print("tkinterdnd2 installed successfully!")
            return True
        except Exception as e:
            print(f"Failed to install tkinterdnd2: {e}")
            messagebox.showerror("Error", "Could not install the drag and drop library (tkinterdnd2).\n"
                                "Please install it manually with:\npip install tkinterdnd2")
            return False

# Main application
class WebPConverter:
    def __init__(self, root):
        self.root = root
        
        # Set window properties
        self.root.title("WebP Converter")
        self.root.geometry("400x300")
        self.root.minsize(300, 200)
        self.root.configure(bg="#f0f0f0")
        
        # Make window stay on top
        self.root.attributes("-topmost", True)
        
        # Create and configure the main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create drop zone with instructions
        self.drop_zone = Label(
            self.main_frame, 
            text="Drag and drop images here\nto convert to WebP (50% scale, 50% quality)",
            bg="#e0e0e0",
            relief="solid",
            borderwidth=2,
            font=("Arial", 12),
            height=10
        )
        self.drop_zone.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status indicator
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = Label(
            self.main_frame,
            textvariable=self.status_var,
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=10)
        
        # Setup the drop target
        self.setup_drop_target()
        
        # Counter for processed images
        self.processed_count = 0
    
    def setup_drop_target(self):
        """Configure drag and drop using tkinterdnd2"""
        # Register the drop zone as a drop target
        self.drop_zone.drop_target_register("DND_Files")
        # Bind the drop event
        self.drop_zone.dnd_bind('<<Drop>>', self.handle_drop)
    
    def handle_drop(self, event):
        """Handle file drop event"""
        # Get the dropped data
        data = event.data
        
        # Handle different data formats
        if data.startswith('{'):
            # Windows sometimes adds curly braces, strip them
            files = [path.strip('{}') for path in data.split('} {')]
        else:
            # Handle space-separated paths
            files = data.split()
        
        # Process the files
        threading.Thread(target=self.process_files, args=(files,), daemon=True).start()
    
    def process_files(self, files):
        """Process dropped files - convert to WebP"""
        self.status_var.set("Processing...")
        self.processed_count = 0
        
        for file_path in files:
            # Check if it's an image file
            if not self.is_image_file(file_path):
                continue
                
            try:
                # Open the image
                img = Image.open(file_path)
                
                # Get original dimensions
                width, height = img.size
                
                # Calculate new dimensions (50% scale)
                new_width = int(width * 0.5)
                new_height = int(height * 0.5)
                
                # Resize the image
                img = img.resize((new_width, new_height), Image.LANCZOS)
                
                # Create output path (same directory, change extension to .webp)
                output_path = os.path.splitext(file_path)[0] + ".webp"
                
                # Save as WebP with 50% quality
                img.save(output_path, "WEBP", quality=50)
                
                # Increment counter
                self.processed_count += 1
                self.status_var.set(f"Processed: {self.processed_count} image(s)")
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Update status when done
        if self.processed_count > 0:
            self.status_var.set(f"Converted {self.processed_count} image(s) to WebP")
        else:
            self.status_var.set("No valid images found to convert")
    
    def is_image_file(self, file_path):
        """Check if the file is a valid image based on extension"""
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
        _, ext = os.path.splitext(file_path.lower())
        return ext in valid_extensions

# Installation instructions for tkinterdnd2
def show_installation_instructions():
    """Show a message with tkinterdnd2 installation instructions"""
    msg = """To enable drag-and-drop functionality, you need to install the tkinterdnd2 package:

1. Open Command Prompt as administrator
2. Run: pip install tkinterdnd2

Alternative methods if the above fails:

Option A) Download the wheel file from https://pypi.org/project/tkinterdnd2/#files
   - Then install with: pip install [downloaded-file-path]

Option B) Use conda: conda install -c conda-forge tkinterdnd2

After installation, restart this application."""
    
    messagebox.showinfo("Installation Required", msg)

if __name__ == "__main__":
    # Try to ensure tkinterdnd2 is installed
    if ensure_tkinterdnd2():
        # Import after installation check
        from tkinterdnd2 import DND_FILES, TkinterDnD
        # Use the TkinterDnD.Tk as the root
        root = TkinterDnD.Tk()
        app = WebPConverter(root)
        root.mainloop()
    else:
        # Show regular Tk window with installation instructions
        root = tk.Tk()
        root.title("WebP Converter - Setup")
        root.geometry("400x300")
        
        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(
            frame,
            text="Drag and Drop functionality requires\nthe tkinterdnd2 package",
            font=("Arial", 12),
            pady=20
        )
        label.pack()
        
        button = tk.Button(
            frame,
            text="Show Installation Instructions",
            command=show_installation_instructions,
            padx=10,
            pady=5
        )
        button.pack(pady=10)
        
        root.mainloop()