### Proyecto1-TC: Autómatas Finitos a partir de Expresiones Regulares

**Descripción del Proyecto**

Este proyecto implementa algoritmos fundamentales para la construcción de autómatas finitos (AF) a partir de expresiones regulares (ER). El sistema toma como entrada una expresión regular \( r \) y una cadena \( w \). A partir de \( r \), se construye un autómata finito no determinista (AFN), que se transforma en un autómata finito determinista (AFD), luego se minimiza el AFD y, finalmente, se determina si la cadena \( w \) pertenece al lenguaje \( L(r) \).

**Características Principales**

1. **Análisis de Expresiones Regulares**:
   - Utiliza el algoritmo *Shunting Yard* para convertir la expresión regular de notación infija a notación postfija, facilitando la construcción del autómata.

2. **Construcción de Thompson**:
   - A partir de la expresión postfija, se construye un AFN utilizando el algoritmo de Thompson, lo que permite expresar cualquier lenguaje regular.

3. **Construcción de Subconjuntos**:
   - El AFN se convierte en un AFD utilizando el algoritmo de Construcción de Subconjuntos, lo que permite la determinización del autómata.

4. **Minimización de Hopcroft**:
   - El AFD es minimizado utilizando el algoritmo de Hopcroft, haciendo que el autómata sea más eficiente en cuanto a las transiciones de estado, pero manteniendo la capacidad de reconocer el mismo lenguaje.

5. **Simulación de Autómatas**:
   - El programa simula el AFN, AFD y el AFD minimizado con la cadena de entrada \( w \) para verificar si la cadena pertenece al lenguaje definido por la expresión regular.

6. **Exportación a JSON**:
   - Los autómatas (AFN, AFD y AFD minimizado) se exportan en formato JSON para su fácil inspección y uso posterior.

**Cómo Ejecutar el Programa**

1. Ejecuta el programa con el siguiente comando:
   ```bash
   python main.py
   ```
   
2. El programa solicitará:
   - Una expresión regular \( r \).
   - Una cadena \( w \) que será validada contra el autómata.

3. Los autómatas (AFN, AFD y AFD minimizado) serán construidos, impresos y exportados como archivos JSON:
   - `finite_non_deterministic.json`: Autómata Finito No Determinista (AFN).
   - `deterministic_automaton.json`: Autómata Finito Determinista (AFD).
   - `reduced_automaton.json`: Autómata Finito Determinista Minimizado.

4. Los resultados de la simulación se mostrarán en la pantalla, indicando si la cadena \( w \) pertenece a \( L(r) \), junto con los detalles de ejecución para cada autómata.

**Archivos Clave**

- `main.py`: El script principal que coordina todos los componentes y maneja la entrada/salida.
- `thompson.py`: Implementa el algoritmo de Thompson para convertir expresiones regulares en AFNs.
- `subset.py`: Implementa el algoritmo de Construcción de Subconjuntos para transformar AFNs en AFDs.
- `Hopcroft.py`: Contiene la implementación del algoritmo de minimización de Hopcroft para AFDs.
- `ShuntingYard.py`: Convierte expresiones regulares a notación postfija utilizando el algoritmo Shunting Yard.

**Simulación de Autómatas**

El sistema simula los AFNs y AFDs construidos a partir de la expresión regular para evaluar la cadena. Además, genera estructuras de grafos dirigidos para visualizar el AFD minimizado.

---
