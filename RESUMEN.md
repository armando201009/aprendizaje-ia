# Resumen: Building Effective Agents (Anthropic)

**Autor:** Armando  
**Fase 0:** Entorno y Fundamentos de Arquitectura de Agentes  
**Lectura:** [*Building Effective Agents*](https://www.anthropic.com/research/building-effective-agents) — Anthropic Engineering

---

## 1. La Regla de Oro: Empezar por lo más simple

La lección primordial que plantea Anthropic es no caer en la trampa de sobrecomplicar la arquitectura desde el día uno. Muchos desarrolladores intentan resolver sus problemas implementando frameworks pesados de agentes autónomos con memoria compleja y decenas de herramientas, cuando en la práctica la inmensa mayoría de las aplicaciones tienen mucho mejor desempeño, menor costo y latencias drásticamente inferiores empezando por lo más elemental: **un prompt bien optimizado con llamadas directas a la API**.

La complejidad nunca debe ser el punto de partida, sino una decisión deliberada: solo se debe agregar un nuevo nivel de abstracción o autonomía si las pruebas empíricas demuestran que mejora el resultado final.

---

## 2. Diferencia Fundamental: Workflows vs. Agentes

Para entender cuándo y cómo utilizar la IA, Anthropic establece una distinción clara entre dos conceptos:

* **Workflows (Flujos de trabajo):** Son sistemas donde los modelos de lenguaje y las herramientas están orquestados mediante **código tradicional y rutas deterministas predefinidas**. El desarrollador define paso a paso qué se ejecuta y en qué orden; el LLM se limita a procesar cada tarea individual. Son altamente predecibles, rápidos, económicos y fáciles de evaluar y depurar.
* **Agentes (Agents):** Son sistemas donde el LLM **tiene el control de su propio ciclo de ejecución**. El modelo recibe un objetivo, analiza el contexto, decide dinámicamente qué acciones tomar, qué herramientas invocar, evalúa los resultados intermedios y determina cuándo ha terminado. Brindan una enorme flexibilidad en tareas abiertas o con múltiples bifurcaciones imprevistas, pero a costa de mayor latencia, variabilidad en las respuestas y mayor consumo de tokens.

---

## 3. Los 5 Patrones Esenciales de Arquitectura

Anthropic categoriza los patrones de diseño más efectivos, ordenados de menor a mayor autonomía:

1. **Prompt Chaining (Encadenamiento de prompts):**  
   Descompone una tarea compleja en una secuencia lineal fija de pasos. La salida de un LLM pasa como entrada al siguiente, permitiendo validaciones o transformaciones intermedias en código entre cada llamada.
2. **Routing (Enrutamiento):**  
   Un LLM inicial clasifica la entrada del usuario y la envía a la ruta, prompt o herramienta especializada idónea, evitando un único prompt "sabelotodo" saturado de instrucciones incompatibles.
3. **Parallelization (Paralelización):**  
   Ejecuta múltiples llamadas al modelo en paralelo. Se utiliza bajo dos enfoques:
   * *Sectioning:* dividir una tarea grande en subtareas independientes que se ejecutan al mismo tiempo (ej. procesar varias secciones de un documento).
   * *Voting:* generar múltiples soluciones independientes para contrastarlas, verificar consistencia o prevenir alucinaciones.
4. **Orchestrator-Workers (Orquestador y Trabajadores):**  
   Un LLM central (orquestador) descompone dinámicamente el problema en subtareas según lo requiera el caso particular, delega cada una a modelos secundarios (trabajadores) y finalmente sintetiza todas las respuestas en un resultado cohesivo.
5. **Evaluator-Optimizer (Evaluador y Optimizador):**  
   Un bucle iterativo donde un modelo produce una solución (generador) y otro modelo analiza el resultado y genera retroalimentación detallada (evaluador), iterando hasta alcanzar el estándar de calidad requerido (ideal para generación de código y redacción técnica).

---

## 4. Por qué el Diseño de Herramientas es donde más fallan los Agentes

El punto más frágil de un agente no suele ser la capacidad de razonamiento del LLM, sino **la interfaz de las herramientas (tools) que se le proporcionan**. Si las herramientas no están diseñadas pensando en la forma en que los modelos operan, el agente inevitablemente fallará:

* **Ambigüedad en nombres y descripciones:** Si una herramienta no explica con claridad cristalina *para qué sirve*, *cuándo usarla* y *qué formato exacto espera*, el modelo cometerá errores de invocación o adivinará argumentos.
* **Formatos de datos excesivamente complejos:** Diseñar herramientas que exigen parámetros JSON anidados o campos redundantes aumenta drásticamente la tasa de error sintáctico.
* **Errores silenciosos o poco informativos:** Si una herramienta falla y solo devuelve un código genérico (ej. `Error 500`), el agente no tiene información para corregir su rumbo. Los mensajes de error deben ser descriptivos y sugerirle al modelo cómo rectificar.
* **Falta de idempotencia y operaciones destructivas:** Las herramientas con efectos secundarios graves (borrar registros, enviar correos finales) deben contar con confirmaciones explícitas o mecanismos de seguridad (*human-in-the-loop*), ya que un agente iterará y probará diferentes alternativas en su camino hacia la solución.
