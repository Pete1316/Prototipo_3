# 🔍 DIAGNÓSTICO DEL CULTIVO - VALIDACIÓN DE PPM

## 📊 Rangos de PPM Válidos para Tomate Hidropónico

| Etapa | Días | PPM Mínimo | PPM Máximo | Estado |
|-------|------|-----------|-----------|--------|
| 🌱 Semilla/Plántula | 0-20 | 0 | 400 | ✅ Óptimo |
| 🌿 Vegetativa | 21-40 | 400 | 800 | ✅ Óptimo |
| 🌸 Floración | 41-70 | 800 | 1100 | ✅ Óptimo |
| 🍅 Producción | 71-120 | 1000 | 1200 | ✅ Óptimo |

---

## ⚠️ LÍMITES DE VALIDACIÓN DEL SISTEMA

### Límite del Input HTML
- **Máximo permitido**: 1750 ppm
- **Motivo**: Permitir entrada de datos pero validar después
- **Límite técnico**: Sistema rechaza valores > 1750 ppm

### Límite Recomendado Seguro
- **Máximo recomendado**: 1200 ppm
- **¿Por qué?**: El cultivo de tomate no requiere más de 1200 ppm ni en etapa de producción
- **Riesgo si supera**: Estrés hídrico, acumulación de sales, toxicidad

---

## 🚨 DIAGNÓSTICO: Cuando PPM está en 1750 ppm

### Problemática
❌ **1750 ppm es PELIGROSO para el cultivo**
- Muy por encima del máximo recomendado (1200 ppm)
- Puede causar:
  - Quemadura de raíces (root burn)
  - Marchitez de tallos
  - Clorosis (amarillamiento de hojas)
  - Muerte de planta en 24-72 horas

### Causas Posibles
1. **Acumulación de sales** por evaporación
2. **Fertilización excesiva** (error de dosificación)
3. **Sensor descalibrado** (mide más de lo real)
4. **Agua de baja calidad** (ya tiene minerales)
5. **No hay cambio de agua** desde hace días

---

## ✅ Cómo Validar y Corregir

### PASO 1: Confirmar la Medida
```
Acciones a realizar:
□ Verificar que el sensor TDS esté limpio
□ Calibrar sensor con solución de 1500 ppm
□ Medir nuevamente (esperar 30 segundos)
□ Si marca igual, el valor es REAL
□ Si marca inferior, el sensor estaba sucio
```

### PASO 2: Reducción de Emergencia
```
SI PPM > 1200 ppm:

Opción A - Cambio Rápido (si es CRÍTICO)
├─ Apagar aireadores inmediatamente
├─ Drenar 30-40% del tanque (cuidado con raíces)
├─ Llenar con agua DESTILADA
├─ Esperar 5 minutos
├─ Medir nuevamente
└─ Repetir si es necesario

Opción B - Cambio Seguro (recomendado)
├─ Apagar aireadores
├─ Drenar 20-25% lentamente
├─ Llenar con agua filtrada
├─ Esperar 10 minutos
├─ Medir
├─ Si sigue alto, esperar 2 horas y repetir
└─ No cambiar >50% de una vez (estrés)
```

### PASO 3: Monitoreo Post-Corrección
```
Después de cambio de agua:
├─ Monitorear cada 1 hora
├─ Anotar valores en log
├─ Si baja lentamente: está funcionando ✓
├─ Si se mantiene: revisar sensor o entrada externa
└─ Si sube nuevamente: hay otro problema
```

---

## 📋 Checklist de Validación PPM

### ✅ Validación del Sistema
- [ ] El input HTML permite máximo 1750 ppm
- [ ] Sistema alerta si supera 1200 ppm
- [ ] Hay función `validarPPM()` activa
- [ ] Campo de entrada valida en tiempo real

### ✅ Validación del Sensor
- [ ] Sensor está limpio (sin algas)
- [ ] Sensor está calibrado
- [ ] Sensor tiene batería
- [ ] Sensor está sumergido en agua
- [ ] Lectura es consistente (var < 20 ppm)

### ✅ Validación del Cultivo
- [ ] Hojas NO están amarillas
- [ ] Tallos NO están marchitos
- [ ] Raíces pueden verse (si sistema lo permite)
- [ ] Plantas crecen normalmente
- [ ] NO hay mal olor en el agua

---

## 🔧 Fórmula de Corrección de PPM

Si mediste **PPM actual = 1750** y necesitas **PPM objetivo = 900**:

$$\text{Porcentaje a cambiar} = \frac{\text{PPM actual} - \text{PPM objetivo}}{\text{PPM actual}} \times 100$$

$$\text{Porcentaje a cambiar} = \frac{1750 - 900}{1750} \times 100 = 48.6\%$$

**Ejemplo con tanque de 100 L:**
$$\text{Litros a cambiar} = 100 \times 0.486 = 48.6 \text{ L}$$

⚠️ **Pero dividir en 2 cambios**: 24.3 L + (esperar 2h) + 24.3 L

---

## 📈 Curva Normal de PPM en Tomate

```
PPM durante el cultivo:

1200 ┤                               ╱─ Producción Máx
1100 ┤                        ╱─── Floración Máx
1000 ┤                    ╱────────────────────╲
 900 ┤               ╱──                       ╲
 800 ┤          ╱─── Vegetativa Máx             ╲
 700 ┤     ╱───                                ╲
 600 ┤ ╱──                                       ╲ Cosecha
 500 ┤ Vegetativa Mín                            ╲
 400 ┤─Semilla ─────────────────────────────────
 300 ┤
   0 └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─
     0  10 20 30 40 50 60 70 80 90100 110120
                    Días del Cultivo
```

---

## 🎯 Resumen Rápido de Acciones

| PPM Actual | Acción | Urgencia |
|-----------|--------|----------|
| 0-400 | Agregar nutrientes | Normal |
| 400-800 | Agregar nutrientes | Normal |
| 800-1100 | Agregar nutrientes | Normal |
| 1000-1200 | Sin acción (óptimo) | ✓ |
| 1200-1500 | Cambiar 20% agua | ⚠️ Alta |
| >1500 | Cambiar 30-40% agua | 🚨 MUY ALTA |
| 1750 | **EMERGENCIA** | 🚨🚨 |

---

## 💾 Log de Ejemplo para Validación

```
FECHA: 4/3/2026
HORA: 14:30
CULTIVO: Tomate (Día 80 - Producción)
TANQUE: 100 L

ANTES DEL CAMBIO:
  • PPM Medido: 1750 ppm ❌
  • Sensor: Calibrado ✓
  • Plantas: Estrés visible (hojas amarillas)

ACCIÓN TOMADA:
  • Cambio de agua: 2 etapas de 25 L c/u
  • Tipo agua: Filtrada
  • Hora 1: Drenar 25 L, llenar agua
  • Hora 2 (14:47): Medir = 1200 ppm
  • Esperar 2 horas
  • Hora 3 (16:45): Drenar 25 L más, llenar agua
  • Hora 4 (17:00): Medir = 950 ppm ✓

RESULTADO FINAL:
  • PPM Final: 950 ppm ✓ Óptimo
  • Tiempo total: 2.5 horas
  • Plantas: Sin más amarillamiento
  • Próxima revisión: Cada 2 horas

OBSERVACIONES:
  Sensor estaba correcto. Era acumulación real de sales.
  Reiniciar monitoreo cada 4 horas.
```

---

## ❓ Preguntas Frecuentes

**P: ¿Es posible que 1750 ppm sea correcto?**
R: No. El máximo absoluto para tomate en cualquier etapa es 1200 ppm.

**P: ¿Qué pasa si dejo 1750 ppm por error?**
R: Las plantas morirán entre 24-72 horas por quemadura de raíces.

**P: ¿Cómo sé si el sensor miente?**
R: Verifica calibración con solución patrón (1500 ppm debe marcar 1500±20)

**P: ¿Puedo cambiar 100% del agua?**
R: No, eso causa shock. Máximo 50% en una sesión.

**P: ¿Cuándo es seguro volver a fertilizar?**
R: Espera a que PPM baje a 600 ppm y mide cada 3 horas.

---

## 📞 Soporte Rápido

Si PPM está en 1750 ppm:

1. ✅ **Llama función**: `validarPPM()` → pone limite a 1750
2. ✅ **Script detecta**: Valor 1750 > 1200, muestra alerta roja
3. ✅ **Sistema recomienda**: Cambio de agua INMEDIATO
4. ✅ **Dashboard muestra**: Badge rojo en PPM
5. ✅ **Log advierte**: "SUPERA máximo recomendado"

---

**Última actualización**: 4 de Marzo de 2026  
**Sistema**: Automatización de Nutrientes v2.1  
**Cultivo**: Tomate Hidropónico (NFT)
