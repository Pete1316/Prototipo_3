# 🍅 EJEMPLOS ESPECÍFICOS - CULTIVO DE TOMATE HIDROPÓNICO

## Tu Cultivo Actual

```
🌱 TOMATE HIDROPÓNICO
├─ Sistema: NFT (Nutrient Film Technique)
├─ Tanque: 100 litros
├─ Sensor: TDS para PPM
└─ Objetivo: Máxima cosecha
```

---

## 📅 ETAPAS POR SEMANA

### SEMANA 1-3: FASE SEMILLA/PLÁNTULA 🌱
```
Rango PPM: 0-400

MI CULTIVO ESPECÍFICO (Día 10):
  • Días: 10
  • Etapa: Semilla
  • Volumen: 100 L
  • TDS Actual: 200 ppm

ACCIÓN A TOMAR:
  ✓ Sin acción
  ✓ Esperar a que crezca más
  ✓ Mantener agua limpia

Monitorea cada 4-6 horas
```

---

### SEMANA 4-6: FASE VEGETATIVA 🌿
```
Rango PPM: 400-800

MI CULTIVO ESPECÍFICO (Día 30):
  • Días: 30
  • Etapa: Vegetativa
  • Volumen: 100 L
  • TDS Actual: 350 ppm ← BAJO

QUE PASA:
  Las plantas crecen rápido
  Necesitan más nitrógeno
  
ACCIÓN AUTOMÁTICA:

  🔴 NUTRIENTES BAJOS
  
  Agregar a 100 L:
  ├─ Nitrogeno (N): 2.5 g
  ├─ Fosforo (P): 0.67 g
  ├─ Potasio (K): 1.67 g
  ├─ Calcio (Ca): 0.67 g
  ├─ Magnesio (Mg): 0.25 g
  └─ Azufre (S): 0.17 g
  
  INSTRUCCIONES:
  1. Disolver en orden: N→P→K→Ca→Mg→S
  2. Esperar 10 min entre cada
  3. Medir EC/PPM
  4. Debería subir a ~400-500 ppm
  5. Si no basta, repetir en 2 horas

Monitorea cada 3-4 horas
```

---

### SEMANA 7-10: FASE FLORACIÓN 🌸
```
Rango PPM: 800-1100

MI CULTIVO ESPECÍFICO (Día 50):
  • Días: 50
  • Etapa: Floración
  • Volumen: 100 L
  • TDS Actual: 1050 ppm ← PERFECTO

QUE PASA:
  Aparecen flores
  Primeros tomates pequeños
  Necesita balance de nutrientes
  
ACCIÓN AUTOMÁTICA:

  🟢 NUTRIENTES IDEALES
  
  ✓ 1050 ppm está en rango 800-1100
  ✓ Perfecto para esta etapa
  ✓ Sin acción requerida
  
  RECOMENDACIÓN:
  • Continúa monitoreando cada 2-4h
  • Las plantas usan nutrientes lentamente
  • Si baja mucho en 1 día, agrega pequeña dosis
  • Si sube, cambia agua

Monitorea cada 2-3 horas
```

---

### SEMANA 11-18: FASE PRODUCCIÓN 🍅
```
Rango PPM: 1000-1200

MI CULTIVO ESPECÍFICO (Día 80):
  • Días: 80
  • Etapa: Producción
  • Volumen: 100 L
  • TDS Actual: 1250 ppm ← ALTO

QUE PASA:
  Los tomates crecen
  Están casi listos para cosechar
  PPM está muy alto (estrés)
  
ACCIÓN AUTOMÁTICA:

  🔴 NUTRIENTES ALTOS
  
  Cambiar agua:
  ├─ Drenar: 45.5 L (45.5%)
  ├─ Llenar: Con agua fresca
  └─ PPM esperado: 680 ppm
  
  INSTRUCCIONES:
  1. Apagar aireadores
  2. Drenar 45.5 L lentamente
  3. Llenar con agua fresca (sin nutrientes)
  4. A los 5 min, medir
  5. Debería estar en ~680 ppm
  6. Si está en ~800-900, ¡perfecto!
  7. Si sigue >1000, repetir en 2 horas
  
  ⚠️ ADVERTENCIA:
  No drenear >50% de una vez
  Las raices pueden estresarse

Monitorea cada 2 horas (muy crítico)
```

---

## 🔄 CICLOS REALES - SIMULACIÓN

### Escenario 1: Día 25 - Todo Bajo
```
ENTRADA AL SISTEMA:
┌─────────────────────────────┐
│ Días: 25                    │
│ Etapa: Vegetativa           │
│ Volumen: 100 L              │
│ PPM actual (sensor): 300    │
└─────────────────────────────┘

CÁLCULOS AUTOMÁTICOS:
Falta: 400 - 300 = 100 ppm

Nutrientes a agregar a 100 L:
├─ N: 5.0 g (Nitrato de Potasio)
├─ P: 1.33 g (Fosfato Monopotásico)
├─ K: 3.33 g (Nitrato de Potasio)
├─ Ca: 1.33 g (Nitrato de Calcio)
├─ Mg: 0.50 g (Sulfato de Magnesio)
└─ S: 0.33 g (en la mezcla de Mg)

PASOS:
1. Pesar 5.0g de KNO3
2. Disolver en 10 L de agua
3. Verter al tanque
4. Esperar 10 min [timer ⏱️]
5. Pesar 1.33g de KH2PO4
6. Disolver y verter
... (continuar con otros)
8. Esperar 5 min
9. Medir: debería estar ~400 ppm
10. Si está bien, ¡listo!

RESULTADO ESPERADO:
Antes:  300 ppm
Después: 400 ppm ✓

Documentar en log:
  25/02/2024 14:30
  Fertilizante agregado: N+P+K+Ca+Mg
  Resultado: 400 ppm ✓
```

---

### Escenario 2: Día 45 - Todo Alto
```
ENTRADA AL SISTEMA:
┌──────────────────────────────┐
│ Días: 45                     │
│ Etapa: Floración             │
│ Volumen: 100 L               │
│ PPM actual (sensor): 1200    │
└──────────────────────────────┘

CÁLCULOS AUTOMÁTICOS:
Exceso: 1200 - 900 = 300 ppm

Cambio de agua requerido:
% = (1200 - 900) / 1200 × 100 = 25%
Volumen a drenar = 100 × 0.25 = 25 L

PASOS:
1. Apagar sistemas de aireación
2. Preparar contenedor de 25 L
3. Sifon o llave lentamente
4. Drenar exactamente 25 L
5. PAUSA: Esperar 10 min
6. Llenar con 25 L de agua fresca (SIN nutrientes)
7. PAUSA: Esperar 5 min para mezclar
8. Medir: debería estar ~900 ppm
9. Si está bien, ¡listo!
10. Encender aireadores nuevamente

RESULTADO ESPERADO:
Antes:  1200 ppm
Después: 900 ppm ✓

Documentar en log:
  01/03/2024 10:45
  Cambio agua: 25 L (25%)
  Resultado: 900 ppm ✓
```

---

### Escenario 3: Día 60 - Perfecto
```
ENTRADA AL SISTEMA:
┌─────────────────────────────┐
│ Días: 60                    │
│ Etapa: Floración            │
│ Volumen: 100 L              │
│ PPM actual (sensor): 950    │
└─────────────────────────────┘

CÁLCULOS AUTOMÁTICOS:
Estado: DENTRO DEL RANGO 800-1100 ✓

RESULTADO:

🟢 NUTRIENTES IDEALES

✓ 950 ppm es perfecto para floración
✓ Sin acción requerida
✓ Continúa monitoreando

PRÓXIMAS ACCIONES:
- Monitorear cada 3 horas
- Si baja >100 ppm, agregar nutrientes
- Si sube >100 ppm, cambiar agua
- Observar plantas (sin estrés)

Documentar en log:
  02/03/2024 15:30
  Estado: Óptimo
  PPM: 950 ppm ✓
```

---

## 📊 TABLA DE REFERENCIA RÁPIDA PARA TOMATE

| Etapa | Semana | Días | PPM | Acción si bajo | Acción si alto |
|-------|--------|------|-----|---|---|
| 🌱 Semilla | 1-3 | 0-20 | 0-400 | Esperar | Cambiar agua |
| 🌿 Vegetativa | 4-6 | 21-40 | 400-800 | Agregar N rico | Cambiar 20-30% |
| 🌸 Floración | 7-10 | 41-70 | 800-1100 | Agregar balanceado | Cambiar 30-40% |
| 🍅 Producción | 11-18 | 71-120 | 1000-1200 | Agregar balanceado | Cambiar 40-50% |

---

## 🛠️ HERRAMIENTAS QUE NECESITAS

```
Para reaccionar rápido:

MEDIR:
  ☐ Sensor TDS (en el tanque)
  ☐ Termómetro (temperatura agua)
  ☐ pH metro (calibrado)

AGREGAR NUTRIENTES:
  ☐ Balanza de precisión (0-100g)
  ☐ Vaso o recipiente para mezclar
  ☐ Cuchara de dosificación
  ☐ Nutrientes (N, P, K, Ca, Mg, S)
  ☐ Pipeta o jeringa (para micros)

CAMBIAR AGUA:
  ☐ Sifón de goma o bomba
  ☐ Cubos o contenedores
  ☐ Tela o colador (para agua)
  ☐ Trapos limpios

REGISTRAR:
  ☐ Cuaderno o aplicación
  ☐ Fecha y hora
  ☐ Mediciones
  ☐ Acciones ejecutadas
```

---

## 📈 CURVA TÍPICA DE PPM EN TOMATE

```
PPM durante todo el cultivo:

1200 ┤                               ╱─ Producción
1100 ┤                        ╱─── Floración ─╲
1000 ┤                    ╱────────────────────╲
 900 ┤               ╱──                       ╲
 800 ┤          ╱───                           ╲
 700 ┤     ╱───                                ╲
 600 ┤ ╱──Vegetativa                           ╲ Cosecha
 500 ┤                                          ╲
 400 ┤─Semilla                                  
 300 ┤
   0 └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─
     0 10 20 30 40 50 60 70 80 90 100 120
                    Días

⚠️ NOTA: Esto es una guía. Ajusta según:
   • Tu sistema específico
   • Variedad de tomate
   • Condiciones climáticas
   • Resultados observados en plantas
```

---

## 💾 REGISTRO SUGERIDO

```
FECHA: 25/02/2024
HORA: 14:30
ETAPA: Vegetativa (Día 25)
PPM ANTERIOR: 300 ppm
ACCIÓN: Fertilizar
NUTRIENTES AGREGADOS:
  • N: 5.0 g
  • P: 1.33 g
  • K: 3.33 g
  • Ca: 1.33 g
  • Mg: 0.50 g
  • S: 0.33 g
PPM DESPUÉS (5 min): 400 ppm
OBSERVACIONES: Plantas sanas, sin estrés
PRÓXIMA REVISIÓN: 25/02/2024 18:30
```

---

## 🎯 OBJETIVO FINAL

Con estos cálculos automáticos:
```
✓ No hay errores de medición
✓ Nutrición óptima garantizada
✓ Las plantas crecen al máximo
✓ Te ahorras cálculos mentales
✓ Proceso rápido y confiable
```

---

**¡Usa estos ejemplos como guía durante tu cultivo! 🚀**
