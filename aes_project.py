import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
import json
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib
import threading
import time


class TextEncryption:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()
    
    def encrypt(self, message):
        try:
            iv = get_random_bytes(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            padded = pad(message.encode(), AES.block_size)
            encrypted = cipher.encrypt(padded)
            return base64.b64encode(iv + encrypted).decode()
        except:
            return None
    
    def decrypt(self, encrypted_message):
        try:
            data = base64.b64decode(encrypted_message)
            iv = data[:16]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(data[16:]), AES.block_size)
            return decrypted.decode()
        except:
            return None


class FileEncryption:
    CHUNK_SIZE = 64 * 1024
    
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()
    
    def encrypt_file(self, input_file, callback=None):
        try:
            if not os.path.exists(input_file):
                return None, "File not found"
            
            file_size = os.path.getsize(input_file)
            iv = get_random_bytes(16)
            output_file = input_file + '.encrypted'
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            bytes_done = 0
            with open(input_file, 'rb') as f_in:
                with open(output_file, 'wb') as f_out:
                    f_out.write(iv)
                    while True:
                        chunk = f_in.read(self.CHUNK_SIZE)
                        if not chunk:
                            break
                        if len(chunk) < self.CHUNK_SIZE:
                            chunk = pad(chunk, AES.block_size)
                        encrypted = cipher.encrypt(chunk)
                        f_out.write(encrypted)
                        bytes_done += len(chunk)
                        if callback:
                            callback(min((bytes_done / file_size) * 100, 100))
            
            return output_file, "Success"
        except Exception as e:
            return None, str(e)
    
    def decrypt_file(self, encrypted_file, callback=None):
        try:
            if not os.path.exists(encrypted_file):
                return None, "File not found"
            
            output_file = encrypted_file.replace('.encrypted', '_decrypted')
            file_size = os.path.getsize(encrypted_file)
            
            with open(encrypted_file, 'rb') as f_in:
                iv = f_in.read(16)
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
                
                bytes_done = 0
                with open(output_file, 'wb') as f_out:
                    while True:
                        chunk = f_in.read(self.CHUNK_SIZE)
                        if not chunk:
                            break
                        decrypted = cipher.decrypt(chunk)
                        f_out.write(decrypted)
                        bytes_done += len(chunk)
                        if callback:
                            callback(min((bytes_done / (file_size - 16)) * 100, 100))
            
            return output_file, "Success"
        except Exception as e:
            return None, str(e)


class PasswordManager:
    def __init__(self, master_password, storage_file='passwords.enc'):
        self.storage_file = storage_file
        self.encryptor = TextEncryption(master_password)
        self.passwords = self._load()
    
    def _load(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                decrypted = self.encryptor.decrypt(data['data'])
                if decrypted:
                    return json.loads(decrypted)
            except:
                pass
        return {}
    
    def _save(self):
        encrypted = self.encryptor.encrypt(json.dumps(self.passwords))
        with open(self.storage_file, 'w') as f:
            json.dump({'data': encrypted}, f)
    
    def add(self, service, username, password):
        self.passwords[service] = {'username': username, 'password': password}
        self._save()
    
    def get(self, service):
        return self.passwords.get(service)
    
    def delete(self, service):
        if service in self.passwords:
            del self.passwords[service]
            self._save()
            return True
        return False
    
    def list(self):
        return list(self.passwords.keys())


class AESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES Encryption Suite v3.0")
        self.root.geometry("1200x750")
        self.root.config(bg="#0d1117")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background="#0d1117")
        style.configure('TLabel', background="#0d1117", foreground="#fff")
        style.configure('TLabelframe', background="#0d1117", foreground="#fff")
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background="#0d1117", foreground="#0078d4")
        
        self.create_header()
        self.create_notebook()
        self.create_footer()
    
    def create_header(self):
        header = tk.Frame(self.root, bg="#161b22", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        canvas = tk.Canvas(header, bg="#161b22", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        canvas.create_text(50, 25, text="🔐 AES ENCRYPTION SUITE", font=("Arial", 18, "bold"), fill="#0078d4", anchor=tk.W)
        canvas.create_text(50, 50, text="Professional Encryption & Decryption Tool", font=("Arial", 10), fill="#8b949e", anchor=tk.W)
        canvas.create_line(50, 65, 1150, 65, fill="#30363d", width=2)
    
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.create_text_tab()
        self.create_file_tab()
        self.create_password_tab()
        self.create_info_tab()
    
    def create_text_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Text Encryption")
        
        title = ttk.Label(frame, text="Text Encryption & Decryption", style='Title.TLabel')
        title.pack(pady=15)
        
        pwd_frame = ttk.LabelFrame(frame, text="Password", padding=10)
        pwd_frame.pack(padx=20, pady=10, fill=tk.X)
        
        ttk.Label(pwd_frame, text="Password:").pack(side=tk.LEFT, padx=5)
        self.text_pwd = ttk.Entry(pwd_frame, show="•", width=50)
        self.text_pwd.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        content = ttk.Frame(frame)
        content.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        left = ttk.LabelFrame(content, text="Input", padding=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.text_input = scrolledtext.ScrolledText(left, height=18, width=45, font=('Arial', 10), bg="#161b22", fg="#fff")
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        mid = ttk.Frame(content)
        mid.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        tk.Button(mid, text="ENCRYPT", command=lambda: threading.Thread(target=self.encrypt_text, daemon=True).start(), bg="#238636", fg="white", font=('Arial', 10, 'bold'), width=12, height=3, cursor="hand2").pack(pady=10)
        tk.Button(mid, text="DECRYPT", command=lambda: threading.Thread(target=self.decrypt_text, daemon=True).start(), bg="#0078d4", fg="white", font=('Arial', 10, 'bold'), width=12, height=3, cursor="hand2").pack(pady=10)
        tk.Button(mid, text="CLEAR", command=lambda: self.text_input.delete('1.0', tk.END), bg="#444", fg="white", font=('Arial', 9), width=12, cursor="hand2").pack(pady=5)
        
        right = ttk.LabelFrame(content, text="Output", padding=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.text_output = scrolledtext.ScrolledText(right, height=18, width=45, font=('Arial', 10), bg="#161b22", fg="#fff")
        self.text_output.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(right, text="Copy", command=self.copy_text, bg="#444", fg="white", font=('Arial', 9), width=15, cursor="hand2").pack(pady=5, side=tk.BOTTOM)
    
    def encrypt_text(self):
        pwd = self.text_pwd.get()
        msg = self.text_input.get('1.0', tk.END).strip()
        
        if not pwd or not msg:
            messagebox.showerror("Error", "Enter password and text!")
            return
        
        enc = TextEncryption(pwd).encrypt(msg)
        if enc:
            self.text_output.delete('1.0', tk.END)
            self.text_output.insert('1.0', enc)
            messagebox.showinfo("Success", "Encrypted!")
        else:
            messagebox.showerror("Error", "Encryption failed!")
    
    def decrypt_text(self):
        pwd = self.text_pwd.get()
        msg = self.text_input.get('1.0', tk.END).strip()
        
        if not pwd or not msg:
            messagebox.showerror("Error", "Enter password and text!")
            return
        
        dec = TextEncryption(pwd).decrypt(msg)
        if dec:
            self.text_output.delete('1.0', tk.END)
            self.text_output.insert('1.0', dec)
            messagebox.showinfo("Success", "Decrypted!")
        else:
            messagebox.showerror("Error", "Decryption failed!")
    
    def copy_text(self):
        try:
            output = self.text_output.get('1.0', tk.END).strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            messagebox.showinfo("Success", "Copied!")
        except:
            messagebox.showerror("Error", "Nothing to copy!")
    
    def create_file_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="File Encryption")
        
        title = ttk.Label(frame, text="File Encryption & Decryption", style='Title.TLabel')
        title.pack(pady=15)
        
        pwd_frame = ttk.LabelFrame(frame, text="Password", padding=10)
        pwd_frame.pack(padx=20, pady=10, fill=tk.X)
        
        ttk.Label(pwd_frame, text="Password:").pack(side=tk.LEFT, padx=5)
        self.file_pwd = ttk.Entry(pwd_frame, show="•", width=50)
        self.file_pwd.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        file_frame = ttk.LabelFrame(frame, text="Select File", padding=10)
        file_frame.pack(padx=20, pady=10, fill=tk.X)
        
        ttk.Label(file_frame, text="File:").pack(side=tk.LEFT, padx=5)
        self.file_path = ttk.Entry(file_frame, width=60)
        self.file_path.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        tk.Button(file_frame, text="Browse", command=self.browse_file, bg="#444", fg="white", font=('Arial', 9), cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(padx=20, pady=20)
        
        self.enc_file_btn = tk.Button(btn_frame, text="ENCRYPT FILE", command=lambda: threading.Thread(target=self.encrypt_file, daemon=True).start(), bg="#238636", fg="white", font=('Arial', 11, 'bold'), width=20, height=2, cursor="hand2")
        self.enc_file_btn.pack(side=tk.LEFT, padx=10)
        
        self.dec_file_btn = tk.Button(btn_frame, text="DECRYPT FILE", command=lambda: threading.Thread(target=self.decrypt_file, daemon=True).start(), bg="#0078d4", fg="white", font=('Arial', 11, 'bold'), width=20, height=2, cursor="hand2")
        self.dec_file_btn.pack(side=tk.LEFT, padx=10)
        
        prog_frame = ttk.LabelFrame(frame, text="Progress", padding=10)
        prog_frame.pack(padx=20, pady=10, fill=tk.X)
        
        self.progress_canvas = tk.Canvas(prog_frame, bg="#161b22", height=30, highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X, expand=True)
        
        info_frame = ttk.LabelFrame(frame, text="Information", padding=10)
        info_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.file_info = scrolledtext.ScrolledText(info_frame, height=10, width=100, font=('Courier', 10), bg="#161b22", fg="#fff")
        self.file_info.pack(fill=tk.BOTH, expand=True)
    
    def browse_file(self):
        file = filedialog.askopenfilename()
        if file:
            self.file_path.delete(0, tk.END)
            self.file_path.insert(0, file)
    
    def draw_progress(self, value):
        self.progress_canvas.delete("all")
        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()
        
        self.progress_canvas.create_rectangle(0, 0, width, height, fill="#3d3d3d", outline="#666")
        filled = (value / 100) * width
        self.progress_canvas.create_rectangle(0, 0, filled, height, fill="#0078d4", outline="#0078d4")
        self.progress_canvas.create_text(width/2, height/2, text=f"{int(value)}%", fill="white", font=("Arial", 10, "bold"))
        self.root.update()
    
    def encrypt_file(self):
        pwd = self.file_pwd.get()
        path = self.file_path.get()
        
        if not pwd or not path:
            messagebox.showerror("Error", "Enter password and select file!")
            return
        
        try:
            self.enc_file_btn.config(state=tk.DISABLED, text="ENCRYPTING...")
            self.file_info.config(state=tk.NORMAL)
            self.file_info.delete('1.0', tk.END)
            self.file_info.insert('1.0', "Processing...\n")
            
            enc = FileEncryption(pwd)
            output, msg = enc.encrypt_file(path, self.draw_progress)
            
            if output:
                info = f"File: {path}\nEncrypted: {output}\nSize: {os.path.getsize(output)} bytes\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                self.file_info.delete('1.0', tk.END)
                self.file_info.insert('1.0', info)
                messagebox.showinfo("Success", "File encrypted!")
            else:
                messagebox.showerror("Error", msg)
        finally:
            self.enc_file_btn.config(state=tk.NORMAL, text="ENCRYPT FILE")
    
    def decrypt_file(self):
        pwd = self.file_pwd.get()
        path = self.file_path.get()
        
        if not pwd or not path:
            messagebox.showerror("Error", "Enter password and select file!")
            return
        
        try:
            self.dec_file_btn.config(state=tk.DISABLED, text="DECRYPTING...")
            self.file_info.config(state=tk.NORMAL)
            self.file_info.delete('1.0', tk.END)
            self.file_info.insert('1.0', "Processing...\n")
            
            dec = FileEncryption(pwd)
            output, msg = dec.decrypt_file(path, self.draw_progress)
            
            if output:
                info = f"File: {path}\nDecrypted: {output}\nSize: {os.path.getsize(output)} bytes\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                self.file_info.delete('1.0', tk.END)
                self.file_info.insert('1.0', info)
                messagebox.showinfo("Success", "File decrypted!")
            else:
                messagebox.showerror("Error", msg)
        finally:
            self.dec_file_btn.config(state=tk.NORMAL, text="DECRYPT FILE")
    
    def create_password_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Password Manager")
        
        title = ttk.Label(frame, text="Secure Password Manager", style='Title.TLabel')
        title.pack(pady=15)
        
        master_frame = ttk.LabelFrame(frame, text="Master Password", padding=10)
        master_frame.pack(padx=20, pady=10, fill=tk.X)
        
        ttk.Label(master_frame, text="Password:").pack(side=tk.LEFT, padx=5)
        self.master_pwd = ttk.Entry(master_frame, show="•", width=50)
        self.master_pwd.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        tk.Button(master_frame, text="Load", command=self.load_pm, bg="#238636", fg="white", font=('Arial', 9), cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        content = ttk.Frame(frame)
        content.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        left = ttk.LabelFrame(content, text="Add Password", padding=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(left, text="Service:").pack(anchor=tk.W, pady=5)
        self.service = ttk.Entry(left, width=40)
        self.service.pack(fill=tk.X, pady=5)
        
        ttk.Label(left, text="Username:").pack(anchor=tk.W, pady=5)
        self.username = ttk.Entry(left, width=40)
        self.username.pack(fill=tk.X, pady=5)
        
        ttk.Label(left, text="Password:").pack(anchor=tk.W, pady=5)
        self.password = ttk.Entry(left, show="•", width=40)
        self.password.pack(fill=tk.X, pady=5)
        
        btn = ttk.Frame(left)
        btn.pack(fill=tk.X, pady=15)
        
        tk.Button(btn, text="Add", command=self.add_pwd, bg="#238636", fg="white", font=('Arial', 9), width=12, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(btn, text="View", command=self.view_pwd, bg="#0078d4", fg="white", font=('Arial', 9), width=12, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(btn, text="Delete", command=self.del_pwd, bg="#da3633", fg="white", font=('Arial', 9), width=12, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        right = ttk.LabelFrame(content, text="Services", padding=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        scrollbar = ttk.Scrollbar(right)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.services_list = tk.Listbox(right, font=('Arial', 11), bg="#161b22", fg="#fff", yscrollcommand=scrollbar.set)
        self.services_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.services_list.yview)
        
        self.pm = None
    
    def load_pm(self):
        pwd = self.master_pwd.get()
        if not pwd:
            messagebox.showerror("Error", "Enter password!")
            return
        try:
            self.pm = PasswordManager(pwd)
            self.update_services()
            messagebox.showinfo("Success", "Loaded!")
        except:
            messagebox.showerror("Error", "Failed!")
    
    def update_services(self):
        if not self.pm:
            return
        self.services_list.delete(0, tk.END)
        for svc in self.pm.list():
            self.services_list.insert(tk.END, svc)
    
    def add_pwd(self):
        if not self.pm:
            messagebox.showerror("Error", "Load first!")
            return
        svc = self.service.get()
        user = self.username.get()
        pwd = self.password.get()
        
        if not svc or not user or not pwd:
            messagebox.showerror("Error", "Fill all!")
            return
        
        self.pm.add(svc, user, pwd)
        self.service.delete(0, tk.END)
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.update_services()
        messagebox.showinfo("Success", "Added!")
    
    def view_pwd(self):
        if not self.pm:
            messagebox.showerror("Error", "Load first!")
            return
        svc = self.service.get()
        if not svc:
            messagebox.showerror("Error", "Enter service!")
            return
        data = self.pm.get(svc)
        if data:
            messagebox.showinfo(svc, f"User: {data['username']}\nPass: {data['password']}")
        else:
            messagebox.showerror("Error", "Not found!")
    
    def del_pwd(self):
        if not self.pm:
            messagebox.showerror("Error", "Load first!")
            return
        svc = self.service.get()
        if not svc:
            messagebox.showerror("Error", "Enter service!")
            return
        if messagebox.askyesno("Confirm", f"Delete {svc}?"):
            if self.pm.delete(svc):
                self.service.delete(0, tk.END)
                self.update_services()
                messagebox.showinfo("Success", "Deleted!")
            else:
                messagebox.showerror("Error", "Not found!")
    
    def create_info_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Info")
        
        title = ttk.Label(frame, text="Information", style='Title.TLabel')
        title.pack(pady=15)
        
        info_frame = ttk.LabelFrame(frame, text="Features", padding=20)
        info_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        text = """AES ENCRYPTION SUITE v3.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FEATURES:
• Text Encryption/Decryption with AES-256
• File Encryption/Decryption with progress tracking
• Secure Password Manager with encryption
• Real-time progress visualization
• Professional GUI Interface

SECURITY:
• Military-grade AES-256 encryption
• SHA-256 key derivation
• Random IV generation
• Secure password storage
• No plaintext storage

HOW TO USE:
1. Text Tab: Enter password → Enter text → Click Encrypt/Decrypt
2. File Tab: Enter password → Browse file → Click Encrypt/Decrypt
3. Password Tab: Load manager → Add/View/Delete passwords

TECHNOLOGY:
• Python 3.7+
• Tkinter GUI
• PyCryptodome encryption
• Base64 encoding

Author: Encryption Team
Version: 3.0
License: Open Source
        """
        
        info_text = scrolledtext.ScrolledText(info_frame, height=20, width=100, font=('Courier', 10), bg="#161b22", fg="#fff")
        info_text.pack(fill=tk.BOTH, expand=True)
        info_text.insert('1.0', text)
        info_text.config(state=tk.DISABLED)
    
    def create_footer(self):
        footer = tk.Frame(self.root, bg="#0d1117", height=35)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        footer_label = tk.Label(footer, text="AES Encryption Suite v3.0 | Secure Your Data with Military-Grade Encryption", bg="#0d1117", fg="#8b949e", font=("Arial", 9))
        footer_label.pack(side=tk.LEFT, padx=20, pady=8)


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AESApp(root)
        root.mainloop()
    except ImportError:
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", "Install: pip install pycryptodome")
    except Exception as e:
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", str(e))