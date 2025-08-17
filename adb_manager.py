import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import subprocess
import threading
import os
import time
import socket
import platform

class ADBFileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB File Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.connected = False
        self.device_ip = tk.StringVar(value="192.168.1.80")
        self.device_port = tk.StringVar()
        self.pairing_code = tk.StringVar()
        self.selected_file = tk.StringVar()
        
        self.setup_ui()
        self.check_adb()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Título
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(title_frame, text="📱 ADB File Manager", 
                font=('Arial', 18, 'bold'), fg='#ecf0f1', bg='#2c3e50').pack()
        
        # Frame de conexión
        self.create_connection_frame()
        
        # Frame de archivos
        self.create_file_frame()
        
        # Frame de herramientas
        self.create_tools_frame()
        
        # Log
        self.create_log_frame()
        
        self.log("🚀 ADB File Manager iniciado")
        self.log("💡 IP detectada: 192.168.1.80")
        self.log("🔧 Para emparejar: Ve al dispositivo → Configuración → Depuración WiFi")
        self.log("📱 Introduce el puerto y código que aparecen en pantalla")
    
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
        
        # Agregar placeholders (solo para puerto y código, IP ya tiene valor por defecto)
        self.add_placeholder(self.port_entry, self.device_port, "Puerto")
        self.add_placeholder(self.code_entry, self.pairing_code, "Código")
        
        # Botones de conexión
        btn_frame = tk.Frame(conn_frame, bg='#34495e')
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.connect_btn = tk.Button(btn_frame, text="🔗 Conectar", 
                                    command=self.connect_tcpip,
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
                                       command=self.disconnect,
                                       bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                                       relief='flat', padx=15, state='disabled')
        self.disconnect_btn.pack(side='left', padx=5)
        
        self.status_label = tk.Label(btn_frame, text="● Desconectado", 
                                    fg='#e74c3c', bg='#34495e', font=('Arial', 10, 'bold'))
        self.status_label.pack(side='right', padx=10)
    
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
        
        tk.Button(btn_frame, text="🧹 Limpiar ADB", 
                 command=self.clean_adb,
                 bg='#34495e', fg='white', font=('Arial', 9, 'bold'),
                 relief='flat', padx=10).pack(side='left', padx=2)
    
    def create_log_frame(self):
        """Crear frame de log"""
        log_frame = tk.LabelFrame(self.root, text="📊 Log", 
                                 font=('Arial', 12, 'bold'), 
                                 fg='#ecf0f1', bg='#34495e', bd=2)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, 
                                                 bg='#1e1e1e', fg='#00ff00',
                                                 font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Button(log_frame, text="🧹 Limpiar", 
                 command=self.clear_log,
                 bg='#95a5a6', fg='white', font=('Arial', 9),
                 relief='flat').pack(pady=2)
    
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
        """Ejecutar comando"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, 
                                  text=True, timeout=timeout)
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Timeout"
        except Exception as e:
            return -1, "", str(e)
    
    def check_adb(self):
        """Verificar ADB"""
        code, stdout, stderr = self.run_command("adb version")
        if code == 0:
            self.log("✅ ADB disponible")
        else:
            self.log("❌ ADB no encontrado - Instala Android SDK Platform Tools")
    
    def is_placeholder(self, value, placeholder):
        """Verificar si el valor es un placeholder"""
        return value == placeholder or value.strip() == ""
    
    def pair_device(self):
        """Emparejar dispositivo con código"""
        ip = self.device_ip.get().strip()
        port = self.device_port.get().strip()
        code = self.pairing_code.get().strip()
        
        # Verificar placeholders
        if not ip or ip.strip() == "":
            messagebox.showerror("Error", "Introduce la IP del dispositivo")
            return
        
        if self.is_placeholder(port, "Puerto"):
            messagebox.showerror("Error", "Introduce el puerto de emparejamiento")
            return
            
        if self.is_placeholder(code, "Código"):
            messagebox.showerror("Error", "Introduce el código de emparejamiento")
            return
        
        self.log(f"🔗 Emparejando con {ip}:{port} usando código {code}...")
        self.pair_btn.config(state='disabled')
        self.connect_btn.config(state='disabled')
        
        def pair_thread():
            # Limpiar conexiones ADB
            self.run_command("adb kill-server")
            time.sleep(1)
            self.run_command("adb start-server")
            time.sleep(1)
            
            # Intentar emparejamiento
            code_result, stdout, stderr = self.run_command(f"adb pair {ip}:{port} {code}")
            
            if code_result == 0 and "Successfully paired" in stdout:
                self.log("✅ Emparejamiento exitoso!")
                self.log("💡 Ahora introduce manualmente el puerto de conexión y usa 'Conectar'")
                    
            elif "already paired" in stdout.lower():
                self.log("✅ Dispositivo ya emparejado")
                self.log("💡 Introduce el puerto de conexión y usa 'Conectar'")
                
            else:
                error_msg = stderr or stdout or "Error desconocido"
                self.log(f"❌ Error en emparejamiento: {error_msg}")
                self.log("💡 VERIFICA EN EL DISPOSITIVO:")
                self.log("   1. Ve a Configuración → Sistema → Opciones desarrollador")
                self.log("   2. Activa 'Depuración ADB por WiFi'")
                self.log("   3. Aparecerá IP:PUERTO y CÓDIGO")
                self.log("   4. Usa esos datos exactos aquí")
            
            self.root.after(0, lambda: [
                self.pair_btn.config(state='normal'),
                self.connect_btn.config(state='normal')
            ])
        
        threading.Thread(target=pair_thread, daemon=True).start()
    
    def connect_tcpip(self):
        """Conectar por TCP/IP"""
        ip = self.device_ip.get().strip()
        port = self.device_port.get().strip()
        
        # Verificar placeholders
        if not ip or ip.strip() == "" or self.is_placeholder(port, "Puerto"):
            messagebox.showerror("Error", "Introduce IP y puerto válidos")
            return
        
        self.log(f"🔗 Conectando a {ip}:{port}...")
        
        def connect_thread():
            # Limpiar conexiones duplicadas antes de conectar
            self.clean_duplicate_connections(f"{ip}:{port}")
            
            code, stdout, stderr = self.run_command(f"adb connect {ip}:{port}")
            
            if code == 0 and ("connected" in stdout.lower() or "already connected" in stdout.lower()):
                # Verificar que solo hay un dispositivo conectado
                time.sleep(1)
                self.ensure_single_device(f"{ip}:{port}")
                
                self.connected = True
                self.log(f"✅ Conectado a {ip}:{port}")
                self.root.after(0, self.update_ui_connection, True)
            else:
                error = stderr or stdout or "Error desconocido"
                self.log(f"❌ Error: {error}")
                self.root.after(0, self.update_ui_connection, False)
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def clean_duplicate_connections(self, target_device):
        """Limpiar conexiones ADB duplicadas manteniendo solo el dispositivo objetivo"""
        self.log("🧹 Limpiando conexiones duplicadas...")
        
        code, stdout, stderr = self.run_command("adb devices")
        if code == 0:
            for line in stdout.split('\n'):
                if ':' in line and 'device' in line:
                    device = line.split()[0]
                    if device != target_device:
                        self.log(f"🔌 Desconectando {device}")
                        self.run_command(f"adb disconnect {device}")
    
    def ensure_single_device(self, target_device):
        """Asegurar que solo hay un dispositivo conectado"""
        code, stdout, stderr = self.run_command("adb devices")
        if code == 0:
            devices = [line.split()[0] for line in stdout.split('\n') 
                      if ':' in line and 'device' in line]
            
            if len(devices) > 1:
                self.log(f"⚠️ Múltiples dispositivos detectados ({len(devices)})")
                self.log("🧹 Limpiando automáticamente...")
                
                for device in devices:
                    if device != target_device:
                        self.log(f"🔌 Desconectando {device}")
                        self.run_command(f"adb disconnect {device}")
                        
                self.log(f"✅ Solo queda conectado: {target_device}")
            else:
                self.log("✅ Dispositivo único verificado")
    
    def clean_adb(self):
        """Limpiar todas las conexiones ADB completamente"""
        self.log("🧹 Limpieza completa de ADB iniciada...")
        
        def clean_thread():
            # Guardar dispositivo actual
            current_ip = self.device_ip.get().strip()
            current_port = self.device_port.get().strip()
            current_device = f"{current_ip}:{current_port}" if current_ip and not self.is_placeholder(current_port, "Puerto") else None
            
            # PASO 1: Matar servidor ADB completamente
            self.log("🔪 Deteniendo servidor ADB...")
            self.run_command("adb kill-server")
            time.sleep(3)
            
            # PASO 2: Limpiar procesos ADB residuales (Windows/Linux)
            if platform.system() == "Windows":
                self.run_command("taskkill /f /im adb.exe", timeout=5)
            else:
                self.run_command("pkill -f adb", timeout=5)
            
            time.sleep(2)
            
            # PASO 3: Reiniciar servidor ADB
            self.log("🔄 Iniciando servidor ADB limpio...")
            start_code, start_out, start_err = self.run_command("adb start-server")
            
            if start_code != 0:
                self.log(f"❌ Error iniciando ADB: {start_err}")
                return
            
            time.sleep(2)
            
            # PASO 4: Verificar que no hay dispositivos
            code, stdout, stderr = self.run_command("adb devices")
            devices = [line.split()[0] for line in stdout.split('\n') 
                      if ':' in line and 'device' in line]
            
            if devices:
                self.log(f"🔌 Desconectando {len(devices)} dispositivos residuales...")
                for device in devices:
                    self.run_command(f"adb disconnect {device}")
                time.sleep(1)
            
            self.log("✅ Limpieza ADB completada")
            
            # PASO 5: Reconectar dispositivo si estaba conectado
            if current_device and self.connected:
                self.log(f"🔗 Reconectando a {current_device}...")
                
                # Esperar un poco más para asegurar limpieza
                time.sleep(3)
                
                connect_code, connect_out, connect_err = self.run_command(f"adb connect {current_device}")
                
                if connect_code == 0 and ("connected" in connect_out.lower() or "already connected" in connect_out.lower()):
                    # Verificar conexión única
                    time.sleep(2)
                    verify_code, verify_out, verify_err = self.run_command("adb devices")
                    device_count = len([line for line in verify_out.split('\n') 
                                      if ':' in line and 'device' in line])
                    
                    if device_count == 1:
                        self.log(f"✅ Reconectado limpiamente a {current_device}")
                        self.log("🎉 ADB listo para transferencias sin conflictos")
                        self.root.after(0, self.update_ui_connection, True)
                    else:
                        self.log(f"⚠️ Conectado pero con {device_count} dispositivos")
                        self.root.after(0, self.update_ui_connection, True)
                else:
                    self.log(f"❌ Error en reconexión: {connect_err or connect_out}")
                    self.connected = False
                    self.root.after(0, self.update_ui_connection, False)
            else:
                self.connected = False
                self.root.after(0, self.update_ui_connection, False)
                self.log("🔌 Limpieza completada - Listo para nueva conexión")
        
        threading.Thread(target=clean_thread, daemon=True).start()
    
    def connect_usb(self):
        """Conectar dispositivo USB"""
        self.log("🔌 Verificando dispositivos USB...")
        
        def usb_thread():
            code, stdout, stderr = self.run_command("adb devices")
            
            if code == 0:
                devices = [line for line in stdout.split('\n') 
                          if line.strip() and not line.startswith('List of') and 'device' in line]
                
                if devices:
                    self.connected = True
                    self.log(f"✅ Dispositivo USB conectado: {devices[0].split()[0]}")
                    self.root.after(0, self.update_ui_connection, True)
                else:
                    self.log("❌ No hay dispositivos USB conectados")
                    self.root.after(0, self.update_ui_connection, False)
            else:
                self.log("❌ Error verificando dispositivos")
                self.root.after(0, self.update_ui_connection, False)
        
        threading.Thread(target=usb_thread, daemon=True).start()
    
    def disconnect(self):
        """Desconectar dispositivo"""
        ip = self.device_ip.get().strip()
        port = self.device_port.get().strip()
        
        # Verificar placeholders
        if ip and ip.strip() != "" and not self.is_placeholder(port, "Puerto"):
            self.run_command(f"adb disconnect {ip}:{port}")
        
        self.connected = False
        self.update_ui_connection(False)
        self.log("🔌 Desconectado")
    
    def update_ui_connection(self, connected):
        """Actualizar UI según estado de conexión"""
        self.connected = connected
        
        if connected:
            self.status_label.config(text="● Conectado", fg='#27ae60')
            self.connect_btn.config(state='disabled')
            self.pair_btn.config(state='disabled')
            self.usb_btn.config(state='disabled')
            self.disconnect_btn.config(state='normal')
            
            # Habilitar botones de archivo si hay archivo seleccionado
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
            file_size = os.path.getsize(file_path) / (1024*1024)  # MB
            
            self.file_label.config(text=f"📄 {filename} ({file_size:.1f} MB)", fg='#ecf0f1')
            self.log(f"📁 Archivo seleccionado: {filename}")
            
            if self.connected:
                self.push_btn.config(state='normal')
                if file_path.endswith('.apk'):
                    self.install_btn.config(state='normal')
                else:
                    self.install_btn.config(state='disabled')
    
    def install_apk(self):
        """Instalar APK"""
        if not self.connected:
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
            self.log(f"📦 Instalando {filename}...")
            
            # SOLUCIÓN ROBUSTA: Reiniciar ADB antes de instalar
            ip = self.device_ip.get().strip()
            port = self.device_port.get().strip()
            target_device = f"{ip}:{port}"
            
            self.log("🔄 Preparando ADB para instalación...")
            self.run_command("adb kill-server")
            time.sleep(2)
            self.run_command("adb start-server")
            time.sleep(2)
            
            # Reconectar solo nuestro dispositivo
            connect_code, connect_out, connect_err = self.run_command(f"adb connect {target_device}")
            
            if connect_code != 0 or "connected" not in connect_out.lower():
                self.log(f"❌ Error reconectando: {connect_err or connect_out}")
                self.root.after(0, self.progress.stop)
                self.root.after(0, lambda: self.install_btn.config(state='normal'))
                return
            
            time.sleep(1)
            
            # Intentar instalación
            code, stdout, stderr = self.run_command(f'adb -s "{target_device}" install "{apk_path}"', timeout=120)
            
            # Si falla, intentar sin especificar dispositivo
            if code != 0 and "more than one device" in (stderr or "").lower():
                self.log("🔄 Reintentando instalación...")
                code, stdout, stderr = self.run_command(f'adb install "{apk_path}"', timeout=120)
            
            self.root.after(0, self.progress.stop)
            
            if code == 0 and "Success" in stdout:
                self.log(f"✅ {filename} instalado exitosamente")
                messagebox.showinfo("Éxito", f"APK instalado: {filename}")
            else:
                error = stderr or stdout or "Error desconocido"
                self.log(f"❌ Error instalando: {error}")
                
                if "more than one device" in error.lower():
                    self.log("💡 SOLUCIÓN MANUAL:")
                    self.log("   1. Usa '🧹 Limpiar ADB'")
                    self.log("   2. Reinicia el dispositivo")
                    self.log("   3. Vuelve a emparejar")
                
                messagebox.showerror("Error", f"No se pudo instalar:\n{error}")
            
            if self.connected:
                self.root.after(0, lambda: self.install_btn.config(state='normal'))
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def push_file(self):
        """Enviar archivo al dispositivo"""
        if not self.connected:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        file_path = self.selected_file.get()
        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo")
            return
        
        # Preguntar ruta de destino
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
            
            self.log(f"📤 Enviando {filename} a {full_dest}...")
            
            # SOLUCIÓN ROBUSTA: Reiniciar ADB completamente antes de enviar
            ip = self.device_ip.get().strip()
            port = self.device_port.get().strip()
            target_device = f"{ip}:{port}"
            
            self.log("🔄 Reiniciando ADB para evitar conflictos...")
            self.run_command("adb kill-server")
            time.sleep(2)
            self.run_command("adb start-server")
            time.sleep(2)
            
            # Conectar SOLO nuestro dispositivo
            self.log(f"🔗 Conectando únicamente a {target_device}...")
            connect_code, connect_out, connect_err = self.run_command(f"adb connect {target_device}")
            
            if connect_code != 0 or "connected" not in connect_out.lower():
                self.log(f"❌ Error reconectando: {connect_err or connect_out}")
                self.root.after(0, self.progress.stop)
                self.root.after(0, lambda: self.push_btn.config(state='normal'))
                return
            
            # Verificar que solo hay UN dispositivo
            time.sleep(1)
            verify_code, verify_out, verify_err = self.run_command("adb devices")
            device_count = len([line for line in verify_out.split('\n') 
                              if ':' in line and 'device' in line])
            
            self.log(f"📱 Dispositivos conectados: {device_count}")
            
            if device_count != 1:
                self.log(f"⚠️ Detectados {device_count} dispositivos - Forzando limpieza...")
                # Desconectar todo y reconectar solo el nuestro
                self.run_command("adb disconnect")
                time.sleep(1)
                self.run_command(f"adb connect {target_device}")
                time.sleep(2)
            
            # Enviar archivo con dispositivo específico
            code, stdout, stderr = self.run_command(f'adb -s "{target_device}" push "{file_path}" "{full_dest}"', timeout=300)
            
            # Si aún falla, intentar sin especificar dispositivo (solo debería haber uno)
            if code != 0 and "more than one device" in (stderr or "").lower():
                self.log("🔄 Reintentando con comando simple...")
                code, stdout, stderr = self.run_command(f'adb push "{file_path}" "{full_dest}"', timeout=300)
            
            self.root.after(0, self.progress.stop)
            
            if code == 0:
                self.log(f"✅ {filename} enviado exitosamente")
                messagebox.showinfo("Éxito", f"Archivo enviado a:\n{full_dest}")
            else:
                error = stderr or stdout or "Error desconocido"
                self.log(f"❌ Error enviando: {error}")
                
                if "more than one device" in error.lower():
                    self.log("💡 SOLUCIÓN MANUAL:")
                    self.log("   1. Usa '🧹 Limpiar ADB'")
                    self.log("   2. Desactiva y reactiva WiFi en el dispositivo") 
                    self.log("   3. Vuelve a emparejar desde cero")
                
                messagebox.showerror("Error", f"No se pudo enviar:\n{error}")
            
            if self.connected:
                self.root.after(0, lambda: self.push_btn.config(state='normal'))
        
        threading.Thread(target=push_thread, daemon=True).start()
    
    def pull_file(self):
        """Descargar archivo del dispositivo"""
        if not self.connected:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        # Preguntar ruta del archivo en el dispositivo
        remote_path = simpledialog.askstring("Archivo Remoto", 
                                            "Ruta del archivo en el dispositivo:",
                                            initialvalue="/sdcard/")
        
        if not remote_path:
            return
        
        # Seleccionar donde guardar
        save_path = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            initialvalue=os.path.basename(remote_path)
        )
        
        if not save_path:
            return
        
        self.pull_btn.config(state='disabled')
        self.progress.start()
        
        def pull_thread():
            self.log(f"📥 Descargando {remote_path}...")
            
            code, stdout, stderr = self.run_command(f'adb pull "{remote_path}" "{save_path}"', timeout=300)
            
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
        if not self.connected:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        self.log("📱 Obteniendo información...")
        
        def info_thread():
            properties = [
                ("ro.product.model", "Modelo"),
                ("ro.product.manufacturer", "Fabricante"),
                ("ro.build.version.release", "Android"),
                ("ro.build.version.sdk", "API Level"),
            ]
            
            info_text = "📱 Información del Dispositivo:\n" + "="*30 + "\n"
            
            for prop, label in properties:
                code, stdout, stderr = self.run_command(f"adb shell getprop {prop}")
                value = stdout.strip() if code == 0 and stdout.strip() else "N/A"
                info_text += f"{label}: {value}\n"
            
            self.log("✅ Información obtenida")
            messagebox.showinfo("Info Dispositivo", info_text)
        
        threading.Thread(target=info_thread, daemon=True).start()
    
    def list_apps(self):
        """Listar aplicaciones instaladas"""
        if not self.connected:
            messagebox.showerror("Error", "Dispositivo no conectado")
            return
        
        self.log("📋 Obteniendo aplicaciones...")
        
        def list_thread():
            code, stdout, stderr = self.run_command("adb shell pm list packages -3")
            
            if code == 0:
                packages = [line.replace('package:', '') for line in stdout.split('\n') 
                           if line.startswith('package:')]
                
                packages.sort()
                apps_text = f"📱 Apps Instaladas ({len(packages)}):\n" + "="*30 + "\n"
                apps_text += "\n".join(packages[:20])  # Mostrar solo las primeras 20
                
                if len(packages) > 20:
                    apps_text += f"\n... y {len(packages) - 20} más"
                
                self.log(f"✅ {len(packages)} aplicaciones encontradas")
                messagebox.showinfo("Apps Instaladas", apps_text)
            else:
                self.log("❌ Error obteniendo aplicaciones")
        
        threading.Thread(target=list_thread, daemon=True).start()
    
    def screenshot(self):
        """Tomar captura de pantalla"""
        if not self.connected:
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
            # Tomar captura
            code, stdout, stderr = self.run_command("adb shell screencap -p /sdcard/temp_screenshot.png")
            
            if code == 0:
                # Descargar
                code, stdout, stderr = self.run_command(f'adb pull /sdcard/temp_screenshot.png "{save_path}"')
                
                if code == 0:
                    # Limpiar
                    self.run_command("adb shell rm /sdcard/temp_screenshot.png")
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
            time.sleep(1)
            code, stdout, stderr = self.run_command("adb start-server")
            
            if code == 0:
                self.log("✅ ADB reiniciado")
            else:
                self.log("❌ Error reiniciando ADB")
        
        threading.Thread(target=restart_thread, daemon=True).start()
    
    def scan_network(self):
        """Escanear red buscando dispositivos"""
        if not self.device_ip.get() or self.device_ip.get().strip() == "":
            messagebox.showwarning("Advertencia", "Introduce una IP base para escanear")
            return
        
        ip_base = ".".join(self.device_ip.get().split('.')[:-1]) + "."
        self.log(f"🔍 Escaneando red {ip_base}0/24...")
        
        def scan_thread():
            found = []
            for i in range(1, 255):
                ip = f"{ip_base}{i}"
                try:
                    ping_cmd = f"ping -c 1 -W 1 {ip}" if platform.system() != "Windows" else f"ping -n 1 -w 1000 {ip}"
                    code, stdout, stderr = self.run_command(ping_cmd, timeout=2)
                    
                    if code == 0:
                        found.append(ip)
                        self.log(f"📱 Dispositivo: {ip}")
                        
                        # Probar puerto 5555
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(1)
                            if sock.connect_ex((ip, 5555)) == 0:
                                self.log(f"🎯 Puerto 5555 abierto: {ip}")
                                self.device_ip.set(ip)
                                self.device_port.set("5555")
                                self.port_entry.config(fg='black')
                            sock.close()
                        except:
                            pass
                except:
                    continue
            
            self.log(f"✅ Escaneo completado. {len(found)} dispositivos encontrados")
        
        threading.Thread(target=scan_thread, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ADBFileManager(root)
    root.mainloop()