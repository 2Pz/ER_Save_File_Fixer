"""
Elden Ring - Torrent State Fixer (GUI Version)
Fixes the loading screen freeze caused by Torrent being Active with 0 HP
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import struct
import os
import shutil
from pathlib import Path

class TorrentStateFixer:
    def __init__(self, root):
        self.root = root
        self.root.title("Elden Ring - Torrent State Fixer")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Default save location for Elden Ring
        self.default_save_path = Path(os.environ.get('APPDATA', '')) / "EldenRing"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title Section
        title_frame = ttk.Frame(self.root, padding="15")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame, 
            text="Elden Ring Torrent State Fixer",
            font=('Segoe UI', 18, 'bold')
        )
        title_label.pack()
        
        subtitle = ttk.Label(
            title_frame,
            text="Fix the stuck loading screen bug",
            font=('Segoe UI', 10)
        )
        subtitle.pack()
        
        # Info Panel
        info_frame = ttk.LabelFrame(self.root, text="How It Works", padding="15")
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        info_text = """Works with: Standard saves (.sl2) and Seamless Co-op saves (.co2)"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT, wraplength=650)
        info_label.pack()
        
        # File Selection
        file_frame = ttk.LabelFrame(self.root, text="Select Save File", padding="15")
        file_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.file_path_var = tk.StringVar()
        
        path_frame = ttk.Frame(file_frame)
        path_frame.pack(fill=tk.X)
        
        ttk.Label(path_frame, text="File:", font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        
        file_entry = ttk.Entry(path_frame, textvariable=self.file_path_var, width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        btn_frame = ttk.Frame(path_frame)
        btn_frame.pack(side=tk.LEFT)
        
        ttk.Button(btn_frame, text="Browse", command=self.browse_file, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Auto-Find", command=self.auto_detect, width=10).pack(side=tk.LEFT, padx=2)
        
        # Action Buttons
        action_frame = ttk.Frame(self.root, padding="15")
        action_frame.pack(fill=tk.X)
        
        self.fix_button = ttk.Button(
            action_frame,
            text="Fix Torrent State",
            command=self.fix_save,
            width=25
        )
        self.fix_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Restore Backup",
            command=self.restore_backup,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Clear Log",
            command=self.clear_log,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Log Output
        log_frame = ttk.LabelFrame(self.root, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            width=80,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status Bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        )
        status_bar.pack(fill=tk.X)
        
        # Initial log message
        self.log("Welcome! Select your save file and click 'Fix Torrent State'")
        self.log("WARNING: Make sure Elden Ring is CLOSED before fixing!\n")
    
    def log(self, message, color=None):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        if color:
            pass
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)
    
    def browse_file(self):
        """Browse for save file"""
        filename = filedialog.askopenfilename(
            title="Select Elden Ring Save File",
            initialdir=self.default_save_path,
            filetypes=[
                ("Elden Ring Saves", "*.sl2;*.co2"),
                ("Standard Save", "*.sl2"),
                ("Seamless Co-op Save", "*.co2"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.file_path_var.set(filename)
            self.log(f"Selected: {os.path.basename(filename)}")
            self.status_var.set(f"File selected: {os.path.basename(filename)}")
    
    def auto_detect(self):
        """Auto-detect save files"""
        if not self.default_save_path.exists():
            messagebox.showerror(
                "Not Found",
                f"Elden Ring save folder not found:\n{self.default_save_path}"
            )
            return
        
        # Find save files
        saves = list(self.default_save_path.rglob("ER*.sl2")) + \
                list(self.default_save_path.rglob("ER*.co2"))
        
        if not saves:
            messagebox.showwarning(
                "Not Found",
                "No Elden Ring save files found.\nPlease select manually."
            )
            return
        
        if len(saves) == 1:
            # Only one save found
            self.file_path_var.set(str(saves[0]))
            self.log(f"Auto-detected: {saves[0].name}")
            self.status_var.set("Save file auto-detected")
        else:
            # Multiple saves - show selection dialog
            self.show_save_selector(saves)
    
    def show_save_selector(self, saves):
        """Show dialog to select from multiple saves"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Save File")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(
            dialog,
            text=f"Found {len(saves)} save files. Select one:",
            font=('Segoe UI', 10, 'bold'),
            padding=10
        ).pack()
        
        listbox_frame = ttk.Frame(dialog, padding=10)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=('Consolas', 9)
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for save in saves:
            listbox.insert(tk.END, str(save))
        
        def select_save():
            selection = listbox.curselection()
            if selection:
                self.file_path_var.set(str(saves[selection[0]]))
                self.log(f"Selected: {saves[selection[0]].name}")
                dialog.destroy()
        
        ttk.Button(
            dialog,
            text="Select",
            command=select_save
        ).pack(pady=10)
        
        listbox.bind('<Double-Button-1>', lambda e: select_save())
    
    def fix_save(self):
        """Main fix function"""
        save_path = self.file_path_var.get()
        
        if not save_path or not os.path.exists(save_path):
            messagebox.showerror("Error", "Please select a valid save file first!")
            return
        
        # Confirm
        if not messagebox.askyesno(
            "Confirm",
            "This will modify your save file.\n"
            "A backup will be created automatically.\n\n"
            "Is Elden Ring closed?\n\n"
            "Continue?"
        ):
            return
        
        self.clear_log()
        self.log("="*70)
        self.log("STARTING FIX PROCESS")
        self.log("="*70)
        self.status_var.set("Processing...")
        self.fix_button.config(state=tk.DISABLED)
        
        try:
            # Create backup
            backup_path = save_path + ".backup"
            self.log(f"\nCreating backup: {os.path.basename(backup_path)}")
            shutil.copy2(save_path, backup_path)
            self.log("Backup created successfully")
            
            # Read file
            self.log(f"\nReading save file...")
            with open(save_path, 'rb') as f:
                data = bytearray(f.read())
            
            self.log(f"Loaded {len(data):,} bytes")
            
            # Search for pattern
            self.log("\nSearching for Torrent state issues...")
            self.log("   Looking for: State=13 (Active) with HP=0 at offset +17")
            
            fixes = []
            
            for i in range(len(data) - 21):
                try:
                    state = struct.unpack('<I', data[i:i+4])[0]
                    hp = struct.unpack('<I', data[i+17:i+21])[0]
                    
                    if state == 13 and hp == 0:
                        
                        self.log(f"\n   [!] Found at offset 0x{i:08X}")
                        
                        # Change state from 13 to 3
                        data[i] = 0x03
                        data[i+1] = 0x00
                        data[i+2] = 0x00
                        data[i+3] = 0x00
                        
                        fixes.append(i)
                        self.log(f"   [OK] Changed State from Active (13) -> Dead (3)")
                
                except (struct.error, IndexError):
                    pass
            
            if not fixes:
                self.log("\n[OK] No issues found!")
                self.log("   Your save file is already fine.")
                messagebox.showinfo(
                    "No Issues Found",
                    "Your save doesn't have the Torrent state bug.\n"
                    "A backup was still created for safety."
                )
                self.status_var.set("No issues detected")
                self.fix_button.config(state=tk.NORMAL)
                return
            
            # Write changes
            self.log(f"\nWriting {len(fixes)} fix(es) to file...")
            with open(save_path, 'wb') as f:
                bytes_written = f.write(data)
                f.flush()
                os.fsync(f.fileno())
            
            self.log(f"Wrote {bytes_written:,} bytes")
            
            # Verify
            self.log("\nVerifying changes...")
            with open(save_path, 'rb') as f:
                verify_data = bytearray(f.read())
            
            all_verified = True
            for offset in fixes:
                state = struct.unpack('<I', verify_data[offset:offset+4])[0]
                hp = struct.unpack('<I', verify_data[offset+17:offset+21])[0]
                
                if state == 3:
                    self.log(f"   [OK] Offset 0x{offset:08X}: State=Dead (3), HP={hp}")
                else:
                    self.log(f"   [FAIL] Offset 0x{offset:08X}: FAILED (State={state})")
                    all_verified = False
            
            # Final result
            self.log("\n" + "="*70)
            if all_verified:
                self.log("SUCCESS! All fixes verified!")
                self.log(f"Fixed {len(fixes)} instance(s)")
                self.log(f"Backup: {os.path.basename(backup_path)}")
                self.log("="*70)
                
                messagebox.showinfo(
                    "Success!",
                    f"Torrent state fixed successfully!\n\n"
                    f"Fixed {len(fixes)} instance(s)\n"
                    f"Backup created: {os.path.basename(backup_path)}\n\n"
                    f"You can now load your save in Elden Ring!"
                )
                self.status_var.set(f"Fixed {len(fixes)} instance(s)")
            else:
                self.log("WARNING: PARTIAL SUCCESS - Some verifications failed")
                self.log("="*70)
                messagebox.showwarning(
                    "Partial Success",
                    "Some changes may not have been saved properly.\n"
                    "Check the log for details."
                )
                self.status_var.set("Partial success")
        
        except Exception as e:
            self.log(f"\nERROR: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_var.set("Error occurred")
            import traceback
            traceback.print_exc()
        
        finally:
            self.fix_button.config(state=tk.NORMAL)
    
    def restore_backup(self):
        """Restore from backup"""
        save_path = self.file_path_var.get()
        
        if not save_path:
            messagebox.showerror("Error", "Please select a save file first!")
            return
        
        backup_path = save_path + ".backup"
        
        if not os.path.exists(backup_path):
            messagebox.showerror("Error", "No backup file found!")
            return
        
        if messagebox.askyesno(
            "Restore Backup",
            f"This will restore your save to the backup.\n\n"
            f"Current save will be overwritten.\n\n"
            f"Continue?"
        ):
            try:
                shutil.copy2(backup_path, save_path)
                self.log("\n[OK] Backup restored successfully!")
                messagebox.showinfo("Success", "Backup restored successfully!")
                self.status_var.set("Backup restored")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore backup:\n{str(e)}")

def main():
    root = tk.Tk()
    app = TorrentStateFixer(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
