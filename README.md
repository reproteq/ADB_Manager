# 📱 ADB Manager v1.2

Una aplicación GUI moderna y profesional para gestionar dispositivos Android mediante ADB (Android Debug Bridge). Incluye consola de comandos personalizada, gestión avanzada de archivos y herramientas integradas para desarrollo Android.

🎥 **[Ver Video Tutorial en YouTube](https://youtu.be/hvMkiT95O5E)**

## ✨ Características Principales

### 🔗 Conexión Avanzada
- **Emparejamiento WiFi** - Conecta dispositivos usando códigos de emparejamiento
- **Conexión USB** - Soporte completo para dispositivos por cable
- **Limpieza automática** - Elimina conexiones duplicadas automáticamente
- **Detección inteligente** - Escaneo de red para encontrar dispositivos ADB

### 💻 Consola ADB Integrada
- **Comandos personalizados** - Ejecuta cualquier comando ADB
- **21+ comandos rápidos** organizados por categorías
- **Salida en tiempo real** - Ve los resultados inmediatamente
- **Historial y gestión** - Guarda, copia y limpia resultados

### 📁 Gestión de Archivos
- **Transferencia universal** - Envía cualquier tipo de archivo
- **Instalación de APKs** - Instalación robusta con verificación
- **Descarga de archivos** - Descarga desde cualquier ruta del dispositivo
- **Progreso visual** - Barras de estado y feedback en tiempo real

### 🛠️ Herramientas Integradas
- **Información del dispositivo** - Especificaciones completas
- **Gestión de aplicaciones** - Lista e información de apps instaladas
- **Capturas de pantalla** - Screenshots directos del dispositivo
- **Diagnósticos** - Estado detallado de ADB y conexiones

## 🖥️ Interfaz

### Pantalla Principal v1.2
![Pantalla Principal](https://github.com/reproteq/ADB_Manager/blob/main/screenshots/main_v12.png?raw=true)

La nueva interfaz incluye:
- **Consola ADB integrada** con comandos rápidos
- **Área de salida expandida** para mejor visibilidad
- **Interfaz más amplia** (1000x850) para mayor comodidad
- **21+ botones de comandos** organizados en 4 filas

### Consola de Comandos ADB
![Consola ADB](https://github.com/reproteq/ADB_Manager/blob/main/screenshots/console_v12.png?raw=true)

#### Comandos Rápidos Disponibles:

**📱 Básicos:**
- `devices` - Ver dispositivos conectados
- `info` - Información del dispositivo
- `reboot` - Reiniciar dispositivo
- `shell` - Acceso al shell
- `logcat` - Ver logs del sistema

**📁 Archivos:**
- `/sdcard` - Listar archivos en almacenamiento
- `Download` - Ver carpeta de descargas
- `storage` - Espacio disponible
- `packages` - Apps instaladas

**🔧 Sistema:**
- `processes` - Procesos en ejecución
- `meminfo` - Información de memoria
- `volume` - Control de volumen
- `brightness` - Brillo de pantalla
- `wifi` - Información WiFi

**⚙️ Avanzado:**
- `uninstall` - Desinstalar aplicación
- `recovery` - Reiniciar en recovery
- `airplane` - Estado modo avión
- `data` - Datos móviles

## 🚀 Instalación

### Opción 1: Ejecutable Portable (Recomendado)
1. **Descarga** el ejecutable desde [Releases](https://github.com/reproteq/ADB_Manager/releases)
2. **Ejecuta** `ADB_Manager_v1.2_Portable.exe`
3. **¡Listo!** - No necesita instalación de ADB

### Opción 2: Desde Código Fuente
```bash
# Clona el repositorio
git clone https://github.com/reproteq/ADB_Manager.git
cd ADB_Manager

# Instala dependencias
pip install -r requirements.txt

# Ejecuta la aplicación
python adb_manager.py
```

### Requisitos para Código Fuente
- **Python 3.7+**
- **tkinter** (incluido en Python)
- **Android SDK Platform Tools** (para ADB)

## 📦 Compilación Portable

Para crear tu propio ejecutable portable:

### 1. Organiza los archivos:
```
📁 Proyecto/
├── 📄 adb_manager.py
├── 🖼️ icon.ico
└── 📁 adb_tools/
    ├── adb.exe
    ├── AdbWinApi.dll
    ├── AdbWinUsbApi.dll
    ├── fastboot.exe
    └── [archivos ADB...]
```

### 2. Compila con PyInstaller:
```bash
# Instala PyInstaller
pip install pyinstaller

# Compila con herramientas incluidas
pyinstaller --onefile --windowed --icon=icon.ico --name="ADB_Manager_v1.2_Portable" --add-data "adb_tools;adb_tools" adb_manager.py
```

### 3. Resultado:
- **Ejecutable único** con todas las herramientas incluidas
- **Sin dependencias** - funciona en cualquier Windows
- **Completamente portable** - no requiere instalación

## 📱 Configuración del Dispositivo

### Para Android / Wear OS

1. **Habilita Opciones de Desarrollador**:
   ```
   Configuración → Sistema → Acerca de
   Toca 7 veces en "Número de compilación"
   ```

2. **Activa Depuración ADB por WiFi**:
   ```
   Configuración → Sistema → Opciones desarrollador
   Activa "Depuración ADB por WiFi"
   ```

3. **Anota los datos mostrados**:
   - **IP del dispositivo** (ej: 192.168.1.100)
   - **Puerto de emparejamiento** (ej: 37851)
   - **Código de 6 dígitos** (ej: 123456)
   - **Puerto de conexión** (normalmente 5555)

## 🔧 Guía de Uso

### 🔗 Conexión WiFi
1. **Configura** los datos de emparejamiento:
   - IP: `192.168.1.100`
   - Puerto: `37851` (puerto de emparejamiento)
   - Código: `123456`

2. **Empareja** haciendo clic en "🔗 Emparejar"

3. **Cambia** al puerto de conexión:
   - Puerto: `5555` (puerto de conexión)

4. **Conecta** haciendo clic en "🔗 Conectar"

### 💻 Uso de la Consola
1. **Escribe comandos** directamente o usa botones rápidos
2. **Presiona Enter** o clic en "▶️ Ejecutar"
3. **Ve los resultados** en el área de salida
4. **Guarda o copia** resultados según necesites

### 📦 Instalación de APKs
1. **Conecta** tu dispositivo
2. **Selecciona** el archivo APK
3. **Haz clic** en "📦 Instalar APK"
4. **Espera** la confirmación de instalación

### 📁 Transferencia de Archivos
1. **Selecciona** cualquier archivo
2. **Clic** en "📤 Enviar Archivo"
3. **Especifica** la ruta de destino
4. **Confirma** la transferencia

## 🆕 Novedades v1.2

### ✨ Características Nuevas
- **💻 Consola ADB integrada** con 21+ comandos rápidos
- **🖥️ Interfaz expandida** a 1000x850 píxeles
- **📊 Área de logs mejorada** con mayor visibilidad
- **💾 Guardar y copiar** resultados de comandos
- **🔧 Variables globales** centralizadas para fácil mantenimiento
- **⚠️ Kill Logcat** para terminar procesos colgados

### 🔧 Mejoras Técnicas
- **🎯 Detección automática** de herramientas ADB incluidas
- **📁 Gestión de rutas** mejorada para ejecutables portables
- **🔍 Búsqueda inteligente** de ADB en múltiples ubicaciones
- **🧹 Limpieza más robusta** de conexiones duplicadas

### 🎨 Mejoras de Interfaz
- **Botones más compactos** y organizados
- **Área de comandos** sin scroll para mejor acceso
- **Feedback visual** mejorado en todas las operaciones
- **Ventana "Acerca de"** con información completa

## ⚠️ Solución de Problemas

### "adb no se reconoce como comando"
- **Solución**: Usa la versión portable que incluye ADB
- **Alternativa**: Instala Android SDK Platform Tools

### Error "more than one device"
1. **Usa** "🧹 Limpiar Todo" para resetear conexiones
2. **Reinicia** la aplicación
3. **Vuelve a emparejar** desde cero

### No se puede conectar por WiFi
1. **Verifica** que ambos estén en la misma red
2. **Desactiva y reactiva** "Depuración ADB por WiFi"
3. **Usa** comando `devices` en la consola para verificar

### Emparejamiento falla
- **Código caducado**: Los códigos expiran rápidamente
- **Puerto incorrecto**: Usa puerto de emparejamiento, no de conexión
- **Firewall**: Verifica que no bloquee las conexiones ADB

## 🎯 Comandos Útiles de la Consola

### Información del Sistema
```bash
shell getprop ro.build.version.release  # Versión Android
shell getprop ro.product.model          # Modelo del dispositivo
shell df -h                             # Espacio en disco
shell dumpsys battery                   # Estado de batería
```

### Gestión de Archivos
```bash
shell ls -la /sdcard/Download          # Listar descargas
shell ls -la /system/app               # Apps del sistema
push "archivo.txt" "/sdcard/"          # Enviar archivo
pull "/sdcard/archivo.txt" "./descarga.txt"  # Descargar archivo
```

### Gestión de Aplicaciones
```bash
shell pm list packages -3              # Apps de terceros
shell pm list packages -s              # Apps del sistema
install -r app.apk                     # Instalar con reemplazo
uninstall com.ejemplo.app              # Desinstalar app
```

### Sistema y Depuración
```bash
logcat -d                              # Ver logs
shell top                              # Procesos en ejecución
shell ps                               # Lista de procesos
reboot                                 # Reiniciar dispositivo
```

## 🛠️ Para Desarrolladores

### Estructura del Proyecto v1.2
```
ADB_Manager/
├── 📄 adb_manager.py          # Aplicación principal v1.2
├── 📄 README.md               # Este archivo
├── 📄 requirements.txt        # Dependencias Python
├── 🖼️ icon.ico               # Icono de la aplicación
├── 📁 adb_tools/             # Herramientas ADB para portable
│   ├── adb.exe
│   ├── AdbWinApi.dll
│   ├── fastboot.exe
│   └── [archivos ADB...]
├── 📁 screenshots/           # Capturas de pantalla
└── 📁 dist/                  # Ejecutables compilados
```

### Variables de Configuración
```python
# Cambiar fácilmente la versión y configuración
APP_VERSION = "1.2"
APP_TITLE = "ADB Manager"
DEVELOPER = "Alex G.T"
COMPANY = "REPROTEQ 2025"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 850
```

### Compilación Automática
```bash
# Script de compilación incluido
python build_portable.py

# O usando el .bat incluido
build_portable.bat
```

## 📊 Estadísticas v1.2

- **21+ comandos rápidos** organizados
- **6 herramientas integradas** de diagnóstico
- **3 métodos de conexión** (WiFi, USB, automático)
- **4 tipos de transferencia** (APK, archivos, capturas, pull)
- **Interfaz 25% más grande** para mejor usabilidad
- **100% portable** sin dependencias externas

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas:

1. **Fork** el proyecto
2. **Crea** una rama (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. **Push** (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

## 📞 Soporte

- **GitHub Issues**: Para bugs y sugerencias
- **YouTube**: [Tutorial completo](https://youtu.be/hvMkiT95O5E)
- **Email**: Incluye logs y pasos para reproducir problemas

## 🎯 Roadmap v1.3

- [ ] **Explorador de archivos** integrado en el dispositivo
- [ ] **Transferencia múltiple** de archivos
- [ ] **Gestión de backups** automáticos
- [ ] **Modo desarrollador** con herramientas avanzadas
- [ ] **Soporte para múltiples dispositivos** simultáneos
- [ ] **Interfaz web** opcional
- [ ] **Integración con Android Studio**
- [ ] **Temas personalizables**

## 🏆 Reconocimientos

- **Android Debug Bridge** - Google Android Team
- **Python Tkinter** - Python Software Foundation
- **PyInstaller** - PyInstaller Development Team
- **Comunidad Android** - Por feedback y testing

---

## 📱 Compatibilidad

- **✅ Windows 10/11** (ejecutable portable)
- **✅ Android 4.1+** (API 16+)
- **✅ Wear OS 2.0+**
- **✅ Android TV**
- **✅ Dispositivos rooteados y no rooteados**

## 🎥 Media

- **🎬 Video Tutorial**: [YouTube](https://youtu.be/hvMkiT95O5E)
- **📸 Screenshots**: [Ver galería](screenshots/)
- **📱 Demo en vivo**: Disponible en el video

---

**Desarrollado con ❤️ por Alex G.T para REPROTEQ 2025**

**¿Te gusta el proyecto? ⭐ Dale una estrella en GitHub**
