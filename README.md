# 📱 ADB File Manager

Una aplicación GUI moderna y simplificada para gestionar archivos en dispositivos Android mediante ADB (Android Debug Bridge). Diseñada especialmente para dispositivos Wear OS con soporte completo para emparejamiento WiFi.

## ✨ Características

- 🔗 **Emparejamiento WiFi** - Conecta dispositivos usando códigos de emparejamiento
- 📤 **Transferencia de archivos** - Envía cualquier tipo de archivo al dispositivo
- 📦 **Instalación de APKs** - Instala aplicaciones automáticamente
- 📥 **Descarga de archivos** - Descarga archivos desde el dispositivo
- 🔌 **Conexión USB** - Soporte para dispositivos conectados por cable
- 🛠️ **Herramientas integradas** - Información del dispositivo, capturas, gestión de apps
- 🧹 **Limpieza automática** - Resuelve conflictos de múltiples dispositivos
- 🌐 **Escaneo de red** - Busca dispositivos ADB en la red local

## 🖥️ Interfaz

### Pantalla Principal
![Pantalla Principal](screenshots/main_screen.png)

La interfaz principal muestra:
- **Sección de Conexión**: IP, Puerto, Código de emparejamiento
- **Gestión de Archivos**: Selección, instalación y transferencia
- **Herramientas**: Utilidades para gestión del dispositivo
- **Log en tiempo real**: Feedback detallado de todas las operaciones

### Proceso de Emparejamiento
![Emparejamiento](screenshots/pairing_process.png)

1. **Configura WiFi Debugging** en tu dispositivo
2. **Introduce** IP, puerto y código mostrados
3. **Empareja** usando el botón correspondiente
4. **Conecta** con el puerto de conexión

### Gestión de Archivos
![Gestión de Archivos](screenshots/file_management.png)

- **Selecciona archivos** de cualquier tipo
- **Instalación automática** para APKs
- **Transferencia universal** para documentos, imágenes, videos, etc.
- **Progreso visual** con barras de estado

### Instalación Exitosa
![Instalación APK](screenshots/apk_installation.png)

- **Instalación robusta** con reinicio automático de ADB
- **Detección de conflictos** y resolución automática
- **Confirmación visual** del éxito de la operación

## 🚀 Instalación

### Requisitos
- **Python 3.7+**
- **Android SDK Platform Tools** (para ADB)
- **Tkinter** (incluido en la mayoría de instalaciones de Python)

### Pasos de instalación

1. **Clona el repositorio**
```bash
git clone https://github.com/tu-usuario/adb_manager.git
cd adb_manager
```

2. **Instala ADB** (Android SDK Platform Tools)
   - **Windows**: Descarga desde [developer.android.com](https://developer.android.com/studio/releases/platform-tools)
   - **macOS**: `brew install android-platform-tools`
   - **Linux**: `sudo apt install android-tools-adb` (Ubuntu/Debian)

3. **Ejecuta la aplicación**
```bash
python adb_file_manager.py
```

## 📱 Configuración del Dispositivo

### Para Wear OS / Android

1. **Habilita Opciones de Desarrollador**:
   - Ve a `Configuración` → `Sistema` → `Acerca de`
   - Toca 7 veces en `Número de compilación`

2. **Activa Depuración ADB por WiFi**:
   - Ve a `Configuración` → `Sistema` → `Opciones desarrollador`
   - Activa `Depuración ADB por WiFi`
   - Aparecerá una pantalla con IP:PUERTO y CÓDIGO

3. **Empareja en la aplicación**:
   - **IP**: Ya está configurada como `192.168.1.80` (modifica si es necesario)
   - **Puerto**: Introduce el puerto de emparejamiento mostrado
   - **Código**: Introduce el código de 6 dígitos mostrado

## 🔧 Uso

### Emparejamiento WiFi
1. **Activa** "Depuración ADB por WiFi" en tu dispositivo
2. **Anota** la IP, puerto y código mostrados
3. **Introduce** los datos en la aplicación
4. **Haz clic** en "🔗 Emparejar"
5. **Cambia** al puerto de conexión mostrado después del emparejamiento
6. **Haz clic** en "🔗 Conectar"

### Transferencia de Archivos
1. **Conecta** tu dispositivo (WiFi o USB)
2. **Selecciona** archivo usando "📂 Seleccionar Archivo"
3. **Para APKs**: Usa "📦 Instalar APK"
4. **Para otros archivos**: Usa "📤 Enviar Archivo"
5. **Especifica** la ruta de destino en el dispositivo

### Herramientas Disponibles
- **📱 Info Dispositivo**: Información del sistema
- **📋 Apps Instaladas**: Lista de aplicaciones instaladas
- **📸 Captura**: Tomar screenshots
- **🔄 Reiniciar ADB**: Reiniciar el servidor ADB
- **🔍 Escanear Red**: Buscar dispositivos en la red
- **🧹 Limpiar ADB**: Resolver conflictos de conexión

## ⚠️ Solución de Problemas

### Error "more than one device/emulator"
- **Usa** el botón "🧹 Limpiar ADB"
- **Reinicia** la aplicación
- **Vuelve a emparejar** el dispositivo

### No se puede conectar
- **Verifica** que ambos dispositivos estén en la misma red WiFi
- **Desactiva y reactiva** "Depuración ADB por WiFi"
- **Usa** "🔄 Reiniciar ADB"

### Emparejamiento falla
- **Verifica** que el código sea correcto (caduca rápidamente)
- **Asegúrate** de usar el puerto de emparejamiento, no el de conexión
- **Reactiva** la depuración WiFi para obtener nuevos datos

## 🛠️ Desarrollo

### Estructura del Proyecto
```
adb_manager/
├── adb_file_manager.py    # Aplicación principal
├── README.md              # Este archivo
├── screenshots/           # Capturas de pantalla
│   ├── main_screen.png
│   ├── pairing_process.png
│   ├── file_management.png
│   └── apk_installation.png
└── requirements.txt       # Dependencias (opcional)
```

### Funcionalidades Técnicas
- **Interfaz moderna** con Tkinter y tema oscuro
- **Threading** para operaciones no bloqueantes
- **Manejo robusto de errores** con reintentos automáticos
- **Limpieza automática** de conexiones ADB duplicadas
- **Placeholders inteligentes** para campos de entrada
- **Log en tiempo real** con códigos de color

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:

- **Abre un issue** en GitHub
- **Incluye** logs de la aplicación
- **Describe** los pasos para reproducir el problema

## 🎯 Roadmap

- [ ] Soporte para transferencia de múltiples archivos
- [ ] Integración con Android File Transfer
- [ ] Modo batch para instalación masiva de APKs
- [ ] Interfaz web opcional
- [ ] Soporte para Android TV

---

**Desarrollado con ❤️ para la comunidad Android**