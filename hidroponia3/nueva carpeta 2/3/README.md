# Sistema de Monitoreo Hidropónico PWA 🌱

Una aplicación web progresiva (PWA) para monitoreo en tiempo real de cultivos hidropónicos de tomate, con análisis automático de nutrientes, pH y variables ambientales.

## 📁 Estructura del Proyecto

```
.
├── index.html              # Aplicación principal PWA
├── manifest.json          # Configuración del instalable
├── sw.js                  # Service Worker (offline & caché)
├── .gitignore            # Archivos ignorados por git
│
├── src/                   # Recursos estáticos
│   ├── estilo.css        # Estilos principales
│   └── script.js         # JavaScript original
│
├── config/               # Configuración
│   └── config.json       # Parámetros de automatización
│
├── docs/                 # Documentación técnica
│   ├── README.md
│   ├── PWA_README.md
│   ├── GITHUB_SETUP.md
│   ├── AUTOMATIZACION_NUTRIENTES.md
│   └── ... otros documentos
│
└── .git/                 # Control de versiones
```

---

## 🚀 Características Principales

### ✅ Funcionalidades Implementadas

- **📊 Dashboard en Tiempo Real**
  - Sensor de temperatura (agua y ambiente)
  - pH y EC (Conductividad Eléctrica)
  - TDS (Sólidos Disueltos Totales)
  - Humedad relativa
  - Nivel de agua del tanque

- **📈 Visualización Gráfica**
  - Gráficas 4 en 1 actualizadas en tiempo real
  - Chart.js 4.4.0 para renderizado
  - Máximo 20 puntos de datos para performance

- **🧪 Automatización de Nutrientes**
  - Cálculo automático de PPM según etapa
  - Dosis de macroelementos (N, P, K, Ca, Mg, S)
  - Dosis de microelementos (Fe, Mn, Zn, Cu, B, Mo)
  - Recomendaciones de ajuste automático

- **⚗️ Automatización de pH** (NUEVO)
  - Análisis automático de correcciones pH
  - Recomendaciones basadas en valores actuales
  - Generación de reportes personalizados

- **📄 Generación de PDF**
  - Reportes técnicos completos
  - Dosis de nutrientes personalizadas
  - Datos de automatización incluidos

- **📲 Progressive Web App (PWA)**
  - Instalable en móviles y escritorio
  - Funciona offline con Service Worker
  - Caché inteligente de recursos

- **📚 Modo Docente**
  - Información técnica detallada
  - Explicaciones de cada sensor
  - Toggle para mostrar/ocultar

---

## 🔧 Instalación y Uso

### Opción 1: Navegador Web
1. Acceder a [tu-url-github-pages.io](https://tu-url-github-pages.io)
2. Usar desde cualquier navegador

### Opción 2: Instalar como Aplicación
- **Escritorio**: Click en el botón "Instalar" (Chrome/Edge)
- **Móvil**: Añadir a pantalla de inicio (Chrome/Safari)

### Opción 3: Desarrollador Local
```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/sistema-hidroponico.git
cd sistema-hidroponico

# Instalar servidor local (Python)
python -m http.server 8000

# Acceder a http://localhost:8000
```

---

## 📊 Etapas de Desarrollo del Tomate

### 🌱 Semilla/Plántula (0-20 días)
- **TDS**: 0-400 ppm
- **pH**: 5.5-6.5
- **EC**: 0.5-1.5 mS/cm

### 🌿 Vegetativa (21-40 días)
- **TDS**: 400-800 ppm
- **pH**: 5.5-6.5
- **EC**: 1.2-2.2 mS/cm

### 🌸 Floración (41-70 días)
- **TDS**: 800-1100 ppm
- **pH**: 5.8-6.5
- **EC**: 2.0-2.8 mS/cm

### 🍅 Producción (71-120 días)
- **TDS**: 1000-1200 ppm
- **pH**: 5.8-6.5
- **EC**: 2.5-3.0 mS/cm

---

## 🔐 Configuración de Firebase

El proyecto utiliza **Firebase Realtime Database** para sincronizar datos de sensores en tiempo real.

```javascript
// Rutas esperadas en Firebase:
sensores/
├── pH
├── EC
├── TDS
├── waterTemp
├── dhtTemp
├── hum
└── nivel
```

---

## 📱 Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| HTML5 | - | Estructura |
| CSS3 | - | Estilos |
| JavaScript (ES6+) | - | Lógica |
| Bootstrap | 5.3.3 | Framework UI |
| Chart.js | 4.4.0 | Gráficas |
| jsPDF | 2.5.1 | Reportes PDF |
| Firebase | 9.23.0 | BD Realtime |
| Font Awesome | 6.5.0 | Iconos |
| Service Worker | - | Offline mode |

---

## 🛠️ Desarrollo

### Estructura de Scripts

**Archivo**: `index.html` (3,300+ líneas)
- Contiene toda la interfaz UI
- Scripts inline optimizados
- Service Worker registration

**Estilos**: `src/estilo.css`
- Diseño responsivo
- Paleta personalizada
- Animaciones y transiciones

### Agregar Nuevas Funciones

1. Editar `index.html` para UI
2. Agregar funciones JavaScript en las secciones correspondientes
3. Actualizar `src/estilo.css` si es necesario
4. Actualizar documentación en `docs/`

---

## 📖 Documentación

Consulta los archivos en la carpeta `/docs` para:
- [`PWA_README.md`](docs/PWA_README.md) - Detalles de Progressive Web App
- [`AUTOMATIZACION_NUTRIENTES.md`](docs/AUTOMATIZACION_NUTRIENTES.md) - Fórmulas de nutrientes
- [`GITHUB_SETUP.md`](docs/GITHUB_SETUP.md) - Guía de deployment
- Y más archivos técnicos...

---

## 🚀 Deployment a GitHub Pages

```bash
# 1. Crear repositorio en GitHub
# ...crear en github.com con el nombre: sistema-hidroponico

# 2. Configurar remoto local
git remote set-url origin https://github.com/TU_USUARIO/sistema-hidroponico.git

# 3. Push inicial
git add .
git commit -m "Deploy: Sistema Hidropónico PWA"
git push -u origin main

# 4. En GitHub:
# Settings > Pages > Source: main branch > root folder
# Esperar 1-2 minutos hasta que esté en vivo
```

---

## 📞 Soporte y Contribuciones

Para reportar errores o sugerencias, abre un **Issue** en el repositorio.

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Libre para uso educativo y comercial.

---

## 👨‍🌾 Créditos

Desarrollado para monitoreo inteligente de hidroponía.

**Última actualización**: 2024
**Estado**: ✅ Funcional con PWA y Automatización
