#!/usr/bin/env python3
"""
Aplikasi Manajemen Properti
Aplikasi desktop untuk mengelola properti dengan autentikasi pengguna
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
import hashlib
import json
import os
import shutil
import webbrowser
import urllib.parse
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageTk
from airtable_sync import AirtableSync
# Removed enhanced logging to fix permission errors
# from enhanced_logging import property_logger
# from error_dialog import show_sync_error

class PropertyManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistem Manajemen Properti")
        
        # Set window to be maximized by default but allow resizing
        self.root.state('zoomed')  # Windows maximized
        
        # Set minimum window size to ensure all controls are visible
        self.root.minsize(1400, 900)
        
        # Fallback geometry in case maximized doesn't work
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Make window resizable
        self.root.resizable(True, True)
        
        # Pengguna saat ini
        self.current_user = None
        
        # Variabel untuk gambar yang dipilih
        self.selected_image_path = None
        self.image_preview_label = None
        
        # Inisialisasi database
        self.init_database()
        
        # Inisialisasi sinkronisasi Airtable
        self.airtable_sync = AirtableSync()
        
        # Buat direktori gambar jika belum ada
        if getattr(sys, 'frozen', False):
            # Berjalan sebagai executable - coba direktori app dulu, fallback ke AppData
            app_dir = os.path.dirname(sys.executable)
            images_path = os.path.join(app_dir, 'property_images')
            
            # Test apakah bisa menulis ke direktori app
            try:
                test_dir = os.path.join(app_dir, 'test_images')
                os.makedirs(test_dir, exist_ok=True)
                os.rmdir(test_dir)
                # Jika bisa menulis, gunakan direktori app
                self.images_dir = Path(images_path)
            except (PermissionError, OSError):
                # Jika tidak bisa menulis ke direktori app, gunakan AppData
                app_data = os.path.expanduser('~')
                app_data_dir = os.path.join(app_data, 'PropertyManagement')
                self.images_dir = Path(os.path.join(app_data_dir, 'property_images'))
        else:
            # Berjalan sebagai script
            app_dir = os.path.dirname(os.path.abspath(__file__))
            self.images_dir = Path(os.path.join(app_dir, 'property_images'))
        
        self.images_dir.mkdir(exist_ok=True)
        
        # Buat antarmuka login
        self.create_login_interface()
    
    def init_database(self):
        """Inisialisasi database SQLite dengan tabel yang diperlukan"""
        # Dapatkan direktori yang tepat untuk database
        if getattr(sys, 'frozen', False):
            # Berjalan sebagai executable - coba direktori app dulu, fallback ke AppData
            app_dir = os.path.dirname(sys.executable)
            db_path = os.path.join(app_dir, 'property_management.db')
            
            # Test apakah bisa menulis ke direktori app
            try:
                test_file = os.path.join(app_dir, 'test_write.tmp')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                # Jika bisa menulis, gunakan direktori app
            except (PermissionError, OSError):
                # Jika tidak bisa menulis ke direktori app, gunakan AppData
                app_data = os.path.expanduser('~')
                app_data_dir = os.path.join(app_data, 'PropertyManagement')
                os.makedirs(app_data_dir, exist_ok=True)
                db_path = os.path.join(app_data_dir, 'property_management.db')
        else:
            # Berjalan sebagai script
            app_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(app_dir, 'property_management.db')
        
        # Buat koneksi database
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            messagebox.showerror("Error Database", 
                               f"Tidak dapat membuat file database.\nPath: {db_path}\nError: {str(e)}\n\nHarap jalankan sebagai administrator atau hubungi dukungan.")
            raise e
        
        # Cek apakah tabel lama ada dan perlu migrasi
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='properties'")
        table_exists = self.cursor.fetchone()
        
        if table_exists:
            # Cek apakah kolom lama masih ada (untuk migrasi)
            self.cursor.execute("PRAGMA table_info(properties)")
            columns = [column[1] for column in self.cursor.fetchall()]
            
            if 'address' in columns and 'city' in columns and 'state' in columns and 'zip_code' in columns:
                # Lakukan migrasi dari struktur lama ke baru
                self.migrate_database()
        
        # Buat tabel users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Periksa apakah tabel properties sudah ada dengan struktur baru
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='properties'")
        table_exists = self.cursor.fetchone()
        
        if table_exists:
            # Periksa apakah kolom lokasi ada (struktur baru)
            self.cursor.execute("PRAGMA table_info(properties)")
            columns = [row[1] for row in self.cursor.fetchall()]
            
            if 'lokasi' not in columns:
                # Tabel ada tapi dengan struktur lama, lakukan migrasi
                self.migrate_database()
            else:
                print("Database sudah menggunakan struktur Indonesian")
        else:
            # Buat tabel properties dengan struktur baru (Indonesian)
            self.cursor.execute('''
                CREATE TABLE properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_properti TEXT NOT NULL,
                    lokasi TEXT NOT NULL,
                    tipe_properti TEXT NOT NULL,
                    kamar_tidur INTEGER,
                    kamar_mandi INTEGER,
                    luas_bangunan INTEGER,
                    harga REAL,
                    status TEXT DEFAULT 'Tersedia',
                    deskripsi TEXT,
                    gambar_path TEXT,
                    link_map TEXT,
                    ditambahkan_oleh TEXT,
                    airtable_record_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("Tabel properties baru dibuat dengan struktur Indonesian")
        
        # Tambahkan kolom nama_properti jika belum ada (untuk upgrade database existing)
        try:
            self.cursor.execute("PRAGMA table_info(properties)")
            columns = [column[1] for column in self.cursor.fetchall()]
            if 'nama_properti' not in columns:
                self.cursor.execute('ALTER TABLE properties ADD COLUMN nama_properti TEXT DEFAULT ""')
                self.conn.commit()
                print("Kolom nama_properti berhasil ditambahkan")
        except Exception as e:
            print(f"Error menambah kolom nama_properti: {e}")
        
        # Buat tabel untuk jenis properti custom
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS property_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_tipe TEXT UNIQUE NOT NULL,
                dibuat_oleh TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tambahkan jenis properti default jika belum ada
        default_types = ['Rumah', 'Apartemen', 'Ruko', 'Tanah', 'Villa', 'Kondominium']
        for prop_type in default_types:
            self.cursor.execute(
                'INSERT OR IGNORE INTO property_types (nama_tipe, dibuat_oleh) VALUES (?, ?)',
                (prop_type, 'system')
            )
        
        self.conn.commit()
        
        # Buat admin default jika belum ada pengguna
        self.cursor.execute('SELECT COUNT(*) FROM users')
        if self.cursor.fetchone()[0] == 0:
            self.create_default_admin()
        
        # Sinkronisasi data dari Airtable saat startup
        self.sync_from_airtable()

    def migrate_database(self):
        """Migrasi database dari struktur lama ke struktur baru"""
        try:
            # Periksa struktur tabel yang ada
            self.cursor.execute("PRAGMA table_info(properties)")
            columns_info = self.cursor.fetchall()
            columns = [row[1] for row in columns_info]
            
            print(f"Kolom yang ditemukan: {columns}")
            
            # Buat tabel baru sementara
            self.cursor.execute('''
                CREATE TABLE properties_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_properti TEXT NOT NULL,
                    lokasi TEXT NOT NULL,
                    tipe_properti TEXT NOT NULL,
                    kamar_tidur INTEGER,
                    kamar_mandi INTEGER,
                    luas_bangunan INTEGER,
                    harga REAL,
                    status TEXT DEFAULT 'Tersedia',
                    deskripsi TEXT,
                    gambar_path TEXT,
                    link_map TEXT,
                    ditambahkan_oleh TEXT,
                    airtable_record_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Cek apakah ada data dalam tabel lama
            self.cursor.execute('SELECT COUNT(*) FROM properties')
            record_count = self.cursor.fetchone()[0]
            
            if record_count > 0:
                # Migrasi data berdasarkan struktur yang tersedia
                if 'address' in columns and 'city' in columns:
                    # Struktur lama lengkap
                    print("Migrasi dari struktur English lama")
                    self.cursor.execute('''
                        INSERT INTO properties_new (
                            id, nama_properti, lokasi, tipe_properti, kamar_tidur, kamar_mandi, 
                            luas_bangunan, harga, status, deskripsi, gambar_path, 
                            link_map, ditambahkan_oleh, airtable_record_id, created_at, updated_at
                        )
                        SELECT 
                            id,
                            COALESCE(name, 'Properti ' || id) as nama_properti,
                            COALESCE(address, '') || CASE WHEN address IS NOT NULL AND city IS NOT NULL THEN ', ' ELSE '' END || 
                            COALESCE(city, '') || CASE WHEN city IS NOT NULL AND state IS NOT NULL THEN ', ' ELSE '' END || 
                            COALESCE(state, '') || CASE WHEN state IS NOT NULL AND zip_code IS NOT NULL THEN ' ' ELSE '' END || 
                            COALESCE(zip_code, '') as lokasi,
                            COALESCE(property_type, 'Rumah') as tipe_properti,
                            COALESCE(bedrooms, 0) as kamar_tidur,
                            COALESCE(bathrooms, 0) as kamar_mandi,
                            COALESCE(sqft, 0) as luas_bangunan,
                            COALESCE(harga, price, 0) as harga,
                            CASE 
                                WHEN status = 'available' THEN 'Tersedia'
                                WHEN status = 'sold' THEN 'Terjual'
                                ELSE 'Tersedia'
                            END as status,
                            COALESCE(description, '') as deskripsi,
                            image_path as gambar_path,
                            map_link as link_map,
                            COALESCE(added_by, 'Admin') as ditambahkan_oleh,
                            airtable_record_id,
                            COALESCE(created_at, datetime('now')) as created_at,
                            COALESCE(updated_at, datetime('now')) as updated_at
                        FROM properties
                    ''')
                else:
                    # Struktur tidak dikenali atau campuran, copy yang bisa di-copy
                    print("Migrasi dari struktur yang tidak dikenali, menggunakan default values")
                    self.cursor.execute('''
                        INSERT INTO properties_new (
                            id, nama_properti, lokasi, tipe_properti, kamar_tidur, kamar_mandi, 
                            luas_bangunan, harga, status, deskripsi, ditambahkan_oleh
                        )
                        SELECT 
                            id,
                            'Properti ' || id as nama_properti,
                            'Lokasi tidak diketahui' as lokasi,
                            'Rumah' as tipe_properti,
                            0 as kamar_tidur,
                            0 as kamar_mandi,
                            0 as luas_bangunan,
                            0 as harga,
                            'Tersedia' as status,
                            '' as deskripsi,
                            'Migration' as ditambahkan_oleh
                        FROM properties
                    ''')
            
            # Hapus tabel lama dan rename tabel baru
            self.cursor.execute('DROP TABLE properties')
            self.cursor.execute('ALTER TABLE properties_new RENAME TO properties')
            
            self.conn.commit()
            print("Migrasi database berhasil")
            
        except Exception as e:
            print(f"Error dalam migrasi database: {e}")
            # Jika migrasi gagal, buat tabel baru kosong
            try:
                self.cursor.execute('DROP TABLE IF EXISTS properties_new')
                self.cursor.execute('DROP TABLE IF EXISTS properties')
                self.cursor.execute('''
                    CREATE TABLE properties (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama_properti TEXT NOT NULL,
                        lokasi TEXT NOT NULL,
                        tipe_properti TEXT NOT NULL,
                        kamar_tidur INTEGER,
                        kamar_mandi INTEGER,
                        luas_bangunan INTEGER,
                        harga REAL,
                        status TEXT DEFAULT 'Tersedia',
                        deskripsi TEXT,
                        gambar_path TEXT,
                        link_map TEXT,
                        ditambahkan_oleh TEXT,
                        airtable_record_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                self.conn.commit()
                print("Tabel baru dibuat karena migrasi gagal")
            except Exception as e2:
                print(f"Error membuat tabel baru: {e2}")
                self.conn.rollback()

    def sync_from_airtable(self):
        """Sinkronisasi data dari Airtable ke database lokal"""
        try:
            # Ambil semua record dari Airtable
            airtable_records = self.airtable_sync.get_all_records()
            
            if not airtable_records:
                return
            
            for record in airtable_records:
                record_id = record['id']
                fields = record.get('fields', {})
                
                # Cek apakah record sudah ada di database lokal
                self.cursor.execute(
                    'SELECT id FROM properties WHERE airtable_record_id = ?',
                    (record_id,)
                )
                existing = self.cursor.fetchone()
                
                if not existing:
                    # Tambah record baru ke database lokal
                    nama_properti = fields.get('Name', '') or f"Properti {record_id}"
                    lokasi = fields.get('Location', '') or "Lokasi tidak tersedia"  # User confirmed column is "Location"
                    tipe_properti = fields.get('PropertyType', '') or fields.get('Tipe_Properti', 'Rumah')
                    kamar_tidur = fields.get('Bedrooms', 0) or fields.get('Kamar_Tidur', 0)
                    kamar_mandi = fields.get('Bathrooms', 0) or fields.get('Kamar_Mandi', 0)
                    luas_bangunan = fields.get('Area', 0) or fields.get('Luas_Bangunan', 0) or fields.get('SQFT', 0)
                    harga = fields.get('Price', 0) or fields.get('Harga', 0)
                    status = fields.get('Status', 'Tersedia')
                    if status.lower() in ['available', 'tersedia']:
                        status = 'Tersedia'
                    elif status.lower() in ['sold', 'terjual']:
                        status = 'Terjual'
                    deskripsi = fields.get('Description', '') or fields.get('Deskripsi', '')
                    link_map = fields.get('MapLink', '') or fields.get('Link_Map', '')
                    
                    self.cursor.execute('''
                        INSERT INTO properties (
                            nama_properti, lokasi, tipe_properti, kamar_tidur, kamar_mandi, 
                            luas_bangunan, harga, status, deskripsi, link_map,
                            ditambahkan_oleh, airtable_record_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        nama_properti, lokasi, tipe_properti, kamar_tidur, kamar_mandi,
                        luas_bangunan, harga, status, deskripsi, link_map,
                        'Airtable Sync', record_id
                    ))
            
            self.conn.commit()
            print(f"Berhasil sinkronisasi {len(airtable_records)} record dari Airtable")
            
        except Exception as e:
            print(f"Error sinkronisasi dari Airtable: {e}")

    def format_rupiah(self, amount):
        """Format angka menjadi format Rupiah"""
        if amount is None or amount == '':
            return "Rp 0"
        try:
            amount = float(amount)
            return f"Rp {amount:,.0f}".replace(',', '.')
        except:
            return "Rp 0"

    def get_property_types(self):
        """Ambil semua jenis properti dari database"""
        self.cursor.execute('SELECT nama_tipe FROM property_types ORDER BY nama_tipe')
        return [row[0] for row in self.cursor.fetchall()]

    def add_property_type(self, nama_tipe):
        """Tambah jenis properti baru"""
        try:
            self.cursor.execute(
                'INSERT INTO property_types (nama_tipe, dibuat_oleh) VALUES (?, ?)',
                (nama_tipe, self.current_user['username'])
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Jenis properti sudah ada
    
    def add_new_property_type(self):
        """Dialog untuk menambah tipe properti baru"""
        new_type = simpledialog.askstring(
            "Tambah Tipe Properti Baru",
            "Masukkan nama tipe properti baru:",
            parent=self.root
        )
        
        if new_type:
            new_type = new_type.strip()
            if new_type:
                if self.add_property_type(new_type):
                    messagebox.showinfo("Berhasil", f"Tipe properti '{new_type}' berhasil ditambahkan!")
                    # Update combo box values
                    if 'tipe_properti' in self.property_fields:
                        combo = self.property_fields['tipe_properti']
                        combo['values'] = self.get_property_types()
                        combo.set(new_type)  # Set the new type as selected
                else:
                    messagebox.showerror("Error", f"Tipe properti '{new_type}' sudah ada!")

    def create_default_admin(self):
        """Buat pengguna admin default"""
        admin_password = "admin123"
        password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        
        self.cursor.execute(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            ('admin', password_hash, 'admin')
        )
        self.conn.commit()
        
        messagebox.showinfo("Admin Default Dibuat", 
                          "Pengguna admin default telah dibuat!\nUsername: admin\nPassword: admin123\n\nHarap ubah password setelah login pertama.")
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        password_hash = self.hash_password(password)
        self.cursor.execute(
            'SELECT id, username, role FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        return self.cursor.fetchone()
    
    def create_login_interface(self):
        """Buat antarmuka login"""
        # Bersihkan jendela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Buat frame utama
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both')
        
        # Frame login
        login_frame = tk.Frame(main_frame, bg='white', padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Judul
        title_label = tk.Label(login_frame, text="Sistem Manajemen Properti", 
                              font=("Arial", 24, "bold"), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        # Username
        tk.Label(login_frame, text="Nama Pengguna:", font=("Arial", 12), bg='white').pack(anchor='w')
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=25)
        self.username_entry.pack(pady=(5, 15))
        
        # Password
        tk.Label(login_frame, text="Kata Sandi:", font=("Arial", 12), bg='white').pack(anchor='w')
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), width=25, show='*')
        self.password_entry.pack(pady=(5, 20))
        
        # Login button
        login_btn = tk.Button(login_frame, text="Masuk", font=("Arial", 12, "bold"),
                             bg='#3498db', fg='white', padx=20, pady=10,
                             command=self.login)
        login_btn.pack(pady=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def login(self):
        """Tangani login pengguna"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Harap masukkan nama pengguna dan kata sandi")
            return
        
        user = self.authenticate_user(username, password)
        if user:
            self.current_user = {'id': user[0], 'username': user[1], 'role': user[2]}
            self.create_main_interface()
        else:
            messagebox.showerror("Error", "Nama pengguna atau kata sandi salah")
            self.password_entry.delete(0, tk.END)
    
    def create_main_interface(self):
        """Buat antarmuka utama aplikasi"""
        # Bersihkan jendela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Buat menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Test Koneksi Airtable", command=self.test_airtable_connection)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Tutup", command=self.root.quit)
        
        # Menu User (untuk admin)
        if self.current_user['role'] == 'admin':
            user_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Pengguna", menu=user_menu)
            user_menu.add_command(label="Buat Pengguna", command=self.create_user_dialog)
            user_menu.add_command(label="Ubah Password", command=self.change_password_dialog)
        
        # Buat frame utama
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Label selamat datang
        welcome_label = tk.Label(main_frame, 
                               text=f"Selamat datang, {self.current_user['username']}! ({self.current_user['role']})",
                               font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#2c3e50')
        welcome_label.pack(pady=(0, 20))
        
        # Buat notebook untuk tab
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Tab properti
        self.create_properties_tab()
        
        # Tab tambah properti
        self.create_add_property_tab()
        
        # Muat properti
        self.load_properties()
    
    def create_properties_tab(self):
        """Buat tab manajemen properti"""
        properties_frame = ttk.Frame(self.notebook)
        self.notebook.add(properties_frame, text="Daftar Properti")
        
        # Frame pencarian
        search_frame = tk.Frame(properties_frame, bg='white')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Cari:", font=("Arial", 12), bg='white').pack(side='left', padx=(10, 5))
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
        self.search_entry.pack(side='left', padx=5)
        
        search_btn = tk.Button(search_frame, text="Cari", font=("Arial", 10),
                              bg='#3498db', fg='white', command=self.search_properties)
        search_btn.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(search_frame, text="Refresh", font=("Arial", 10),
                               bg='#27ae60', fg='white', command=self.load_properties)
        refresh_btn.pack(side='left', padx=5)
        
        # Frame tabel properti
        tree_frame = tk.Frame(properties_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame)
        v_scrollbar.pack(side='right', fill='y')
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Treeview dengan kolom baru (Indonesian)
        columns = ('ID', 'Nama Properti', 'Lokasi', 'Tipe', 'Kamar Tidur', 'Kamar Mandi', 'Luas', 'Harga', 'Status')
        self.properties_tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                          yscrollcommand=v_scrollbar.set,
                                          xscrollcommand=h_scrollbar.set)
        
        # Konfigurasi scrollbars
        v_scrollbar.config(command=self.properties_tree.yview)
        h_scrollbar.config(command=self.properties_tree.xview)
        
        # Konfigurasi kolom
        column_widths = {'ID': 50, 'Nama Properti': 150, 'Lokasi': 180, 'Tipe': 100, 'Kamar Tidur': 80, 'Kamar Mandi': 80, 'Luas': 80, 'Harga': 120, 'Status': 80}
        for col in columns:
            self.properties_tree.heading(col, text=col)
            self.properties_tree.column(col, width=column_widths.get(col, 120))
        
        self.properties_tree.pack(fill='both', expand=True)
        
        # Bind scroll wheel events
        self.properties_tree.bind("<MouseWheel>", self._on_tree_mousewheel)
        
        # Frame tombol
        buttons_frame = tk.Frame(properties_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        edit_btn = tk.Button(buttons_frame, text="Edit Properti", font=("Arial", 10),
                           bg='#f39c12', fg='white', command=self.edit_property)
        edit_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(buttons_frame, text="Hapus Properti", font=("Arial", 10),
                              bg='#e74c3c', fg='white', command=self.delete_property)
        delete_btn.pack(side='left', padx=5)
        
        status_btn = tk.Button(buttons_frame, text="Update Status", font=("Arial", 10),
                              bg='#9b59b6', fg='white', command=self.update_property_status)
        status_btn.pack(side='left', padx=5)
    
    def _on_tree_mousewheel(self, event):
        """Handle mouse wheel scrolling on treeview"""
        self.properties_tree.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_add_property_tab(self):
        """Buat tab tambah properti"""
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Tambah Properti")
        
        # Buat frame yang bisa di-scroll
        canvas = tk.Canvas(add_frame, bg='white')
        scrollbar = ttk.Scrollbar(add_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel to canvas
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Form fields
        fields_frame = tk.Frame(scrollable_frame, bg='white', padx=40, pady=20)
        fields_frame.pack(fill='both', expand=True)
        
        # Judul
        title_label = tk.Label(fields_frame, text="Tambah Properti Baru", 
                              font=("Arial", 18, "bold"), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Buat field form
        self.property_fields = {}
        self.selected_image_path = None
        
        fields = [
            ('nama_properti', 'Nama Properti', 'text'),
            ('lokasi', 'Lokasi (Alamat Lengkap)', 'text'),
            ('tipe_properti', 'Tipe Properti', 'combo_custom'),
            ('kamar_tidur', 'Kamar Tidur', 'number'),
            ('kamar_mandi', 'Kamar Mandi', 'number'),
            ('luas_bangunan', 'Luas Bangunan (m²)', 'number'),
            ('harga', 'Harga (Rp)', 'number'),
            ('deskripsi', 'Deskripsi', 'textarea')
        ]
        
        for field_name, label, field_type in fields:
            field_frame = tk.Frame(fields_frame, bg='white')
            field_frame.pack(fill='x', pady=10)
            
            tk.Label(field_frame, text=f"{label}:", font=("Arial", 12), bg='white').pack(anchor='w')
            
            if field_type == 'text' or field_type == 'number':
                entry = tk.Entry(field_frame, font=("Arial", 12), width=40)
                entry.pack(anchor='w', pady=(5, 0))
                self.property_fields[field_name] = entry
            elif field_type == 'combo_custom':
                # Frame untuk combobox dan tombol tambah
                combo_frame = tk.Frame(field_frame, bg='white')
                combo_frame.pack(anchor='w', pady=(5, 0), fill='x')
                
                combo = ttk.Combobox(combo_frame, font=("Arial", 12), width=30)
                combo['values'] = self.get_property_types()
                combo.pack(side='left', padx=(0, 10))
                self.property_fields[field_name] = combo
                
                # Tombol untuk menambah tipe properti baru
                add_type_btn = tk.Button(combo_frame, text="+ Tambah Tipe Baru", 
                                       font=("Arial", 9), bg='#2ecc71', fg='white',
                                       command=self.add_new_property_type)
                add_type_btn.pack(side='left')
            elif field_type == 'textarea':
                text_widget = tk.Text(field_frame, font=("Arial", 12), width=40, height=4)
                text_widget.pack(anchor='w', pady=(5, 0))
                self.property_fields[field_name] = text_widget
        
        # Bagian pemilihan gambar
        image_frame = tk.Frame(fields_frame, bg='white')
        image_frame.pack(fill='x', pady=10)
        
        tk.Label(image_frame, text="Gambar Properti:", font=("Arial", 12), bg='white').pack(anchor='w')
        
        image_button_frame = tk.Frame(image_frame, bg='white')
        image_button_frame.pack(anchor='w', pady=(5, 0))
        
        self.select_image_btn = tk.Button(image_button_frame, text="Pilih Gambar", 
                                         font=("Arial", 10), bg='#3498db', fg='white',
                                         command=self.select_image)
        self.select_image_btn.pack(side='left', padx=(0, 10))
        
        self.remove_image_btn = tk.Button(image_button_frame, text="Hapus Gambar", 
                                         font=("Arial", 10), bg='#e74c3c', fg='white',
                                         command=self.remove_image, state='disabled')
        self.remove_image_btn.pack(side='left')
        
        # Preview gambar
        self.image_preview_frame = tk.Frame(image_frame, bg='white')
        self.image_preview_frame.pack(anchor='w', pady=(10, 0))
        
        self.image_preview_label = tk.Label(self.image_preview_frame, text="Belum ada gambar dipilih", 
                                           bg='white', fg='#7f8c8d', font=("Arial", 10))
        self.image_preview_label.pack()
        
        # Bagian MapLink
        map_frame = tk.Frame(fields_frame, bg='white')
        map_frame.pack(fill='x', pady=10)
        
        tk.Label(map_frame, text="Link Google Maps:", font=("Arial", 12), bg='white').pack(anchor='w')
        
        map_entry_frame = tk.Frame(map_frame, bg='white')
        map_entry_frame.pack(anchor='w', pady=(5, 0), fill='x')
        
        self.map_link_entry = tk.Entry(map_entry_frame, font=("Arial", 11), width=50)
        self.map_link_entry.pack(side='left', fill='x', expand=True)
        
        map_button_frame = tk.Frame(map_frame, bg='white')
        map_button_frame.pack(anchor='w', pady=(5, 0))
        
        self.open_maps_btn = tk.Button(map_button_frame, text="Buka Google Maps", 
                                      font=("Arial", 10), bg='#4285f4', fg='white',
                                      command=self.open_google_maps)
        self.open_maps_btn.pack(side='left', padx=(0, 10))
        
        self.validate_link_btn = tk.Button(map_button_frame, text="Validasi Link", 
                                          font=("Arial", 10), bg='#34a853', fg='white',
                                          command=self.validate_map_link)
        self.validate_link_btn.pack(side='left', padx=(0, 10))
        
        self.clear_link_btn = tk.Button(map_button_frame, text="Hapus Link", 
                                       font=("Arial", 10), bg='#ea4335', fg='white',
                                       command=self.clear_map_link)
        self.clear_link_btn.pack(side='left')
        
        # Status link map
        self.map_status_label = tk.Label(map_frame, text="Tempel link berbagi Google Maps di sini", 
                                        bg='white', fg='#7f8c8d', font=("Arial", 10))
        self.map_status_label.pack(anchor='w', pady=(5, 0))
        
        # Tombol tambah
        add_btn = tk.Button(fields_frame, text="Tambah Properti", font=("Arial", 14, "bold"),
                           bg='#27ae60', fg='white', padx=30, pady=10,
                           command=self.add_property)
        add_btn.pack(pady=20)
        
        # Tombol bersihkan
        clear_btn = tk.Button(fields_frame, text="Bersihkan Form", font=("Arial", 12),
                             bg='#95a5a6', fg='white', padx=20, pady=8,
                             command=self.clear_add_form)
        clear_btn.pack(pady=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def select_image(self):
        """Select an image file for the property"""
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png *.gif *.bmp'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('PNG files', '*.png'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Property Image",
            filetypes=file_types
        )
        
        if filename:
            try:
                # Validate image file
                with Image.open(filename) as img:
                    # Check image size (optional validation)
                    if img.size[0] > 5000 or img.size[1] > 5000:
                        if not messagebox.askyesno("Large Image", 
                                                 "The selected image is very large. Continue anyway?"):
                            return
                
                self.selected_image_path = filename
                self.update_image_preview()
                self.remove_image_btn.config(state='normal')
                
            except Exception as e:
                messagebox.showerror("Error", f"Invalid image file: {str(e)}")
    
    def remove_image(self):
        """Remove the selected image"""
        self.selected_image_path = None
        self.update_image_preview()
        self.remove_image_btn.config(state='disabled')
    
    def update_image_preview(self):
        """Update the image preview display"""
        # Clear existing preview
        for widget in self.image_preview_frame.winfo_children():
            widget.destroy()
        
        if self.selected_image_path:
            try:
                # Create thumbnail
                with Image.open(self.selected_image_path) as img:
                    # Resize image for preview
                    img.thumbnail((200, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    # Display thumbnail
                    image_label = tk.Label(self.image_preview_frame, image=photo, bg='white')
                    image_label.image = photo  # Keep a reference
                    image_label.pack()
                    
                    # Display filename
                    filename = Path(self.selected_image_path).name
                    name_label = tk.Label(self.image_preview_frame, 
                                        text=f"Selected: {filename}", 
                                        bg='white', fg='#2c3e50', font=("Arial", 10))
                    name_label.pack(pady=(5, 0))
                    
            except Exception as e:
                error_label = tk.Label(self.image_preview_frame, 
                                     text=f"Error loading image: {str(e)}", 
                                     bg='white', fg='#e74c3c', font=("Arial", 10))
                error_label.pack()
        else:
            # No image selected
            self.image_preview_label = tk.Label(self.image_preview_frame, 
                                              text="No image selected", 
                                              bg='white', fg='#7f8c8d', font=("Arial", 10))
            self.image_preview_label.pack()
    
    def copy_image_to_storage(self, source_path, property_id):
        """Copy image file to the property images directory"""
        if not source_path:
            return None
            
        try:
            # Generate unique filename based on property ID and original extension
            source_path = Path(source_path)
            extension = source_path.suffix.lower()
            new_filename = f"property_{property_id}{extension}"
            destination = self.images_dir / new_filename
            
            # Copy file
            shutil.copy2(source_path, destination)
            return str(destination)
            
        except Exception as e:
            print(f"Failed to copy image: {str(e)}")
            return None
    
    def open_google_maps(self):
        """Buka Google Maps dengan lokasi properti untuk pemilihan lokasi"""
        try:
            # Ambil informasi lokasi dari form
            lokasi = self.property_fields['lokasi'].get().strip()
            
            # Buat query pencarian
            search_query = lokasi if lokasi else "lokasi properti"
            
            # URL encode the search query
            encoded_query = urllib.parse.quote(search_query)
            maps_url = f"https://maps.google.com/maps?q={encoded_query}"
            
            # Open in default browser
            webbrowser.open(maps_url)
            
            # Show instructions
            messagebox.showinfo("Instruksi Google Maps", 
                              "Google Maps telah dibuka di browser Anda.\n\n"
                              "Untuk mendapatkan link share:\n"
                              "1. Temukan lokasi yang benar\n"
                              "2. Klik tombol 'Bagikan' (Share)\n"
                              "3. Klik 'Salin link' (Copy link)\n"
                              "4. Tempel link di field Link Maps")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka Google Maps: {str(e)}")
    
    def validate_map_link(self):
        """Validate if the entered map link is a valid Google Maps link"""
        link = self.map_link_entry.get().strip()
        
        if not link:
            self.map_status_label.config(text="Please enter a maps link first", fg='#e74c3c')
            return
        
        # Check if it's a valid Google Maps link
        valid_patterns = [
            'maps.google.com',
            'maps.app.goo.gl',
            'goo.gl/maps',
            'google.com/maps'
        ]
        
        is_valid = any(pattern in link.lower() for pattern in valid_patterns)
        
        if is_valid:
            self.map_status_label.config(text="✓ Valid Google Maps link", fg='#27ae60')
        else:
            self.map_status_label.config(text="⚠ Please enter a valid Google Maps share link", fg='#f39c12')
    
    def clear_map_link(self):
        """Clear the map link entry"""
        self.map_link_entry.delete(0, tk.END)
        self.map_status_label.config(text="Paste Google Maps share link here", fg='#7f8c8d')
    
    def add_property(self):
        """Tambah properti baru ke database"""
        try:
            # Ambil data form
            nama_properti = self.property_fields['nama_properti'].get().strip()
            lokasi = self.property_fields['lokasi'].get().strip()
            tipe_properti = self.property_fields['tipe_properti'].get().strip()
            kamar_tidur = self.property_fields['kamar_tidur'].get().strip()
            kamar_mandi = self.property_fields['kamar_mandi'].get().strip()
            luas_bangunan = self.property_fields['luas_bangunan'].get().strip()
            harga = self.property_fields['harga'].get().strip()
            deskripsi = self.property_fields['deskripsi'].get('1.0', tk.END).strip()
            link_map = self.map_link_entry.get().strip()
            
            # Validasi field yang wajib diisi
            if not all([nama_properti, lokasi, tipe_properti]):
                messagebox.showerror("Error", "Harap isi semua field yang wajib diisi (Nama Properti, Lokasi, dan Tipe Properti)")
                return
            
            # Konversi field numerik
            kamar_tidur = int(kamar_tidur) if kamar_tidur else 0
            kamar_mandi = float(kamar_mandi) if kamar_mandi else 0
            luas_bangunan = int(luas_bangunan) if luas_bangunan else 0
            harga = float(harga) if harga else 0
            
            # Siapkan data properti untuk sinkronisasi Airtable
            property_data = {
                'nama_properti': nama_properti,
                'lokasi': lokasi,
                'tipe_properti': tipe_properti,
                'kamar_tidur': kamar_tidur,
                'kamar_mandi': kamar_mandi,
                'luas_bangunan': luas_bangunan,
                'harga': harga,
                'deskripsi': deskripsi,
                'link_map': link_map,
                'status': 'Tersedia'  # Status default untuk properti baru
            }
            
            # Tambahkan gambar jika ada yang dipilih
            if self.selected_image_path:
                property_data['gambar_path'] = self.selected_image_path
            
            # Coba sinkronisasi dengan Airtable terlebih dahulu
            airtable_record_id = None
            airtable_error = None
            try:
                airtable_record_id, airtable_error = self.airtable_sync.add_property_to_airtable(property_data)
            except Exception as e:
                airtable_error = f"Gagal sinkronisasi dengan Airtable: {str(e)}"
                print(airtable_error)
            
            # Insert ke database lokal terlebih dahulu untuk mendapatkan property ID
            self.cursor.execute('''
                INSERT INTO properties 
                (nama_properti, lokasi, tipe_properti, kamar_tidur, kamar_mandi, luas_bangunan, harga, deskripsi, link_map, ditambahkan_oleh, airtable_record_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nama_properti, lokasi, tipe_properti, kamar_tidur, kamar_mandi, luas_bangunan, harga, deskripsi, link_map, self.current_user['username'], airtable_record_id))
            
            # Dapatkan property ID untuk penyimpanan gambar
            property_id = self.cursor.lastrowid
            
            # Tangani penyimpanan gambar lokal
            stored_image_path = None
            if self.selected_image_path:
                stored_image_path = self.copy_image_to_storage(self.selected_image_path, property_id)
                if stored_image_path:
                    # Update record properti dengan path gambar
                    self.cursor.execute(
                        'UPDATE properties SET gambar_path=? WHERE id=?',
                        (stored_image_path, property_id)
                    )
            
            self.conn.commit()
            
            if airtable_record_id:
                sync_message = " dan berhasil disinkronkan ke Airtable"
                if stored_image_path:
                    sync_message += " (dengan gambar)"
                messagebox.showinfo("Berhasil", f"Properti berhasil ditambahkan{sync_message}!")
            else:
                error_details = f"Detail kegagalan:\n{airtable_error}" if airtable_error else "Tidak ada detail."
                messagebox.showwarning("Sinkronisasi Gagal", 
                                     f"Properti berhasil ditambahkan ke database lokal, "
                                     f"tapi gagal disinkronkan ke Airtable.\n\n"
                                     f"Harap periksa koneksi internet Anda dan konfigurasi Airtable.\n\n"
                                     f"{error_details}")
            
            self.clear_add_form()
            self.load_properties()
            
        except ValueError as e:
            messagebox.showerror("Error", "Harap masukkan nilai numerik yang valid untuk kamar tidur, kamar mandi, luas bangunan, dan harga")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah properti: {str(e)}")
    
    def clear_add_form(self):
        """Clear all form fields"""
        for field_name, widget in self.property_fields.items():
            if isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
            else:
                widget.delete(0, tk.END)
        
        # Clear image selection
        self.remove_image()
        
        # Clear map link
        self.clear_map_link()
    
    def load_properties(self):
        """Muat properti ke dalam tree view"""
        # Bersihkan item yang ada
        for item in self.properties_tree.get_children():
            self.properties_tree.delete(item)
        
        # Muat dari database
        self.cursor.execute('''
            SELECT id, nama_properti, lokasi, tipe_properti, kamar_tidur, kamar_mandi, luas_bangunan, harga, status
            FROM properties
            ORDER BY created_at DESC
        ''')
        
        properties = self.cursor.fetchall()
        
        for prop in properties:
            # Format harga dalam Rupiah
            harga_str = self.format_rupiah(prop[7]) if prop[7] else "Tidak ada"
            
            self.properties_tree.insert('', 'end', values=(
                prop[0], prop[1], prop[2], prop[3], prop[4], 
                prop[5], prop[6], harga_str, prop[8]
            ))
    
    def search_properties(self):
        """Cari properti berdasarkan kata kunci"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.load_properties()
            return
        
        # Bersihkan item yang ada
        for item in self.properties_tree.get_children():
            self.properties_tree.delete(item)
        
        # Cari di database
        self.cursor.execute('''
            SELECT id, nama_properti, lokasi, tipe_properti, kamar_tidur, kamar_mandi, luas_bangunan, harga, status
            FROM properties
            WHERE nama_properti LIKE ? OR lokasi LIKE ? OR tipe_properti LIKE ? OR deskripsi LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        properties = self.cursor.fetchall()
        
        for prop in properties:
            harga_str = self.format_rupiah(prop[7]) if prop[7] else "Tidak ada"
            
            self.properties_tree.insert('', 'end', values=(
                prop[0], prop[1], prop[2], prop[3], prop[4], 
                prop[5], prop[6], harga_str, prop[8]
            ))
    
    def edit_property(self):
        """Edit selected property"""
        selected_item = self.properties_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a property to edit")
            return
        
        property_id = self.properties_tree.item(selected_item[0])['values'][0]
        
        # Get property details
        self.cursor.execute('SELECT * FROM properties WHERE id = ?', (property_id,))
        property_data = self.cursor.fetchone()
        
        if not property_data:
            messagebox.showerror("Error", "Property not found")
            return
        
        # Create edit window
        self.create_edit_property_window(property_data)
    
    def create_edit_property_window(self, property_data):
        """Create edit property window"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Properti")
        edit_window.geometry("600x700")
        edit_window.configure(bg='white')
        
        # Create scrollable frame
        canvas = tk.Canvas(edit_window, bg='white')
        scrollbar = ttk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        fields_frame = tk.Frame(scrollable_frame, bg='white', padx=40, pady=20)
        fields_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(fields_frame, text="Edit Properti", 
                              font=("Arial", 18, "bold"), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Create form fields with existing data
        edit_fields = {}
        
        # Database schema: id(0), nama_properti(1), lokasi(2), tipe_properti(3), kamar_tidur(4), 
        # kamar_mandi(5), luas_bangunan(6), harga(7), status(8), deskripsi(9), 
        # gambar_path(10), link_map(11), ditambahkan_oleh(12), airtable_record_id(13)
        
        fields = [
            ('nama_properti', 'Nama Properti', 'text', property_data[1]),
            ('lokasi', 'Lokasi', 'text', property_data[2]),
            ('tipe_properti', 'Tipe Properti', 'combo', property_data[3]),
            ('kamar_tidur', 'Kamar Tidur', 'number', property_data[4]),
            ('kamar_mandi', 'Kamar Mandi', 'number', property_data[5]),
            ('luas_bangunan', 'Luas Bangunan (m²)', 'number', property_data[6]),
            ('harga', 'Harga (Rp)', 'number', property_data[7]),
            ('status', 'Status', 'combo', property_data[8]),
            ('deskripsi', 'Deskripsi', 'textarea', property_data[9]),
            ('link_map', 'Link Google Maps', 'text', property_data[11])
        ]
        
        for field_name, label, field_type, current_value in fields:
            field_frame = tk.Frame(fields_frame, bg='white')
            field_frame.pack(fill='x', pady=10)
            
            tk.Label(field_frame, text=f"{label}:", font=("Arial", 12), bg='white').pack(anchor='w')
            
            if field_type == 'text' or field_type == 'number':
                entry = tk.Entry(field_frame, font=("Arial", 12), width=40)
                entry.insert(0, str(current_value) if current_value else '')
                entry.pack(anchor='w', pady=(5, 0))
                edit_fields[field_name] = entry
            elif field_type == 'combo':
                combo = ttk.Combobox(field_frame, font=("Arial", 12), width=37)
                if field_name == 'tipe_properti':
                    combo['values'] = self.get_property_types()
                elif field_name == 'status':
                    combo['values'] = ['Tersedia', 'Terjual', 'Pending', 'Disewa']
                combo.set(current_value if current_value else '')
                combo.pack(anchor='w', pady=(5, 0))
                edit_fields[field_name] = combo
            elif field_type == 'textarea':
                text_widget = tk.Text(field_frame, font=("Arial", 12), width=40, height=4)
                text_widget.insert('1.0', current_value if current_value else '')
                text_widget.pack(anchor='w', pady=(5, 0))
                edit_fields[field_name] = text_widget
        
        # Buttons
        buttons_frame = tk.Frame(fields_frame, bg='white')
        buttons_frame.pack(pady=20)
        
        save_btn = tk.Button(buttons_frame, text="Simpan Perubahan", font=("Arial", 12, "bold"),
                           bg='#27ae60', fg='white', padx=20, pady=10,
                           command=lambda: self.save_property_changes(property_data[0], edit_fields, edit_window))
        save_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(buttons_frame, text="Batal", font=("Arial", 12),
                              bg='#95a5a6', fg='white', padx=20, pady=10,
                              command=edit_window.destroy)
        cancel_btn.pack(side='left', padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def save_property_changes(self, property_id, edit_fields, edit_window):
        """Save changes to property"""
        try:
            # Get form data
            nama_properti = edit_fields['nama_properti'].get().strip()
            lokasi = edit_fields['lokasi'].get().strip()
            tipe_properti = edit_fields['tipe_properti'].get().strip()
            kamar_tidur = edit_fields['kamar_tidur'].get().strip()
            kamar_mandi = edit_fields['kamar_mandi'].get().strip()
            luas_bangunan = edit_fields['luas_bangunan'].get().strip()
            harga = edit_fields['harga'].get().strip()
            status = edit_fields['status'].get().strip()
            deskripsi = edit_fields['deskripsi'].get('1.0', tk.END).strip()
            link_map = edit_fields['link_map'].get().strip()
            
            # Validate required fields
            if not all([nama_properti, lokasi, tipe_properti]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Convert numeric fields
            kamar_tidur = int(kamar_tidur) if kamar_tidur else 0
            kamar_mandi = float(kamar_mandi) if kamar_mandi else 0
            luas_bangunan = int(luas_bangunan) if luas_bangunan else 0
            harga = float(harga) if harga else 0
            
            # Get current Airtable record ID
            self.cursor.execute('SELECT airtable_record_id FROM properties WHERE id=?', (property_id,))
            result = self.cursor.fetchone()
            airtable_record_id = result[0] if result else None
            
            # Prepare property data for Airtable sync
            property_data = {
                'nama_properti': nama_properti,
                'lokasi': lokasi,
                'tipe_properti': tipe_properti,
                'kamar_tidur': kamar_tidur,
                'kamar_mandi': kamar_mandi,
                'luas_bangunan': luas_bangunan,
                'harga': harga,
                'deskripsi': deskripsi,
                'status': status,
                'link_map': link_map
            }
            
            # Log the edit attempt (simplified)
            print(f"📝 Editing property {property_id} with data: {property_data}")
            
            # Try to sync with Airtable
            airtable_sync_success = False
            airtable_error = None
            if airtable_record_id:
                try:
                    print(f"🔄 Updating property in Airtable record: {airtable_record_id}")
                    print(f"🔄 Sync attempt for record: {airtable_record_id}")
                    
                    print(f"📝 Sending property update to Airtable with data: {property_data}")
                    airtable_sync_success, airtable_error = self.airtable_sync.update_property_in_airtable(airtable_record_id, property_data)
                    
                    if not airtable_sync_success:
                        print(f"❌ Airtable sync failed: {airtable_error}")
                        print(f"❌ Sync failure for record: {airtable_record_id}")
                    else:
                        print(f"✅ Airtable sync successful")
                        print(f"✅ Sync success for record: {airtable_record_id}")
                        
                except Exception as e:
                    airtable_error = f"Exception during Airtable sync: {str(e)}"
                    print(f"❌ {airtable_error}")
                    print(f"❌ Exception sync failure for record: {airtable_record_id}")
                    airtable_sync_success = False
            
            # Update in database
            print(f"💾 Updating database record for property {property_id}")
            self.cursor.execute('''
                UPDATE properties 
                SET nama_properti=?, lokasi=?, tipe_properti=?, kamar_tidur=?, kamar_mandi=?, 
                    luas_bangunan=?, harga=?, status=?, deskripsi=?, link_map=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (nama_properti, lokasi, tipe_properti, kamar_tidur, kamar_mandi, 
                  luas_bangunan, harga, status, deskripsi, link_map, property_id))
            
            self.conn.commit()
            
            if airtable_sync_success:
                messagebox.showinfo("Berhasil", "Properti berhasil diupdate dan disinkronkan ke Airtable.")
            else:
                if airtable_record_id:
                    # Show simple error message instead of enhanced dialog
                    messagebox.showwarning("Sinkronisasi Gagal", 
                                         f"Properti berhasil diupdate dalam database lokal, "
                                         f"tapi sinkronisasi ke Airtable gagal.\n\n"
                                         f"Error: {airtable_error or 'Unknown error'}")
                else: # No airtable_id to begin with
                    messagebox.showinfo("Berhasil", "Properti berhasil diupdate (tidak ada record Airtable untuk disinkronkan).")
            
            edit_window.destroy()
            self.load_properties()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numeric values")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update property: {str(e)}")
    
    def delete_property(self):
        """Delete selected property"""
        selected_item = self.properties_tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Harap pilih properti yang akan dihapus")
            return
        
        property_id = self.properties_tree.item(selected_item[0])['values'][0]
        nama_properti = self.properties_tree.item(selected_item[0])['values'][1]
        
        # Confirm deletion
        if messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus properti:\n{nama_properti}?"):
            try:
                # Get Airtable record ID before deleting
                self.cursor.execute('SELECT airtable_record_id FROM properties WHERE id = ?', (property_id,))
                result = self.cursor.fetchone()
                airtable_record_id = result[0] if result else None
                
                # Try to delete from Airtable first
                airtable_delete_success = False
                airtable_error = None
                if airtable_record_id:
                    try:
                        airtable_delete_success, airtable_error = self.airtable_sync.delete_property_from_airtable(airtable_record_id)
                    except Exception as e:
                        airtable_error = f"Gagal menghapus dari Airtable: {str(e)}"
                        print(airtable_error)
                
                # Delete from local database
                self.cursor.execute('DELETE FROM properties WHERE id = ?', (property_id,))
                self.conn.commit()
                
                if airtable_delete_success:
                    messagebox.showinfo("Berhasil", "Properti berhasil dihapus dari database lokal dan Airtable.")
                else:
                    if airtable_record_id:
                        error_details = f"Detail kegagalan:\n{airtable_error}" if airtable_error else "Tidak ada detail."
                        messagebox.showwarning("Sinkronisasi Gagal", 
                                             f"Properti berhasil dihapus dari database lokal, "
                                             f"tapi gagal dihapus dari Airtable.\n\n"
                                             f"{error_details}")
                    else:
                        messagebox.showinfo("Berhasil", "Properti berhasil dihapus (tidak ada record Airtable untuk dihapus).")

                self.load_properties()
                
            except Exception as e:
                messagebox.showerror("Error Hapus", f"Gagal menghapus properti: {str(e)}")
    
    def update_property_status(self):
        """Update status properti yang dipilih"""
        selected_item = self.properties_tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Harap pilih properti untuk mengupdate status")
            return
        
        property_id = self.properties_tree.item(selected_item[0])['values'][0]
        current_status = self.properties_tree.item(selected_item[0])['values'][7]  # Status di index 7 untuk schema baru
        
        # Buat window update status
        status_window = tk.Toplevel(self.root)
        status_window.title("Update Status Properti")
        status_window.geometry("400x250")  # Increased height from 200 to 250
        status_window.configure(bg='white')
        status_window.resizable(False, False)  # Prevent resizing to maintain fixed layout
        
        # Center the window
        status_window.transient(self.root)
        status_window.grab_set()
        
        # Center the window on screen
        status_window.update_idletasks()
        width = status_window.winfo_width()
        height = status_window.winfo_height()
        x = (status_window.winfo_screenwidth() // 2) - (width // 2)
        y = (status_window.winfo_screenheight() // 2) - (height // 2)
        status_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Content frame
        content_frame = tk.Frame(status_window, bg='white', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Title label
        title_label = tk.Label(content_frame, text="Pilih Status Baru:", font=("Arial", 14, "bold"), bg='white')
        title_label.pack(pady=(0, 15))
        
        # Radio buttons frame
        radio_frame = tk.Frame(content_frame, bg='white')
        radio_frame.pack(pady=(0, 20))
        
        status_var = tk.StringVar(value=current_status)
        
        statuses = ['Tersedia', 'Terjual']  # Hanya 2 status
        for status in statuses:
            radio_btn = tk.Radiobutton(radio_frame, text=status, variable=status_var, 
                                     value=status, font=("Arial", 12), bg='white', 
                                     activebackground='white')
            radio_btn.pack(anchor='w', pady=3)
        
        # Separator line
        separator = tk.Frame(content_frame, bg='#e0e0e0', height=1)
        separator.pack(fill='x', pady=(10, 15))
        
        # Tombol frame
        buttons_frame = tk.Frame(content_frame, bg='white')
        buttons_frame.pack(side='bottom', fill='x')
        
        # Center the buttons horizontally
        button_container = tk.Frame(buttons_frame, bg='white')
        button_container.pack()
        
        update_btn = tk.Button(button_container, text="Update", font=("Arial", 11, "bold"),
                              bg='#3498db', fg='white', padx=25, pady=8,
                              command=lambda: self.save_status_update(property_id, status_var.get(), status_window),
                              cursor='hand2')
        update_btn.pack(side='left', padx=8)
        
        cancel_btn = tk.Button(button_container, text="Batal", font=("Arial", 11),
                              bg='#95a5a6', fg='white', padx=25, pady=8,
                              command=status_window.destroy,
                              cursor='hand2')
        cancel_btn.pack(side='left', padx=8)
    
    def save_status_update(self, property_id, new_status, status_window):
        """Simpan update status ke database"""
        try:
            # Dapatkan data properti saat ini dan Airtable record ID
            self.cursor.execute('SELECT * FROM properties WHERE id=?', (property_id,))
            property_row = self.cursor.fetchone()
            
            if not property_row:
                messagebox.showerror("Error", "Properti tidak ditemukan")
                return
            
            airtable_record_id = property_row[13]  # airtable_record_id di index 13 untuk schema baru (0-based)
            
            # Jika ada record Airtable, sinkronkan update status
            airtable_sync_success = False
            if airtable_record_id:
                try:
                    print(f"🔄 Updating status to '{new_status}' for Airtable record: {airtable_record_id}")
                    
                    # Siapkan data properti untuk sinkronisasi Airtable
                    property_data = {
                        'nama_properti': property_row[1],
                        'lokasi': property_row[2],
                        'tipe_properti': property_row[3],
                        'kamar_tidur': property_row[4],
                        'kamar_mandi': property_row[5],
                        'luas_bangunan': property_row[6],
                        'harga': property_row[7],
                        'status': new_status,  # Status yang diupdate
                        'deskripsi': property_row[9],
                        'link_map': property_row[11]
                    }
                    
                    print(f"📝 Sending status update to Airtable: status = '{new_status}'")
                    airtable_sync_success, error_msg = self.airtable_sync.update_property_in_airtable(airtable_record_id, property_data)
                    
                    if not airtable_sync_success and error_msg:
                        print(f"❌ Airtable sync failed: {error_msg}")
                    else:
                        print(f"✅ Airtable sync successful for status: '{new_status}'")
                        
                except Exception as e:
                    print(f"❌ Exception during Airtable sync: {str(e)}")
                    airtable_sync_success = False
            
            # Update di database lokal
            self.cursor.execute(
                'UPDATE properties SET status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?',
                (new_status, property_id)
            )
            self.conn.commit()
            
            sync_message = ""
            if airtable_record_id:
                if airtable_sync_success:
                    sync_message = " dan berhasil disinkronkan ke Airtable"
                else:
                    sync_message = " (Sinkronisasi Airtable gagal - periksa koneksi)"
            else:
                sync_message = " (tidak ada record Airtable untuk disinkronkan)"
            
            messagebox.showinfo("Berhasil", f"Status properti berhasil diupdate ke '{new_status}'{sync_message}!")
            status_window.destroy()
            self.load_properties()
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengupdate status: {str(e)}")
    
    def create_user_dialog(self):
        """Create new user dialog (admin only)"""
        if self.current_user['role'] != 'admin':
            messagebox.showerror("Error", "Only administrators can create users")
            return
        
        # Create user window
        user_window = tk.Toplevel(self.root)
        user_window.title("Create New User")
        user_window.geometry("400x300")
        user_window.configure(bg='white')
        
        # Center the window
        user_window.transient(self.root)
        user_window.grab_set()
        
        # Content frame
        content_frame = tk.Frame(user_window, bg='white', padx=30, pady=30)
        content_frame.pack(fill='both', expand=True)
        
        tk.Label(content_frame, text="Create New User", font=("Arial", 16, "bold"), bg='white').pack(pady=(0, 20))
        
        # Username
        tk.Label(content_frame, text="Username:", font=("Arial", 12), bg='white').pack(anchor='w')
        username_entry = tk.Entry(content_frame, font=("Arial", 12), width=25)
        username_entry.pack(pady=(5, 15))
        
        # Password
        tk.Label(content_frame, text="Password:", font=("Arial", 12), bg='white').pack(anchor='w')
        password_entry = tk.Entry(content_frame, font=("Arial", 12), width=25, show='*')
        password_entry.pack(pady=(5, 15))
        
        # Role
        tk.Label(content_frame, text="Role:", font=("Arial", 12), bg='white').pack(anchor='w')
        role_var = tk.StringVar(value='user')
        role_combo = ttk.Combobox(content_frame, textvariable=role_var, values=['user', 'admin'], width=22)
        role_combo.pack(pady=(5, 20))
        
        # Buttons
        buttons_frame = tk.Frame(content_frame, bg='white')
        buttons_frame.pack()
        
        create_btn = tk.Button(buttons_frame, text="Create User", font=("Arial", 12, "bold"),
                              bg='#27ae60', fg='white', padx=20, pady=10,
                              command=lambda: self.create_new_user(username_entry.get(), password_entry.get(), 
                                                                    role_var.get(), user_window))
        create_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(buttons_frame, text="Cancel", font=("Arial", 12),
                              bg='#95a5a6', fg='white', padx=20, pady=10,
                              command=user_window.destroy)
        cancel_btn.pack(side='left', padx=10)
    
    def create_new_user(self, username, password, role, user_window):
        """Create new user in database"""
        try:
            if not username or not password:
                messagebox.showerror("Error", "Username and password are required")
                return
            
            if len(password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters long")
                return
            
            password_hash = self.hash_password(password)
            
            self.cursor.execute(
                'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                (username, password_hash, role)
            )
            self.conn.commit()
            
            messagebox.showinfo("Success", f"User '{username}' created successfully!")
            user_window.destroy()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user: {str(e)}")
    
    def change_password_dialog(self):
        """Change password dialog"""
        # Create password change window
        pwd_window = tk.Toplevel(self.root)
        pwd_window.title("Change Password")
        pwd_window.geometry("400x250")
        pwd_window.configure(bg='white')
        
        # Center the window
        pwd_window.transient(self.root)
        pwd_window.grab_set()
        
        # Content frame
        content_frame = tk.Frame(pwd_window, bg='white', padx=30, pady=30)
        content_frame.pack(fill='both', expand=True)
        
        tk.Label(content_frame, text="Change Password", font=("Arial", 16, "bold"), bg='white').pack(pady=(0, 20))
        
        # Current password
        tk.Label(content_frame, text="Current Password:", font=("Arial", 12), bg='white').pack(anchor='w')
        current_pwd_entry = tk.Entry(content_frame, font=("Arial", 12), width=25, show='*')
        current_pwd_entry.pack(pady=(5, 15))
        
        # New password
        tk.Label(content_frame, text="New Password:", font=("Arial", 12), bg='white').pack(anchor='w')
        new_pwd_entry = tk.Entry(content_frame, font=("Arial", 12), width=25, show='*')
        new_pwd_entry.pack(pady=(5, 20))
        
        # Buttons
        buttons_frame = tk.Frame(content_frame, bg='white')
        buttons_frame.pack()
        
        change_btn = tk.Button(buttons_frame, text="Change Password", font=("Arial", 12, "bold"),
                              bg='#3498db', fg='white', padx=20, pady=10,
                              command=lambda: self.change_user_password(current_pwd_entry.get(), 
                                                                       new_pwd_entry.get(), pwd_window))
        change_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(buttons_frame, text="Cancel", font=("Arial", 12),
                              bg='#95a5a6', fg='white', padx=20, pady=10,
                              command=pwd_window.destroy)
        cancel_btn.pack(side='left', padx=10)
    
    def change_user_password(self, current_password, new_password, pwd_window):
        """Change user password"""
        try:
            if not current_password or not new_password:
                messagebox.showerror("Error", "Both passwords are required")
                return
            
            if len(new_password) < 6:
                messagebox.showerror("Error", "New password must be at least 6 characters long")
                return
            
            # Verify current password
            current_hash = self.hash_password(current_password)
            self.cursor.execute('SELECT id FROM users WHERE id = ? AND password_hash = ?', 
                               (self.current_user['id'], current_hash))
            
            if not self.cursor.fetchone():
                messagebox.showerror("Error", "Current password is incorrect")
                return
            
            # Update password
            new_hash = self.hash_password(new_password)
            self.cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', 
                               (new_hash, self.current_user['id']))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Password changed successfully!")
            pwd_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {str(e)}")
    
    def test_airtable_connection(self):
        """Test connection to Airtable"""
        try:
            if self.airtable_sync.test_connection():
                messagebox.showinfo("Success", "Airtable connection successful!\nYour properties will be automatically synced.")
            else:
                messagebox.showerror("Error", "Failed to connect to Airtable.\nPlease check your configuration in airtable_config.py")
        except Exception as e:
            messagebox.showerror("Error", f"Airtable connection test failed:\n{str(e)}\n\nPlease check your configuration in airtable_config.py")
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.create_login_interface()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
        
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    app = PropertyManager()
    app.run() 