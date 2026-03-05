# 🤖 GUÍA DE AUTOMATIZACIÓN DE NUTRIENTES (PPM)

## ¿Qué es la Automatización de Nutrientes?

Es una función que **calcula automáticamente** qué hacer cuando los nutrientes en tu tanque están fuera del rango ideal:
- **Si están bajos** → Te dice CUÁNTO NUTRIENTE agregar
- **Si están altos** → Te dice CUÁNTA AGUA cambiar
- **Si están ideales** → Todos los sensores están en perfecto equilibrio ✓

---

## 📊 Cómo Funciona

### 1️⃣ **CASO: PPM BAJO (Faltan Nutrientes)**

**Ejemplo:** 
- Tu tanque tiene 350 ppm
- Para tomate en fase Vegetativa necesitas 400-800 ppm
- Falta: 50 ppm

**La función te calcula:**
```
📦 Cantidad de CADA nutriente a agregar:
  • Nitrógeno (N): 2.5 g
  • Fósforo (P): 1.2 g
  • Potasio (K): 3.0 g
  • Calcio (Ca): 1.8 g
  • Magnesio (Mg): 0.9 g
  • Azufre (S): 0.6 g

💊 Microelementos (si es necesario ese día):
  • Hierro (Fe): 0.05 g
  • Manganeso (Mn): 0.02 g
  ... etc
```

**Instrucciones automáticas:**
1. Disolver según orden: N → P → K → Ca → Mg → S
2. Esperar 10 min entre cada adición
3. Medir el PPM después

---

### 2️⃣ **CASO: PPM ALTO (Nutrientes en Exceso)**

**Ejemplo:**
- Tu tanque tiene 1100 ppm
- Para tomate en fase Vegetativa ideal es 600 ppm
- Exceso: 500 ppm

**La función te calcula:**
```
💧 Cambio de agua requerido:
   → Cambiar 35 L de tu tanque de 100 L (35%)
   → PPM esperado después: 600 ppm
```

**Instrucciones automáticas:**
1. Apagar aireadores y sifones
2. Drenar exactamente esos 35 L
3. Llenar con agua fresca (SIN nutrientes)
4. A los 5 minutos, medir PPM para verificar

---

### 3️⃣ **CASO: PPM IDEAL (Todo bien)**

✅ El sistema está perfecto
- Continúa monitoreando cada 2-4 horas
- No se requiere ninguna acción

---

## 🎯 Pasos para Usar

### Paso 1: Configurar los parámetros

En la pestaña "Diagnóstico del Cultivo" ingresa:
- **Días de cultivo** (0-120)
- **Etapa actual** (Semilla, Vegetativa, Floración, Producción)
- **Volumen del tanque en litros** (ejemplo: 100 L)

### Paso 2: Verificar que los sensores estén conectados

En el Dashboard, necesitas ver valores en:
- **TDS**: el sensor de nutrientes (ppm)
- **pH**, **EC**, **Temperatura**, etc.

Si dice "Conectando con sensores..." → Los sensores aún no envían datos

### Paso 3: Clic en botón "⚙️ Automatizar Nutrientes"

El sistema:
1. Lee automáticamente el PPM actual del sensor (TDS)
2. Compara con el rango ideal de tu etapa
3. Calcula exactamente qué hacer
4. Muestra una recomendación detallada

---

## 📋 Rango de PPM Ideal por Etapa

| Etapa | Días | PPM Min | PPM Max | EC (mS/cm) |
|-------|------|---------|---------|-----------|
| 🌱 Semilla | 0-20 | 0 | 400 | 0.5-1.5 |
| 🌿 Vegetativa | 21-40 | 400 | 800 | 1.2-2.2 |
| 🌸 Floración | 41-70 | 800 | 1100 | 2.0-2.8 |
| 🍅 Producción | 71-120 | 1000 | 1200 | 2.5-3.0 |

---

## ⚠️ Advertencias Importantes

### ⚡ Si necesita AGREGAR más de 200 ppm:
- NO lo hagas todo de una vez
- Divide en 2-3 dosis
- Espera 1 hora entre dosis
- Esto evita estres en las plantas

### ⚡ Si necesita CAMBIAR más del 50% del agua:
- NO drenyes directo de un tanque lleno
- Primero cambio parcial (25-35%)
- Espera 2 horas
- Mide nuevamente
- Si sigue alto, repite otra vez

---

## 🔍 Ejemplo Práctico Completo

```
📌 SITUACIÓN REAL:
   - Tienes un cultivo de tomate de 35 días (fase Vegetativa)
   - Tanque de 100 litros
   - Sensor TDS marca 450 ppm
   
⚙️ EJECUTAS AUTOMATIZACIÓN:

🟢 RESULTADO: "NUTRIENTES IDEALES"
   ✓ 450 ppm está dentro de 400-800 ppm
   ✓ No necesitas hacer nada
   ✓ Continúa monitoreando

---

📌 OTRA SITUACIÓN:
   - Mismo cultivo, pero ahora TDS marca 350 ppm
   - (Bajo porque has hecho cambios de agua)

🔴 RESULTADO: "NUTRIENTES BAJOS"
   Necesitas agregar a 100 L:
   • Nitrato de potasio (KNO3): 2.5 g
   • Fosfato monopotásico (KH2PO4): 1.2 g
   • Etc...
   
   Instrucciones claras paso a paso

---

📌 OTRA MÁS:
   - TDS marca 1250 ppm (muy alto)
   - Está en 1250 pero necesitas 600

🔴 RESULTADO: "NUTRIENTES ALTOS"
   Necesitas cambiar:
   • 42 L de agua (42%)
   • PPM esperado después: 600 ppm
   
   Instrucciones claras para drenar y llenar
```

---

## 🛠️ Consejos Prácticos

1. **Mide el PPM antes y después** - Verifica que la automatización fue correcta

2. **Hazlo lentamente** - No cambies todo de una vez

3. **Observa a las plantas** - Si ves estrés, reduce los cambios (menos fertilizante, menos cambio de agua)

4. **Horario recomendado**:
   - 🌅 Mañana: 1er medición
   - 🌤️ Mediodía: 2da medición
   - 🌆 Tarde: 3er medición
   - Si está fuera de rango → ejecuta automatización

5. **Aireación** - Mantén los aireadores 24/7, EXCEPTO cuando cambies agua

---

## 📞 Soporte

Si algo no está claro:
1. Verifica que los sensores estén conectados a Firebase
2. Asegúrate de ingresar el volumen correcto del tanque
3. Revisa el TDS en el Dashboard coincida con lo que marca tu sensor manual
4. Si hay diferencia, calibra el sensor

---

**¡Tu sistema hidropónico ahora es inteligente! 🚀**
