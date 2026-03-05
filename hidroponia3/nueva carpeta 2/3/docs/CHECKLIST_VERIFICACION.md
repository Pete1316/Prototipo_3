# ✔️ CHECKLIST DE VERIFICACIÓN - AUTOMATIZACIÓN LISTA

## 🔍 Antes de Usar la Automatización

Verifica estos puntos para asegurar que todo funciona correctamente:

---

## 📋 Checklist Técnico

### ✅ Sensores Conectados
```
En la pestaña Dashboard, confirma que ves:
☐ TDS/PPM (Sensor de nutrientes) - mostrará un número
☐ pH (Sensor de acidez)
☐ EC (Conductividad)
☐ Temp. Agua
☐ Temp. Ambiente
☐ Humedad
☐ Nivel

Si alguno dice "--", revisa:
  → Conexión con Firebase
  → Que el Arduino/ESP32 esté enviando datos
  → WiFi conectado
```

### ✅ Datos Correctos en Dashboard
```
☐ El TDS que ves en Dashboard coincide con tu sensor manual
  (Si no, calibra el sensor)
☐ Los valores se actualizan en tiempo real
☐ No hay errores en la consola (F12 → Consola)
```

### ✅ Base de Datos Firebase Funcionando
```
☐ Dice "Conectado y recibiendo datos en tiempo real"
☐ Si dice error → revisa Firebase config en el código
```

---

## 👨‍🌾 Checklist Operacional

### ✅ Parámetros del Cultivo
```
☐ Sabes exactamente cuántos días tiene tu cultivo
☐ Identificaste bien la etapa (Semilla/Vegetativa/Floración/Producción)
☐ Mediste el volumen real del tanque en litros
☐ Anotaste el volumen en el campo "Volumen del tanque"
```

### ✅ Sensores Calibrados
```
☐ Sensor TDS está calibrado correctamente
☐ Sensor pH está calibrado (7.0 buffer mínimo)
☐ Sensor EC está en buen estado
☐ Temperaturas parecen realistas
```

### ✅ Sistema Preparado
```
☐ Tienes acceso a nutrientes para agregar (si es necesario)
☐ Tienes forma de drenar agua (si es necesario)
☐ Tienes agua fresca disponible
☐ Tu tanque tiene nivel mínimo de 20-30 L
```

---

## 🧪 Test de Funcionamiento

### Test 1: Verificar que el botón aparece
```
Pasos:
1. Abre: Pestaña "Diagnóstico del Cultivo"
2. Busca los botones encima del formulario
3. Deberías ver: "Calcular Todo | ⚙️ Automatizar Nutrientes | Generar PDF"

☐ El botón "⚙️ Automatizar Nutrientes" existe
☐ Es de color rojo
☐ Al pasar el mouse, muestra tooltip
```

### Test 2: Clic de prueba sin parámetros
```
Pasos:
1. Completa mínimamente:
   - Días: 25
   - Etapa: Vegetativa
   - Volumen: 100
2. Presiona "⚙️ Automatizar Nutrientes"

Resultados esperados:
☐ Abre un popup con recomendación
☐ El popup muestra un estado (🟢 o 🔴 o 🔴)
☐ Muestra información sobre PPM actual y rango ideal
☐ Contiene instrucciones claras
```

### Test 3: Verificar que lee el sensor
```
Pasos:
1. Vuelve a Dashboard (pestaña Dashboard)
2. Confirma que TDS tiene un valor (ej: "650")
3. Vuelve a Diagnóstico
4. Presiona nuevamente "⚙️ Automatizar Nutrientes"

Resultados esperados:
☐ El campo "ppmActualDashboard" (dentro del popup) muestra ese valor
☐ Las recomendaciones se basan en ese valor real
```

---

## 🐛 Solucionar Problemas

### Si el botón NO aparece:
```
1. Recarga la página (Ctrl+F5)
2. Abre la consola (F12)
3. Verifica que NO haya errores en rojo
4. Si hay errores, busca "automatizar" en el archivo HTML
5. Revisa que la función esté antes del Firebase
```

### Si el popup aparece pero está vacío:
```
1. Abre consola (F12)
2. Busca errores en rojo
3. El campo "Volumen" ¿está vacío? → Complétalo
4. ¿El sensor dice "--"? → Sensores no conectados
```

### Si los números no cuadran:
```
1. Verifica el volumen ingresado es correcto
2. Verifica que el TDS del sensor coincida con manual
3. Reinicia la página si los datos están desactualizados
```

---

## 🎯 Primera Ejecución Real

Cuando todo esté verificado, haz esto:

### Paso 1: Tomar lectura manual
```
1. Con sensor manual: mide el TDS/PPM actual
2. Anota el valor (ej: 450 ppm)
3. Si difiere del Dashboard > 50 ppm → calibra
```

### Paso 2: Ejecutar automatización
```
1. Asegúrate que Dashboard muestre ese mismo valor
2. Ve a Diagnóstico
3. Presiona "⚙️ Automatizar Nutrientes"
4. Lee la recomendación completa
```

### Paso 3: Ejecutar recomendación
```
1. Si dice agregar: Pesa y disuelve nutrientes
2. Si dice cambiar: Drena y llena agua
3. Sigue las instrucciones paso a paso
```

### Paso 4: Medir nuevamente
```
1. Espera 5 minutos
2. Toma lectura manual
3. Compara con valor esperado
4. Si está cerca (±50 ppm) → ¡Éxito! ✓
5. Si no → verifica volumen y proporciones
```

---

## 📞 Debugging Avanzado

Si necesitas más detalles, abre la consola (F12) y prueba:

```javascript
// Verifica la función existe
typeof automatizarAjustePPM
// Deberá decir: "function"

// Verifica datos actuales
console.log(document.getElementById("ppmActualDashboard").textContent)
// Deberá mostrar un número

// Verifica la etapa
console.log(document.getElementById("etapaSelectNutrientes").value)
// Deberá mostrar: plantula, vegetativa, floracion o produccion

// Verifica el volumen
console.log(document.getElementById("volumeTanque").value)
// Deberá mostrar un número
```

---

## ✅ Checklist Final

Antes de usar en producción:

```
☐ Todos los puntos de "Checklist Técnico" pasados
☐ Todos los puntos de "Checklist Operacional" pasados
☐ Test 1, 2 y 3 completados exitosamente
☐ Primera ejecución real fue precisa (±50 ppm)
☐ Sensores están calibrados
☐ Tienes todo listo para reacción rápida
```

---

## 🎉 ¡LISTO!

Si marcaste todos los checkboxes:

✅ La automatización está lista para usar
✅ Puedes confiar en los cálculos
✅ Tus plantas estarán con nutrición óptima

**Monitorea cada 2-4 horas y ajusta según sea necesario.**

---

**¿Preguntas?** Revisa los otros documentos:
- GUIA_RAPIDA.md
- AUTOMATIZACION_NUTRIENTES.md  
- RESUMEN_CAMBIOS.md
