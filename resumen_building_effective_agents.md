# Resumen: Building Effective Agents (Anthropic)

**Autor del resumen:** Armando  
**Curso:** Aprendizaje IA - Fase 0  
**Referencia:** *Building Effective Agents* (Anthropic Engineering, 2024)

---

## 1. Introducción y Filosofía Central
En el desarrollo de aplicaciones impulsadas por Modelos de Lenguaje (LLMs), existe una tendencia a sobrecomplicar la arquitectura creando agentes completamente autónomos desde el inicio. La recomendación principal de Anthropic es la **simplicidad pragmática**: comenzar siempre con la solución más simple posible (prompts directos o flujos de código convencionales) y solo añadir autonomía y complejidad cuando la tarea realmente lo requiera.

---

## 2. Diferencia Clave: Workflows vs. Agentes

Anthropic establece una distinción fundamental en los sistemas basados en LLM:

* **Workflows (Flujos de trabajo):** Son sistemas donde los LLMs y las herramientas están orquestados mediante **rutas de código predefinidas y deterministas**. El desarrollador define de antemano el flujo de ejecución. Son predecibles, consistentes, económicos y fáciles de evaluar.
* **Agentes (Agents):** Son sistemas donde el LLM **dirige dinámicamente su propio proceso y uso de herramientas**. El modelo decide cuántos pasos dar, qué herramientas llamar y cuándo considerar terminada la tarea. Ofrecen gran flexibilidad en problemas abiertos, pero a costa de mayor latencia, coste y menor determinismo.

---

## 3. Los 5 Patrones de Arquitectura

Anthropic identifica cinco patrones fundamentales que van desde lo determinista hasta lo autónomo:

1. **Prompt Chaining (Encadenamiento de prompts):**
   Divide una tarea en una secuencia lineal fija de pasos. La salida de un LLM se convierte en la entrada del siguiente, permitiendo validaciones intermedias. Ideal para tareas donde cada paso requiere concentración profunda del modelo (ej. redactar, validar y traducir).

2. **Routing (Enrutamiento):**
   Clasifica la entrada del usuario y la dirige a una ruta o prompt especializado. Evita sobrecargar un único prompt con demasiadas instrucciones incompatibles (ej. separar soporte técnico de facturación).

3. **Parallelization (Paralelización):**
   Ejecuta múltiples llamadas al LLM al mismo tiempo. Se divide en dos variantes:
   * *Sectioning:* dividir una tarea grande en subtareas independientes (ej. auditar código y redactar documentación a la vez).
   * *Voting:* generar múltiples respuestas alternativas para evaluar consistencia, calidad o filtrar alucinaciones.

4. **Orchestrator-Workers (Orquestador y Trabajadores):**
   Un LLM central analiza el problema general, descompone la tarea en subtareas dinámicas, las asigna a modelos trabajadores independientes y finalmente sintetiza los resultados. Muy útil cuando no se sabe de antemano qué subtareas se requerirán.

5. **Evaluator-Optimizer (Evaluador y Optimizador):**
   Un modelo genera una propuesta (generador) y otro modelo evalúa la calidad y proporciona retroalimentación específica (evaluador) en un ciclo iterativo hasta alcanzar un estándar definido. Ideal para código y redacción pulida.

---

## 4. Agentes Autónomos y Buenas Prácticas

Cuando el problema exige un agente autónomo real (con bucles de acción y retroalimentación del entorno):

* **Diseño de Herramientas (Tool Design):** Las APIs y herramientas provistas al LLM deben ser claras, con nombres autoexplicativos, documentación precisa de parámetros y manejo de errores informativo (que el error le diga al modelo qué falló y cómo corregirlo).
* **Simplicidad ante todo:** No utilizar frameworks pesados y rígidos antes de entender el flujo básico con llamadas nativas a la API.
* **Humano en el bucle (Human-in-the-loop):** Para acciones críticas (como pagos, borrado de bases de datos o envío de emails externos), el agente debe solicitar aprobación explícita antes de ejecutar.
* **Observabilidad y Evaluación:** Registrar cada llamada, entrada, salida y herramienta utilizada para medir rendimiento, costo y tasas de éxito mediante pruebas continuas.

---

## 5. Conclusión
El éxito al construir agentes eficaces no radica en darles libertad absoluta de inmediato, sino en encontrar el balance correcto: estructurar con código lo predecible (workflows) y delegar al modelo únicamente los pasos que exigen razonamiento y adaptabilidad dinámica.
