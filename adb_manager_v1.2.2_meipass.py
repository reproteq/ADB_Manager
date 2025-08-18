import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import subprocess
import threading
import os
import time
import socket
import platform
import sys

# ========== CONFIGURACIÓN GLOBAL ==========
APP_VERSION = "1.2"
APP_TITLE = "ADB Manager"
DEVELOPER = "Alex G.T"
COMPANY = "REPROTEQ 2025"
DEFAULT_IP = "192.168.1.80"

# CONFIGURACIÓN DE VENTANA
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 850

def get_resource_path(relative_path):
    """Obtener ruta de recursos incluidos en el ejecutable"""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def get_adb_path():
    """Obtener ruta del adb.exe incluido"""
    # Intentar diferentes ubicaciones
    possible_paths = [
        get_resource_path("adb_tools/adb.exe"),  # Empaquetado
        get_resource_path("adb.exe"),            # En la raíz
        os.path.join(os.path.dirname(sys.executable), "adb_tools", "adb.exe"),  # Junto al exe
        os.path.join(os.path.dirname(sys.executable), "adb.exe"),  # Junto al exe directo
        "adb"  # PATH del sistema (fallback)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return "adb"  # Fallback al PATH del sistema

class ADBFileManagerFixed:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_TITLE} v.{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.connected = False
        self.device_ip = tk.StringVar(value=DEFAULT_IP)
        self.device_port = tk.StringVar()
        self.pairing_code = tk.StringVar()
        self.selected_file = tk.StringVar()
        self.target_device = None  # Dispositivo específico conectado
        
        self.setup_ui()
        self.check_adb()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Título
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(title_frame, text=f"📱 {APP_TITLE} V.{APP_VERSION}", 
                font=('Arial', 18, 'bold'), fg='#ecf0f1', bg='#2c3e50').pack()
        
        # Frame de conexión
        self.create_connection_frame()
        
        # Frame de archivos
        self.create_file_frame()
        
        # Frame de herramientas
        self.create_tools_frame()
        
        # Frame de consola ADB (NUEVO)
        self.create_console_frame()
        
        # Log
        self.create_log_frame()
        
        self.log(f"🚀 {COMPANY}")
        self.log(f"🚀 Desarrollado por {DEVELOPER}")
        self.log(f"🚀 {APP_TITLE} v{APP_VERSION}")
    
    def create_connection_frame(self):
        """Crear frame de conexión"""
        conn_frame = tk.LabelFrame(self.root, text="🔗 Conexión", 
                                  font=('Arial', 12, 'bold'), 
                                  fg='#ecf0f1', bg='#34495e', bd=2)
        conn_frame.pack(fill='x', padx=10, pady=5)
        
        # IP y Puerto
        ip_frame = tk.Frame(conn_frame, bg='#34495e')
        ip_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(ip_frame, text="IP:", fg='#ecf0f1', bg='#34495e', 
                font=('Arial', 10, 'bold')).pack(side='left')
        
        self.ip_entry = tk.Entry(ip_frame, textvariable=self.device_ip, width=15, 
                               font=('Arial', 10))
        self.ip_entry.pack(side='left', padx=(5,10))
        
        tk.Label(ip_frame, text="Puerto:", fg='#ecf0f1', bg='#34495e',
                font=('Arial', 10, 'bold')).pack(side='left')
        
        self.port_entry = tk.Entry(ip_frame, textvariable=self.device_port, width=8, 
                                 font=('Arial', 10))
        self.port_entry.pack(side='left', padx=5)
        
        tk.Label(ip_frame, text="Código:", fg='#ecf0f1', bg='#34495e',
                font=('Arial', 10, 'bold')).pack(side='left', padx=(20,5))
        
        self.code_entry = tk.Entry(ip_frame, textvariable=self.pairing_code, width=8, 
                                 font=('Arial', 10))
        self.code_entry.pack(side='left', padx=5)
        
        # Placeholders
        self.add_placeholder(self.port_entry, self.device_port, "Puerto")
        self.add_placeholder(self.code_entry, self.pairing_code, "Código")
        
        # Botones de conexión
        btn_frame = tk.Frame(conn_frame, bg='#34495e')
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.connect_btn = tk.Button(btn_frame, text="🔗 Conectar", 
                                    command=self.connect_clean,
                                    bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                                    relief='flat', padx=15)
        self.connect_btn.pack(side='left', padx=5)
        
        self.pair_btn = tk.Button(btn_frame, text="🔗 Emparejar", 
                                 command=self.pair_device,
                                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                                 relief='flat', padx=15)
        self.pair_btn.pack(side='left', padx=5)
        
        self.usb_btn = tk.Button(btn_frame, text="🔌 USB", 
                                command=self.connect_usb,
                                bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                relief='flat', padx=15)
        self.usb_btn.pack(side='left', padx=5)
        
        self.disconnect_btn = tk.Button(btn_frame, text="❌ Desconectar", 
                                       command=self.disconnect_clean,
                                       bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                                       relief='flat', padx=15, state='disabled')
        self.disconnect_btn.pack(side='left', padx=5)
        
        # Botón de limpieza forzada
        self.clean_btn = tk.Button(btn_frame, text="🧹 Limpiar Todo", 
                                  command=self.force_clean_all,
                                  bg='#8e44ad', fg='white', font=('Arial', 10, 'bold'),
                                  relief='flat', padx=15)
        self.clean_btn.pack(side='left', padx=5)
        
        self.status_label = tk.Label(btn_frame, text="● Desconectado", 
                                    fg='#e74c3c', bg='#34495e', font=('Arial', 10, 'bold'))
        self.status_label.pack(side='right', padx=10)
        
        # Info de dispositivo
        self.device_info_label = tk.Label(conn_frame, text="Dispositivo: Ninguno", 
                                         fg='#95a5a6', bg='#34495e', font=('Arial', 9))
        self.device_info_label.pack(pady=2)
    
    def add_placeholder(self, entry, var, placeholder_text):
        """Agregar placeholder a un Entry"""
        var.set(placeholder_text)
        entry.config(fg='grey')
        
        def on_focus_in(event):
            if var.get() == placeholder_text:
                var.set("")
                entry.config(fg='black')
        
        def on_focus_out(event):
            if var.get() == '':
                var.set(placeholder_text)
                entry.config(fg='grey')
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
    
    def create_file_frame(self):
        """Crear frame de archivos"""
        file_frame = tk.LabelFrame(self.root, text="📁 Gestión de Archivos", 
                                  font=('Arial', 12, 'bold'), 
                                  fg='#ecf0f1', bg='#34495e', bd=2)
        file_frame.pack(fill='x', padx=10, pady=5)
        
        # Selección de archivo
        select_frame = tk.Frame(file_frame, bg='#34495e')
        select_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(select_frame, text="📂 Seleccionar Archivo", 
                 command=self.select_file,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                 relief='flat', padx=15).pack(side='left')
        
        self.file_label = tk.Label(select_frame, text="Ningún archivo seleccionado", 
                                  fg='#bdc3c7', bg='#34495e', font=('Arial', 9))
        self.file_label.pack(side='left', padx=(10,0))
        
        # Botones de acción
        action_frame = tk.Frame(file_frame, bg='#34495e')
        action_frame.pack(fill='x', padx=10, pady=5)
        
        self.install_btn = tk.Button(action_frame, text="📦 Instalar APK", 
                                    command=self.install_apk,
                                    bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                                    relief='flat', padx=15, state='disabled')
        self.install_btn.pack(side='left', padx=5)
        
        self.push_btn = tk.Button(action_frame, text="📤 Enviar Archivo", 
                                 command=self.push_file,
                                 bg='#2980b9', fg='white', font=('Arial', 10, 'bold'),
                                 relief='flat', padx=15, state='disabled')
        self.push_btn.pack(side='left', padx=5)
        
        self.pull_btn = tk.Button(action_frame, text="📥 Descargar Archivo", 
                                 command=self.pull_file,
                                 bg='#8e44ad', fg='white', font=('Arial', 10, 'bold'),
                                 relief='flat', padx=15, state='disabled')
        self.pull_btn.pack(side='left', padx=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(action_frame, mode='indeterminate')
        self.progress.pack(side='right', padx=(10,0), fill='x', expand=True)
    
    def create_tools_frame(self):
        """Crear frame de herramientas"""
        tools_frame = tk.LabelFrame(self.root, text="🛠️ Herramientas", 
                                   font=('Arial', 12, 'bold'), 
                                   fg='#ecf0f1', bg='#34495e', bd=2)
        tools_frame.pack(fill='x', padx=10, pady=5)
        
        btn_frame = tk.Frame(tools_frame, bg='#34495e')
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="📊 Estado ADB", 
                 command=self.show_adb_status,
                 bg='#e67e22', fg='white', font=('Arial', 9, 'bold'),
                 relief='flat', padx=10).pack(side='left', padx=2)
        
        tk.Button(btn_frame, text="📱 Info Dispositivo", 
                 command=self.device_info,
                 bg='#34495e', fg='white', font=('Arial', 9, 'bold'),
                 relief='flat', padx=10).pack(side='left', padx=2)
        
        tk.Button(btn_frame, text="📋 Apps Instaladas", 
                 command=self.list_apps,
                 bg='#34495e', fg='white', font=('Arial', 9, 'bold'),
                 relief='flat', padx=10).pack(side='left', padx=2)
        
        tk.Button(btn_frame, text="📸 Captura", 
                 command=self.screenshot,
                 bg='#34495e', fg='white', font=('Arial', 9, 'bold'),
                 relief='flat', padx=10).pack(side='left', padx=2)
        
        tk.Button(btn_frame, text="🔄 Reiniciar ADB", 
                 command=self.restart_adb,
                 bg='#34495e', fg='white', font=('Arial', 9, 'bold'),
                 relief='flat', padx=10).pack(side='left', padx=2)
        
        tk.Button(btn_frame, text="🔍 Escanear Red", 
                 command=self.scan_network,
                 bg='#34495e', fg='white', font=('Arial', 9, 'bold'),
                 relief='flat', padx=10).pack(side='left', padx=2)
    
    def create_console_frame(self):
        """Crear frame de consola ADB (NUEVO)"""
        console_frame = tk.LabelFrame(self.root, text="💻 Consola ADB", 
                                     font=('Arial', 12, 'bold'), 
                                     fg='#ecf0f1', bg='#34495e', bd=2)
        console_frame.pack(fill='x', padx=10, pady=5)
        
        # Frame de entrada de comando
        input_frame = tk.Frame(console_frame, bg='#34495e')
        input_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(input_frame, text="Comando:", fg='#ecf0f1', bg='#34495e', 
                font=('Arial', 10, 'bold')).pack(side='left')
        
        self.command_var = tk.StringVar()
        self.command_entry = tk.Entry(input_frame, textvariable=self.command_var, 
                                     font=('Consolas', 10), bg='#2c3e50', fg='#ecf0f1',
                                     insertbackground='#ecf0f1')
        self.command_entry.pack(side='left', fill='x', expand=True, padx=(10, 5))
        
        # Bind Enter para ejecutar comando
        self.command_entry.bind('<Return>', lambda e: self.execute_custom_command())
        
        tk.Button(input_frame, text="▶️ Ejecutar", 
                 command=self.execute_custom_command,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                 relief='flat', padx=15).pack(side='right')
        
        # Frame de comandos rápidos
        quick_frame = tk.Frame(console_frame, bg='#34495e')
        quick_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(quick_frame, text="Comandos rápidos:", fg='#95a5a6', bg='#34495e', 
                font=('Arial', 9)).pack(anchor='w')
        
        # Frame de comandos rápidos
        quick_frame = tk.Frame(console_frame, bg='#34495e')
        quick_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(quick_frame, text="Comandos rápidos:", fg='#95a5a6', bg='#34495e', 
                font=('Arial', 9)).pack(anchor='w')
        
        # Comandos organizados de forma más compacta
        quick_commands = [
            # Fila 1 - Básicos
            ("📱 devices", "adb devices"),
            ("ℹ️ info", "adb shell getprop ro.build.version.release"),
            ("🔄 reboot", "adb reboot"),
            ("🏠 shell", "adb shell"),
            ("📊 logcat", "adb logcat -d"),
            
            # Fila 2 - Archivos
            ("🗂️ /sdcard", "adb shell ls -la /sdcard"),
            ("📥 Download", "adb shell ls -la /sdcard/Download"),
            ("💾 storage", "adb shell df -h"),
            ("🔋 battery", "adb shell dumpsys battery | grep level"),
            ("📋 packages", "adb shell pm list packages -3"),
            
            # Fila 3 - Sistema
            ("🔢 processes", "adb shell ps"),
            ("📊 meminfo", "adb shell cat /proc/meminfo | head -10"),
            ("🔊 volume", "adb shell media volume --show"),
            ("💡 brightness", "adb shell settings get system screen_brightness"),
            ("📡 wifi", "adb shell dumpsys wifi | head -20"),
            
            # Fila 4 - Avanzado
            ("🗑️ uninstall", "adb uninstall"),
            ("⚡ recovery", "adb reboot recovery"),
            ("✈️ airplane", "adb shell settings get global airplane_mode_on"),
            ("📶 data", "adb shell svc data enable"),
            ("🧹 clear", "clear")
        ]
        
        # Crear botones en filas de 5
        buttons_per_row = 5
        for i in range(0, len(quick_commands), buttons_per_row):
            row_frame = tk.Frame(quick_frame, bg='#34495e')
            row_frame.pack(fill='x', pady=1)
            
            for j in range(buttons_per_row):
                if i + j < len(quick_commands):
                    text, cmd = quick_commands[i + j]
                    btn = tk.Button(row_frame, text=text, 
                                   command=lambda c=cmd: self.set_quick_command(c),
                                   bg='#95a5a6', fg='white', font=('Arial', 8),
                                   relief='flat', padx=3, pady=2, width=12)
                    btn.pack(side='left', padx=1, pady=1)
        
        # Área de salida de comandos
        output_frame = tk.Frame(console_frame, bg='#34495e')
        output_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(output_frame, text="Salida:", fg='#95a5a6', bg='#34495e', 
                font=('Arial', 9)).pack(anchor='w')
        
        self.command_output = scrolledtext.ScrolledText(output_frame, height=8, 
                                                       bg='#1e1e1e', fg='#00ff00',
                                                       font=('Consolas', 9))
        self.command_output.pack(fill='x', pady=2)
        
        # Frame de botones de la consola
        console_btn_frame = tk.Frame(output_frame, bg='#34495e')
        console_btn_frame.pack(fill='x', pady=2)
        
        tk.Button(console_btn_frame, text="🧹 Limpiar Salida", 
                 command=self.clear_command_output,
                 bg='#95a5a6', fg='white', font=('Arial', 9),
                 relief='flat', padx=10).pack(side='left', padx=2)
        
        tk.Button(console_btn_frame, text="💾 Guardar Salida", 
                 command=self.save_command_output,
                 bg='#95a5a6', fg='white', font=('Arial', 9),
                 relief='flat', padx=10).pack(side='left', padx=2)
        
        tk.Button(console_btn_frame, text="📋 Copiar Salida", 
                 command=self.copy_command_output,
                 bg='#95a5a6', fg='white', font=('Arial', 9),
                 relief='flat', padx=10).pack(side='left', padx=2)
        
        tk.Button(console_btn_frame, text="⚠️ Kill Logcat", 
                 command=self.kill_logcat,
                 bg='#e74c3c', fg='white', font=('Arial', 9),
                 relief='flat', padx=10).pack(side='right', padx=2)
    
    def set_quick_command(self, command):
        """Establecer comando rápido en el campo de entrada"""
        if command == "clear":
            self.clear_command_output()
        else:
            self.command_var.set(command)
            self.command_entry.focus()
    
    def execute_custom_command(self):
        """Ejecutar comando ADB personalizado"""
        command = self.command_var.get().strip()
        
        if not command:
            self.show_command_output("❌ Error: Comando vacío\n")
            return
        
        # Si no empieza con 'adb', agregarlo
        if not command.startswith('adb'):
            command = f"adb {command}"
        
        # Si hay dispositivo conectado y no especifica dispositivo, agregarlo
        if self.target_device and '-s' not in command:
            # Insertar -s después de 'adb'
            parts = command.split(' ', 1)
            if len(parts) == 2:
                command = f"{parts[0]} -s \"{self.target_device}\" {parts[1]}"
        
        self.show_command_output(f"$ {command}\n")
        
        def execute_thread():
            try:
                # Ejecutar comando
                code, stdout, stderr = self.run_command(command, timeout=60)
                
                output = ""
                if stdout:
                    output += stdout
                if stderr:
                    output += f"\nERROR:\n{stderr}"
                
                if code == 0:
                    self.root.after(0, lambda: self.show_command_output(f"{output}\n✅ Comando ejecutado exitosamente\n\n"))
                else:
                    self.root.after(0, lambda: self.show_command_output(f"{output}\n❌ Error (código: {code})\n\n"))
                
            except Exception as e:
                self.root.after(0, lambda: self.show_command_output(f"❌ Excepción: {str(e)}\n\n"))
        
        threading.Thread(target=execute_thread, daemon=True).start()
        
        # Limpiar campo de entrada
        self.command_var.set("")
    
    def show_command_output(self, text):
        """Mostrar salida en el área de comandos"""
        self.command_output.insert(tk.END, text)
        self.command_output.see(tk.END)
        self.root.update_idletasks()
    
    def save_command_output(self):
        """Guardar salida de comandos en archivo"""
        output_text = self.command_output.get(1.0, tk.END)
        if not output_text.strip():
            messagebox.showwarning("Advertencia", "No hay salida para guardar")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Guardar salida de comandos",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                self.log(f"✅ Salida guardada en: {os.path.basename(file_path)}")
                messagebox.showinfo("Éxito", f"Salida guardada en:\n{file_path}")
            except Exception as e:
                self.log(f"❌ Error guardando salida: {e}")
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")
    
    def copy_command_output(self):
        """Copiar salida de comandos al portapapeles"""
        output_text = self.command_output.get(1.0, tk.END)
        if not output_text.strip():
            messagebox.showwarning("Advertencia", "No hay salida para copiar")
            return
        
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_text)
            self.log("✅ Salida copiada al portapapeles")
            messagebox.showinfo("Éxito", "Salida copiada al portapapeles")
        except Exception as e:
            self.log(f"❌ Error copiando: {e}")
            messagebox.showerror("Error", f"No se pudo copiar:\n{e}")
    
    def kill_logcat(self):
        """Matar proceso logcat si está ejecutándose"""
        def kill_thread():
            if platform.system() == "Windows":
                # En Windows, matar procesos adb que puedan estar ejecutando logcat
                self.run_command("taskkill /f /im adb.exe", timeout=5)
            else:
                # En Linux/Mac, matar procesos logcat
                self.run_command("pkill -f logcat", timeout=5)
            
            self.log("⚠️ Procesos logcat terminados")
            self.show_command_output("⚠️ Procesos logcat terminados\n")
        
        threading.Thread(target=kill_thread, daemon=True).start()
    
    def clear_command_output(self):
        """Limpiar área de salida de comandos"""
        self.command_output.delete(1.0, tk.END)
    
    def create_log_frame(self):
        """Crear frame de log"""
        log_frame = tk.LabelFrame(self.root, text="📊 Log del Sistema", 
                                 font=('Arial', 12, 'bold'), 
                                 fg='#ecf0f1', bg='#34495e', bd=2)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, 
                                                 bg='#1e1e1e', fg='#00ff00',
                                                 font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        log_btn_frame = tk.Frame(log_frame, bg='#34495e')
        log_btn_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Button(log_btn_frame, text="🧹 Limpiar Log", 
                 command=self.clear_log,
                 bg='#95a5a6', fg='white', font=('Arial', 9),
                 relief='flat').pack(side='left', padx=2)
        
        tk.Button(log_btn_frame, text="ℹ️ Acerca de", 
                 command=self.show_about,
                 bg='#95a5a6', fg='white', font=('Arial', 9),
                 relief='flat').pack(side='right', padx=2)
    
    def show_about(self):
        """Mostrar información de la aplicación"""
        about_text = f"""
🚀 {APP_TITLE} v{APP_VERSION}

👨‍💻 Desarrollado por: {DEVELOPER}
🏢 Empresa: {COMPANY}

📱 Gestor completo de ADB con:
• Conexión WiFi y USB
• Transferencia de archivos
• Instalación de APKs
• Consola de comandos personalizada
• Herramientas de diagnóstico

🔧 Características v{APP_VERSION}:
• Sin conexiones duplicadas
• Comandos ADB personalizados
• Interfaz mejorada
• Limpieza automática
        """
        
        messagebox.showinfo(f"Acerca de {APP_TITLE}", about_text)
    
    def log(self, message):
        """Agregar mensaje al log"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Limpiar el log"""
        self.log_text.delete(1.0, tk.END)
    
    def run_command(self, command, timeout=30):
        """Ejecutar comando usando ADB incluido"""
        try:
            # Si el comando empieza con 'adb', usar el ADB incluido
            if command.startswith('adb'):
                adb_path = get_adb_path()
                # Reemplazar 'adb' con la ruta completa
                command = command.replace('adb', f'"{adb_path}"', 1)
                self.log(f"🔧 Usando ADB: {adb_path}")
            
            result = subprocess.run(command, shell=True, capture_output=True, 
                                  text=True, timeout=timeout)
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Timeout"
        except Exception as e:
            return -1, "", str(e)
    
    def check_adb(self):
        """Verificar ADB"""
        adb_path = get_adb_path()
        self.log(f"🔍 Buscando ADB en: {adb_path}")
        
        code, stdout, stderr = self.run_command("adb version")
        if code == 0:
            version_info = stdout.split('\n')[0] if stdout else "Versión desconocida"
            self.log(f"✅ ADB disponible: {version_info}")
            self.log(f"📁 Ruta ADB: {adb_path}")
            self.show_current_devices()
        else:
            self.log("❌ ADB no encontrado")
            self.log(f"🔍 Buscando en ubicaciones alternativas...")
            
            # Intentar encontrar ADB en otras ubicaciones
            alternative_paths = [
                os.path.join(os.path.dirname(sys.executable), "adb.exe"),
                os.path.join(os.path.dirname(sys.executable), "adb_tools", "adb.exe"),
                "./adb.exe",
                "./adb_tools/adb.exe"
            ]
            
            for path in alternative_paths:
                if os.path.exists(path):
                    self.log(f"✅ ADB encontrado en: {path}")
                    return
            
            self.log("❌ Instala Android SDK Platform Tools o incluye adb.exe")
    
    def show_current_devices(self):
        """Mostrar dispositivos actuales"""
        code, stdout, stderr = self.run_command("adb devices")
        if code == 0:
            devices = []
            for line in stdout.split('\n'):
                if '\t' in line and 'device' in line:
                    device_id = line.split('\t')[0].strip()
                    devices.append(device_id)
            
            if devices:
                self.log(f"📱 Dispositivos detectados: {len(devices)}")
                for device in devices:
                    self.log(f"   - {device}")
            else:
                self.log("📱 No hay dispositivos conectados")
    
    def is_placeholder(self, value, placeholder):
        """Verificar si el valor es un placeholder"""
        return value == placeholder or value.strip() == ""
    
    def force_clean_all(self):
        """LIMPIEZA FORZADA - Elimina TODAS las conexiones"""
        self.log("🧹 LIMPIEZA FORZADA iniciada...")
        
        def clean_thread():
            # PASO 1: Matar servidor ADB completamente
            self.log("🔪 Matando servidor ADB...")
            for _ in range(3):  # Triple kill
                self.run_command("adb kill-server", timeout=10)
                time.sleep(1)
            
            # PASO 2: Matar procesos del sistema
            if platform.system() == "Windows":
                self.run_command("taskkill /f /im adb.exe", timeout=10)
            else:
                self.run_command("pkill -9 adb", timeout=10)
            
            time.sleep(3)
            
            # PASO 3: Reiniciar limpio
            self.log("🔄 Reiniciando ADB limpio...")
            code, stdout, stderr = self.run_command("adb start-server", timeout=15)
            
            if code == 0:
                self.log("✅ ADB reiniciado limpiamente")
                
                # PASO 4: Verificar limpieza
                time.sleep(2)
                self.show_current_devices()
                
                # Reset estado
                self.connected = False
                self.target_device = None
                self.root.after(0, self.update_ui_connection, False)
                
            else:
                self.log(f"❌ Error reiniciando ADB: {stderr}")
        
        threading.Thread(target=clean_thread, daemon=True).start()
    
    def pair_device(self):
        """Emparejar dispositivo"""
        ip = self.device_ip.get().strip()
        port = self.device_port.get().strip()
        code = self.pairing_code.get().strip()
        
        if not ip:
            messagebox.showerror("Error", "Introduce la IP del dispositivo")
            return
        
        if self.is_placeholder(port, "Puerto"):
            messagebox.showerror("Error", "Introduce el puerto de emparejamiento")
            return
            
        if self.is_placeholder(code, "Código"):
            messagebox.showerror("Error", "Introduce el código de emparejamiento")
            return
        
        self.log(f"🔗 Emparejando con {ip}:{port}...")
        
        def pair_thread():
            # Limpieza previa
            self.run_command("adb kill-server")
            time.sleep(2)
            self.run_command("adb start-server")
            time.sleep(2)
            
            # Intentar emparejamiento
            code_result, stdout, stderr = self.run_command(f"adb pair {ip}:{port} {code}")
            
            if code_result == 0 and "Successfully paired" in stdout:
                self.log("✅ Emparejamiento exitoso!")
                self.log("💡 Introduce el puerto de conexión (normalmente 5555) y conecta")
            elif "already paired" in stdout.lower():
                self.log("✅ Dispositivo ya emparejado")
                self.log("💡 Introduce el puerto de conexión y conecta")
            else:
                error_msg = stderr or stdout or "Error desconocido"
                self.log(f"❌ Error: {error_msg}")
        
        threading.Thread(target=pair_thread, daemon=True).start()
    
    def connect_clean(self):
        """Conectar de forma limpia (sin duplicados)"""
        ip = self.device_ip.get().strip()
        port = self.device_port.get().strip()
        
        if not ip or self.is_placeholder(port, "Puerto"):
            messagebox.showerror("Error", "Introduce IP y puerto válidos")
            return
        
        target = f"{ip}:{port}"
        self.log(f"🔗 Conectando a {target}...")
        
        def connect_thread():
            # PASO 1: Limpieza total antes de conectar
            self.log("🧹 Limpiando conexiones existentes...")
            
            # Desconectar TODO
            self.run_command("adb disconnect", timeout=10)
            time.sleep(1)
            
            # Verificar que no queda nada
            code, stdout, stderr = self.run_command("adb devices")
            if code == 0:
                existing = [line.split('\t')[0] for line in stdout.split('\n') 
                           if '\t' in line and 'device' in line]
                
                # Forzar desconexión de cada dispositivo individualmente
                for device in existing:
                    self.log(f"🔌 Forzando desconexión: {device}")
                    self.run_command(f"adb disconnect {device}")
                
                time.sleep(2)
            
            # PASO 2: Conectar SOLO el dispositivo objetivo
            self.log(f"🎯 Conectando únicamente a {target}...")
            code, stdout, stderr = self.run_command(f"adb connect {target}")
            
            if code == 0 and "connected" in stdout.lower():
                # PASO 3: Verificación final
                time.sleep(2)
                verify_code, verify_out, verify_err = self.run_command("adb devices")
                
                if verify_code == 0:
                    connected_devices = [line.split('\t')[0] for line in verify_out.split('\n') 
                                       if '\t' in line and 'device' in line]
                    
                    if len(connected_devices) == 1 and connected_devices[0] == target:
                        self.log("✅ Conexión única exitosa!")
                        self.target_device = target
                        self.connected = True
                        self.root.after(0, self.update_ui_connection, True)
                        self.root.after(0, lambda: self.device_info_label.config(text=f"Dispositivo: {target}"))
                    else:
                        self.log(f"⚠️ Múltiples dispositivos detectados: {len(connected_devices)}")
                        self.log("💡 Usa 'Limpiar Todo' y vuelve a intentar")
                        self.root.after(0, self.update_ui_connection, False)
                else:
                    self.log("❌ Error verificando conexión")
                    self.root.after(0, self.update_ui_connection, False)
            else:
                error = stderr or stdout or "Error desconocido"
                self.log(f"❌ Error conectando: {error}")
                self.root.after(0, self.update_ui_connection, False)
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def connect_usb(self):
        """Conectar dispositivo USB"""
        self.log("🔌 Buscando dispositivos USB...")
        
        def usb_thread():
            code, stdout, stderr = self.run_command("adb devices")
            
            if code == 0:
                usb_devices = []
                for line in stdout.split('\n'):
                    if '\t' in line and 'device' in line:
                        device_id = line.split('\t')[0].strip()
                        if ':' not in device_id:  # USB no tiene ':'
                            usb_devices.append(device_id)
                
                if usb_devices:
                    self.target_device = usb_devices[0]
                    self.connected = True
                    self.log(f"✅ USB conectado: {self.target_device}")
                    self.root.after(0, self.update_ui_connection, True)
                    self.root.after(0, lambda: self.device_info_label.config(text=f"Dispositivo USB: {self.target_device}"))
                else:
                    self.log("❌ No hay dispositivos USB")
                    self.root.after(0, self.update_ui_connection, False)
            else:
                self.log("❌ Error verificando USB")
        
        threading.Thread(target=usb_thread, daemon=True).start()
    
    def disconnect_clean(self):
        """Desconectar limpiamente"""
        self.log("🔌 Desconectando...")
        
        def disconnect_thread():
            if self.target_device:
                self.run_command(f"adb disconnect {self.target_device}")
            
            self.run_command("adb disconnect")  # Desconectar todo por si acaso
            
            self.connected = False
            self.target_device = None
            self.root.after(0, self.update_ui_connection, False)
            self.root.after(0, lambda: self.device_info_label.config(text="Dispositivo: Ninguno"))
            self.log("✅ Desconectado")
        
        threading.Thread(target=disconnect_thread, daemon=True).start()
    
    def update_ui_connection(self, connected):
        """Actualizar UI según conexión"""
        self.connected = connected
        
        if connected:
            self.status_label.config(text="● Conectado", fg='#27ae60')
            self.connect_btn.config(state='disabled')
            self.pair_btn.config(state='disabled')
            self.usb_btn.config(state='disabled')
            self.disconnect_btn.config(state='normal')
            
            if self.selected_file.get():
                self.push_btn.config(state='normal')
                if self.selected_file.get().endswith('.apk'):
                    self.install_btn.config(state='normal')
            
            self.pull_btn.config(state='normal')
        else:
            self.status_label.config(text="● Desconectado", fg='#e74c3c')
            self.connect_btn.config(state='normal')
            self.pair_btn.config(state='normal')
            self.usb_btn.config(state='normal')
            self.disconnect_btn.config(state='disabled')
            self.install_btn.config(state='disabled')
            self.push_btn.config(state='disabled')
            self.pull_btn.config(state='disabled')
    
    def show_adb_status(self):
        """Mostrar estado detallado de ADB"""
        def status_thread():
            code, stdout, stderr = self.run_command("adb devices -l")
            
            status_text = "📊 ESTADO ADB\n" + "="*30 + "\n\n"
            
            if code == 0:
                lines = stdout.strip().split('\n')[1:]  # Skip header
                if lines and any(line.strip() for line in lines):
                    status_text += f"Dispositivos encontrados: {len([l for l in lines if l.strip()])}\n\n"
                    
                    for line in lines:
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 2:
                                device_id = parts[0]
                                status = parts[1]
                                
                                status_text += f"📱 {device_id}\n"
                                status_text += f"   Estado: {status}\n"
                                status_text += f"   Tipo: {'USB' if ':' not in device_id else 'Red'}\n\n"
                else:
                    status_text += "❌ No hay dispositivos conectados\n"
            else:
                status_text += f"❌ Error: {stderr}\n"
            
            if self.target_device:
                status_text += f"\n🎯 Dispositivo activo: {self.target_device}\n"
            
            status_text += f"\n📱 App: {APP_TITLE} v{APP_VERSION}\n"
            status_text += f"👨‍💻 Por: {DEVELOPER}\n"
            
            messagebox.showinfo("Estado ADB", status_text)
        
        threading.Thread(target=status_thread, daemon=True).start()
    
    def select_file(self):
        """Seleccionar archivo"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[
                ("Archivos APK", "*.apk"),
                ("Documentos", "*.pdf;*.doc;*.docx;*.txt"),
                ("Imágenes", "*.jpg;*.jpeg;*.png;*.gif"),
                ("Videos", "*.mp4;*.avi;*.mkv"),
                ("Archivos ZIP", "*.zip;*.rar"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            self.selected_file.set(file_path)
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / (1024*1024)
            
            self.file_label.config(text=f"📄 {filename} ({file_size:.1f} MB)", fg='#ecf0f1')
            self.log(f"📁 Archivo seleccionado: {filename}")
            
            if self.connected:
                self.push_btn.config(state='normal')
                if file_path.endswith('.apk'):
                    self.install_btn.config(state='normal')
                else:
                    self.install_btn.config(state='disabled')
    
    def install_apk(self):
        """Instalar APK usando dispositivo específico"""
        if not self.connected or not self.target_device:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        apk_path = self.selected_file.get()
        if not apk_path.endswith('.apk'):
            messagebox.showerror("Error", "El archivo no es un APK")
            return
        
        self.install_btn.config(state='disabled')
        self.progress.start()
        
        def install_thread():
            filename = os.path.basename(apk_path)
            self.log(f"📦 Instalando {filename} en {self.target_device}...")
            
            # Comando específico para el dispositivo
            cmd = f'adb -s "{self.target_device}" install "{apk_path}"'
            code, stdout, stderr = self.run_command(cmd, timeout=120)
            
            self.root.after(0, self.progress.stop)
            
            if code == 0 and "Success" in stdout:
                self.log(f"✅ {filename} instalado exitosamente")
                messagebox.showinfo("Éxito", f"APK instalado: {filename}")
            else:
                error = stderr or stdout or "Error desconocido"
                self.log(f"❌ Error instalando: {error}")
                messagebox.showerror("Error", f"No se pudo instalar:\n{error}")
            
            if self.connected:
                self.root.after(0, lambda: self.install_btn.config(state='normal'))
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def push_file(self):
        """Enviar archivo usando dispositivo específico"""
        if not self.connected or not self.target_device:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        file_path = self.selected_file.get()
        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo")
            return
        
        dest_path = simpledialog.askstring("Destino", 
                                          "Ruta en el dispositivo:",
                                          initialvalue="/sdcard/Download/")
        
        if not dest_path:
            return
        
        self.push_btn.config(state='disabled')
        self.progress.start()
        
        def push_thread():
            filename = os.path.basename(file_path)
            full_dest = dest_path + filename if dest_path.endswith('/') else dest_path
            
            self.log(f"📤 Enviando {filename} a {self.target_device}...")
            
            # Comando específico para el dispositivo
            cmd = f'adb -s "{self.target_device}" push "{file_path}" "{full_dest}"'
            code, stdout, stderr = self.run_command(cmd, timeout=300)
            
            self.root.after(0, self.progress.stop)
            
            if code == 0:
                self.log(f"✅ {filename} enviado exitosamente")
                messagebox.showinfo("Éxito", f"Archivo enviado a:\n{full_dest}")
            else:
                error = stderr or stdout or "Error desconocido"
                self.log(f"❌ Error enviando: {error}")
                messagebox.showerror("Error", f"No se pudo enviar:\n{error}")
            
            if self.connected:
                self.root.after(0, lambda: self.push_btn.config(state='normal'))
        
        threading.Thread(target=push_thread, daemon=True).start()
    
    def pull_file(self):
        """Descargar archivo usando dispositivo específico"""
        if not self.connected or not self.target_device:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        remote_path = simpledialog.askstring("Archivo Remoto", 
                                            "Ruta del archivo en el dispositivo:",
                                            initialvalue="/sdcard/")
        
        if not remote_path:
            return
        
        save_path = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            initialvalue=os.path.basename(remote_path)
        )
        
        if not save_path:
            return
        
        self.pull_btn.config(state='disabled')
        self.progress.start()
        
        def pull_thread():
            self.log(f"📥 Descargando {remote_path} de {self.target_device}...")
            
            # Comando específico para el dispositivo
            cmd = f'adb -s "{self.target_device}" pull "{remote_path}" "{save_path}"'
            code, stdout, stderr = self.run_command(cmd, timeout=300)
            
            self.root.after(0, self.progress.stop)
            
            if code == 0:
                self.log(f"✅ Archivo descargado: {os.path.basename(save_path)}")
                messagebox.showinfo("Éxito", f"Archivo guardado en:\n{save_path}")
            else:
                error = stderr or stdout or "Error desconocido"
                self.log(f"❌ Error descargando: {error}")
                messagebox.showerror("Error", f"No se pudo descargar:\n{error}")
            
            if self.connected:
                self.root.after(0, lambda: self.pull_btn.config(state='normal'))
        
        threading.Thread(target=pull_thread, daemon=True).start()
    
    def device_info(self):
        """Mostrar información del dispositivo"""
        if not self.connected or not self.target_device:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        self.log("📱 Obteniendo información...")
        
        def info_thread():
            properties = [
                ("ro.product.model", "Modelo"),
                ("ro.product.manufacturer", "Fabricante"),
                ("ro.build.version.release", "Android"),
                ("ro.build.version.sdk", "API Level"),
                ("ro.product.brand", "Marca"),
            ]
            
            info_text = f"📱 Información de {self.target_device}:\n" + "="*35 + "\n"
            
            for prop, label in properties:
                cmd = f'adb -s "{self.target_device}" shell getprop {prop}'
                code, stdout, stderr = self.run_command(cmd)
                value = stdout.strip() if code == 0 and stdout.strip() else "N/A"
                info_text += f"{label}: {value}\n"
            
            self.log("✅ Información obtenida")
            messagebox.showinfo("Info Dispositivo", info_text)
        
        threading.Thread(target=info_thread, daemon=True).start()
    
    def list_apps(self):
        """Listar aplicaciones instaladas"""
        if not self.connected or not self.target_device:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        self.log("📋 Obteniendo aplicaciones...")
        
        def list_thread():
            cmd = f'adb -s "{self.target_device}" shell pm list packages -3'
            code, stdout, stderr = self.run_command(cmd)
            
            if code == 0:
                packages = [line.replace('package:', '') for line in stdout.split('\n') 
                           if line.startswith('package:')]
                
                packages.sort()
                apps_text = f"📱 Apps en {self.target_device} ({len(packages)}):\n" + "="*40 + "\n"
                apps_text += "\n".join(packages[:25])
                
                if len(packages) > 25:
                    apps_text += f"\n... y {len(packages) - 25} más"
                
                self.log(f"✅ {len(packages)} aplicaciones encontradas")
                messagebox.showinfo("Apps Instaladas", apps_text)
            else:
                self.log("❌ Error obteniendo aplicaciones")
        
        threading.Thread(target=list_thread, daemon=True).start()
    
    def screenshot(self):
        """Tomar captura de pantalla"""
        if not self.connected or not self.target_device:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        save_path = filedialog.asksaveasfilename(
            title="Guardar captura",
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )
        
        if not save_path:
            return
        
        self.log("📸 Tomando captura...")
        
        def screenshot_thread():
            temp_path = "/sdcard/temp_screenshot.png"
            
            # Tomar captura
            cmd1 = f'adb -s "{self.target_device}" shell screencap -p {temp_path}'
            code, stdout, stderr = self.run_command(cmd1)
            
            if code == 0:
                # Descargar
                cmd2 = f'adb -s "{self.target_device}" pull {temp_path} "{save_path}"'
                code, stdout, stderr = self.run_command(cmd2)
                
                if code == 0:
                    # Limpiar
                    cmd3 = f'adb -s "{self.target_device}" shell rm {temp_path}'
                    self.run_command(cmd3)
                    
                    self.log("✅ Captura guardada")
                    messagebox.showinfo("Éxito", f"Captura guardada en:\n{save_path}")
                else:
                    self.log("❌ Error descargando captura")
            else:
                self.log("❌ Error tomando captura")
        
        threading.Thread(target=screenshot_thread, daemon=True).start()
    
    def restart_adb(self):
        """Reiniciar ADB"""
        self.log("🔄 Reiniciando ADB...")
        
        def restart_thread():
            self.run_command("adb kill-server")
            time.sleep(2)
            code, stdout, stderr = self.run_command("adb start-server")
            
            if code == 0:
                self.log("✅ ADB reiniciado")
                self.show_current_devices()
            else:
                self.log("❌ Error reiniciando ADB")
        
        threading.Thread(target=restart_thread, daemon=True).start()
    
    def scan_network(self):
        """Escanear red buscando dispositivos"""
        if not self.device_ip.get().strip():
            messagebox.showwarning("Advertencia", "Introduce una IP base para escanear")
            return
        
        ip_base = ".".join(self.device_ip.get().split('.')[:-1]) + "."
        self.log(f"🔍 Escaneando red {ip_base}0/24...")
        
        def scan_thread():
            found_devices = []
            adb_ports = []
            
            for i in range(1, 255):
                ip = f"{ip_base}{i}"
                try:
                    # Ping rápido
                    ping_cmd = f"ping -c 1 -W 1 {ip}" if platform.system() != "Windows" else f"ping -n 1 -w 1000 {ip}"
                    code, stdout, stderr = self.run_command(ping_cmd, timeout=2)
                    
                    if code == 0:
                        found_devices.append(ip)
                        self.log(f"📱 Encontrado: {ip}")
                        
                        # Verificar puerto 5555 (ADB)
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(1)
                            if sock.connect_ex((ip, 5555)) == 0:
                                adb_ports.append(f"{ip}:5555")
                                self.log(f"🎯 ADB disponible: {ip}:5555")
                                
                                # Auto-rellenar si es el primero
                                if not adb_ports[:-1]:  # Si es el primero
                                    self.device_ip.set(ip)
                                    self.device_port.set("5555")
                                    self.port_entry.config(fg='black')
                            sock.close()
                        except:
                            pass
                except:
                    continue
                
                # Mostrar progreso cada 50 IPs
                if i % 50 == 0:
                    self.log(f"🔍 Progreso: {i}/254...")
            
            self.log(f"✅ Escaneo completado:")
            self.log(f"   📱 {len(found_devices)} dispositivos activos")
            self.log(f"   🎯 {len(adb_ports)} con ADB disponible")
            
            if adb_ports:
                self.log("💡 Dispositivos ADB encontrados:")
                for device in adb_ports:
                    self.log(f"   🔗 {device}")
        
        threading.Thread(target=scan_thread, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ADBFileManagerFixed(root)
    root.mainloop()