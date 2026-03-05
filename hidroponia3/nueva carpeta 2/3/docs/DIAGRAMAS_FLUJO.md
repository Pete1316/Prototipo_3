```mermaid
graph TD
    A["👨‍🌾 USUARIO ABRE INTERFAZ"] --> B["📊 Ingresa Parámetros"]
    B --> C["✏️ Días de Cultivo<br/>Etapa<br/>Volumen del Tanque"]
    C --> D["🔘 Clic: Automatizar Nutrientes"]
    
    D --> E["⚙️ SISTEMA PROCESA"]
    E --> F["📡 Lee PPM Actual del Sensor"]
    F --> G["📊 Compara con Rango Ideal"]
    
    G --> H{¿PPM Actual?}
    
    H -->|"BAJO"| I["🔴 NUTRIENTES BAJOS"]
    H -->|"ALTO"| J["🔴 NUTRIENTES ALTOS"]
    H -->|"IDEAL"| K["🟢 NUTRIENTES IDEALES"]
    
    I --> I1["🧮 Calcula PPM Faltante"]
    I1 --> I2["📦 Calcula Dosis de Cada Nutriente"]
    I2 --> I3["✍️ Prepara Instrucciones"]
    I3 --> I4["⚠️ Agrega Advertencias"]
    I4 --> POPUP1["📋 POPUP con Recomendación:<br/>- Gramos de cada nutriente<br/>- Orden de aplicación<br/>- Pasos detallados<br/>- Resultado esperado"]
    
    J --> J1["🧮 Calcula PPM Exceso"]
    J1 --> J2["💧 Calcula Agua a Cambiar"]
    J2 --> J3["✍️ Prepara Instrucciones"]
    J3 --> J4["⚠️ Agrega Advertencias"]
    J4 --> POPUP2["📋 POPUP con Recomendación:<br/>- Litros a drenar (porcentaje)<br/>- Cómo hacerlo seguro<br/>- Pasos detallados<br/>- PPM esperado"]
    
    K --> K1["✅ Sin Acción"]
    K1 --> POPUP3["📋 POPUP con Mensaje:<br/>- Felicidades!<br/>- Todo está perfecto<br/>- Monitorea próximamente"]
    
    POPUP1 --> L["👨‍🌾 USUARIO EJECUTA"]
    POPUP2 --> L
    POPUP3 --> L
    
    L --> M["⏱️ Espera indicado<br/>Agrega nutrientes O<br/>Cambia agua"]
    M --> N["📏 Mide PPM nuevamente"]
    N --> O{¿Coincide con<br/>Esperado?}
    
    O -->|"✓ SÍ"| P["✅ ÉXITO"]
    O -->|"✗ NO"| Q["⚠️ Revisa volumen<br/>Repite en 2-3 horas"]
    
    P --> R["📊 Registra en Log"]
    Q --> R
    R --> S["🔄 Monitorea en 2-4 horas"]
    S --> T{¿PPM Cambió<br/>Significativamente?}
    T -->|"SÍ"| D
    T -->|"NO"| S
```

---

# 📊 DIAGRAMA DE DECISIÓN

```mermaid
graph LR
    INICIO["🚀 INICIO"] --> SENSOR["📡 Lee Sensor TDS"]
    SENSOR --> ETAPA["🌱 Identifica Etapa"]
    ETAPA --> RANGO["📊 Obtiene Rango Ideal"]
    RANGO --> COMPARA["⚖️ PPM Actual vs Rango"]
    
    COMPARA --> DEC{Resultado}
    
    DEC -->|"ALGO < MÍNIMO"| BAJO["🔴 BAJO"]
    DEC -->|"ALGO ∈ [MIN,MAX]"| OK["🟢 OK"]
    DEC -->|"ALGO > MÁXIMO"| ALTO["🔴 ALTO"]
    
    BAJO --> CAL_B["🧮 Calcula Dosis"]
    OK --> MSG_OK["✅ OK"]
    ALTO --> CAL_A["💧 Calcula Cambio Agua"]
    
    CAL_B --> REC_B["📋 Recomendación:<br/>Agregar nutrientes"]
    MSG_OK --> REC_OK["✅ Sin acción"]
    CAL_A --> REC_A["📋 Recomendación:<br/>Cambiar agua"]
    
    REC_B --> OUT["📤 Muestra al Usuario"]
    REC_OK --> OUT
    REC_A --> OUT
    
    OUT --> FIN["✔️ FIN"]
```

---

# 🔄 CICLO DE OPERACIÓN DIARIA

```mermaid
timeline
    title Ciclo Típico Diario de Monitoreo
    
    6:00 : Revisa Dashboard 📊
    6:15 : Primer cálculo automático
    6:30 : Ejecuta acción si es necesario
    
    12:00 : Segunda revisión
    12:15 : Cálculo automático
    12:30 : Ejecuta acción si es necesario
    
    18:00 : Tercera revisión  
    18:15 : Cálculo automático
    18:30 : Ejecuta acción si es necesario
    
    23:00 : Revisión nocturna rápida
    23:15 : Verifica sensores
```

---

# 📈 CAMBIOS DE PPM TÍPICOS

```
Antes y después del cálculo automático:

AGREGAR NUTRIENTES:
  350 ppm ──[+100 ppm]──> 450 ppm
           (5 minutos)
           
  La función calcula:
  ✓ Qué agregar exactamente
  ✓ En qué orden
  ✓ Cuánto esperar
  
---

CAMBIAR AGUA:
  1150 ppm ──[cambio 30%]──> 805 ppm
           (5 minutos)
           
  La función calcula:
  ✓ Cuánta agua drenar (30% = 30L de 100L)
  ✓ Cómo hacerlo sin shock
  ✓ PPM esperado
```

---

# 🎯 MATRIZ DE DECISIÓN

| PPM Actual | Rango Ideal | Estado | Acción |
|-----------|------------|--------|--------|
| 200 | 400-800 | 🔴 Bajo | Agregar nutrientes |
| 350 | 400-800 | 🔴 Bajo | Agregar nutrientes |
| 450 | 400-800 | 🟢 OK | Monitorear |
| 600 | 400-800 | 🟢 OK | Monitorear |
| 750 | 400-800 | 🟢 OK | Monitorear |
| 850 | 400-800 | 🔴 Alto | Cambiar agua |
| 1000 | 400-800 | 🔴 Alto | Cambiar agua |
| 1200 | 400-800 | 🔴 Alto | Cambiar agua |

---

# 🔐 LÍMITES DE SEGURIDAD

```
MAX AGREGAR EN UNA DOSIS:
  200 ppm
  └─> Si necesita más, divide en 2-3 aplicaciones

MAX CAMBIAR AGUA EN UNA VEZ:
  50% del tanque
  └─> Si necesita más, divide en 2 cambios

TIEMPO ENTRE NUTRIENTES:
  10 minutos (para evitar picos)

TIEMPO ENTRE DOSIS:
  1-2 horas (para observar plantas)

TEMPERATURA AGUA:
  18-24°C ideal
  └─> >25°C favorece problemas de raíz
```

---

Estos diagramas muestran visualmente cómo el sistema:
1. Lee el sensor
2. Compara con rangos ideales
3. Decide la acción
4. Calcula exactamente qué hacer
5. Instruye al usuario
6. Se cicla continuamente

El proceso es **automático, seguro y preciso**.
