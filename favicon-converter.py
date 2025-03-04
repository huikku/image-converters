import os
import sys
import tkinter as tk
from tkinter import messagebox, Label, Button, IntVar, Checkbutton, Frame
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
class FaviconConverter:
    def __init__(self, root):
        self.root = root
        
        # Set window properties
        self.root.title("Favicon ICO Converter")
        self.root.geometry("480x400")
        self.root.minsize(400, 300)
        self.root.configure(bg="#f0f0f0")
        
        # Make window stay on top
        self.root.attributes("-topmost", True)
        
        # Create and configure the main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create drop zone with instructions
        self.drop_zone = Label(
            self.main_frame, 
            text="Drag and drop images here\nto convert to ICO favicon format",
            bg="#e0e0e0",
            relief="solid",
            borderwidth=2,
            font=("Arial", 12),
            height=8
        )
        self.drop_zone.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create options frame
        self.options_frame = Frame(self.main_frame, bg="#f0f0f0")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create size options
        self.size_label = Label(
            self.options_frame,
            text="Include sizes:",
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        self.size_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Size checkboxes
        self.size_vars = {}
        favicon_sizes = [16, 32, 48, 64, 128, 256]
        
        # Create a frame for the checkboxes
        self.sizes_frame = Frame(self.options_frame, bg="#f0f0f0")
        self.sizes_frame.grid(row=0, column=1, sticky="w")
        
        # Add checkboxes for each size
        for i, size in enumerate(favicon_sizes):
            self.size_vars[size] = IntVar(value=1)  # Default all checked
            cb = Checkbutton(
                self.sizes_frame, 
                text=f"{size}x{size}", 
                variable=self.size_vars[size],
                bg="#f0f0f0"
            )
            cb.grid(row=0, column=i, padx=5)
        
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
        """Process dropped files - convert to ICO"""
        self.status_var.set("Processing...")
        self.processed_count = 0
        
        # Get selected sizes
        selected_sizes = [size for size, var in self.size_vars.items() if var.get() == 1]
        
        if not selected_sizes:
            self.status_var.set("Error: No sizes selected")
            return
        
        for file_path in files:
            # Check if it's an image file
            if not self.is_image_file(file_path):
                continue
                
            try:
                # Open the image
                original_img = Image.open(file_path)
                
                # Prepare a list to hold different size versions
                img_list = []
                
                # Create each requested size
                for size in selected_sizes:
                    # Create a square version with transparency
                    img = self.create_square_thumbnail(original_img, size)
                    img_list.append(img)
                
                # Create output path (same directory, change extension to .ico)
                output_path = os.path.splitext(file_path)[0] + ".ico"
                
                # Save as ICO with all sizes
                img_list[0].save(
                    output_path, 
                    format="ICO", 
                    sizes=[(img.width, img.height) for img in img_list],
                    append_images=img_list[1:]
                )
                
                # Increment counter
                self.processed_count += 1
                self.status_var.set(f"Processed: {self.processed_count} image(s)")
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                self.status_var.set(f"Error: {str(e)}")
        
        # Update status when done
        if self.processed_count > 0:
            size_text = ", ".join([f"{s}x{s}" for s in selected_sizes])
            self.status_var.set(f"Converted {self.processed_count} image(s) to ICO with sizes: {size_text}")
        else:
            self.status_var.set("No valid images found to convert")
    
    def create_square_thumbnail(self, img, size):
        """Create a square thumbnail with alpha channel"""
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create a square image with transparent background
        square_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # Calculate dimensions to maintain aspect ratio
        img_ratio = img.width / img.height
        
        if img_ratio > 1:
            # Wider than tall
            new_width = size
            new_height = int(size / img_ratio)
            offset_x = 0
            offset_y = (size - new_height) // 2
        else:
            # Taller than wide or square
            new_width = int(size * img_ratio)
            new_height = size
            offset_x = (size - new_width) // 2
            offset_y = 0
        
        # Resize the original image
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Paste the resized image onto the square background
        square_img.paste(resized_img, (offset_x, offset_y), resized_img)
        
        return square_img
    
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
        app = FaviconConverter(root)
        root.mainloop()
    else:
        # Show regular Tk window with installation instructions
        root = tk.Tk()
        root.title("Favicon Converter - Setup")
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