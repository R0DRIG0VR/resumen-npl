from rouge_score import rouge_scorer

textobase = """"La computación cuántica es un campo de la informática que utiliza los principios de la mecánica cuántica para procesar información de una manera completamente diferente a la computación clásica.

 ¿Qué es la mecánica cuántica?
La mecánica cuántica es la teoría física que describe el comportamiento de la materia y la energía a escalas muy pequeñas, como átomos y partículas subatómicas. A diferencia de la física clásica, donde todo es determinista, en el mundo cuántico hay fenómenos extraños como:

Superposición

Entrelazamiento

Colapso de la función de onda

¿Cómo se aplica esto a la computación?
En la computación clásica, la unidad básica de información es el bit, que puede valer 0 o 1.

En la computación cuántica, la unidad básica es el qubit (bit cuántico), que puede estar en una superposición de 0 y 1 al mismo tiempo.

 Principios fundamentales
1. Superposición
Un qubit puede representar simultáneamente 0 y 1 con ciertas probabilidades. Esto permite a una computadora cuántica explorar muchas soluciones a la vez.

2. Entrelazamiento
Los qubits pueden estar conectados de manera no local. Cambiar el estado de uno afecta instantáneamente al otro, sin importar la distancia.

3. Interferencia
Se utilizan interferencias cuánticas para reforzar las probabilidades de obtener las respuestas correctas y cancelar las incorrectas.

4. Medición
Cuando se mide un qubit, colapsa a un estado clásico (0 o 1). Esto hace que la programación cuántica sea más delicada, ya que medir destruye la superposición.

 ¿Qué ventajas tiene?
Velocidad en problemas específicos: Algunos problemas que tomarían millones de años con supercomputadoras clásicas podrían resolverse en minutos (ej.: factorización, simulaciones químicas).

Simulación de sistemas cuánticos: Como moléculas complejas, lo cual ayuda en medicina, materiales, etc.

Criptografía: Tanto para romperla como para crear nuevos métodos cuánticos más seguros.

 ¿Y en la práctica?
Hoy en día:

Las computadoras cuánticas reales existen, pero son muy limitadas (pocos qubits, ruido, errores).

Empresas como IBM, Google, D-Wave, IonQ y Microsoft están desarrollando hardware cuántico.

Se pueden escribir programas cuánticos con lenguajes como Qiskit (IBM), Cirq (Google), Q# (Microsoft).

 Ejemplo sencillo (intuición)
Un sistema clásico de 3 bits puede estar en un solo estado a la vez:
000, 001, 010, ..., 111 (8 combinaciones).

Un sistema de 3 qubits puede representar todas esas combinaciones a la vez en superposición. Esto no significa que se obtengan todas las respuestas mágicamente, pero sí que se pueden explorar muchos caminos paralelos, acelerando ciertos algoritmos.

¿Te gustaría un ejemplo concreto de código cuántico con Qiskit, o ver cómo se usa en inteligencia artificial o criptografía?"""


resumen = """En la computación cuántica, la unidad básica es el qubit (bit cuántico), que puede estar en una superposición de 0 y 1 al mismo tiempo. La computación cuántica es un campo de la informática que utiliza los principios de la mecánica cuántica para procesar información de una manera completamente diferente a la computación clásica. Un sistema de 3 qubits puede representar todas esas combinaciones a la vez en superposición. A diferencia de la física clásica, donde todo es determinista, en el mundo cuántico hay fenómenos extraños como:

Superposición

Entrelazamiento

Colapso de la función de onda

 ¿Cómo se aplica esto a la computación? La mecánica cuántica es la teoría física que describe el comportamiento de la materia y la energía a escalas muy pequeñas, como átomos y partículas subatómicas. Esto hace que la programación cuántica sea más delicada, ya que medir destruye la superposición.  ¿Y en la práctica? En la computación clásica, la unidad básica de información es el bit, que puede valer 0 o 1. ¿Te gustaría un ejemplo concreto de código cuántico con Qiskit, o ver cómo se usa en inteligencia artificial o criptografía?  ¿Qué es la mecánica cuántica? Esto no significa que se obtengan todas las respuestas mágicamente, pero sí que se pueden explorar muchos caminos paralelos, acelerando ciertos algoritmos.  Ejemplo sencillo (intuición)
Un sistema clásico de 3 bits puede estar en un solo estado a la vez:
000, 001, 010, ..., 111 (8 combinaciones). Esto permite a una computadora cuántica explorar muchas soluciones a la vez. Simulación de sistemas cuánticos: Como moléculas complejas, lo cual ayuda en medicina, materiales, etc.

Criptografía: Tanto para romperla como para crear nuevos métodos cuánticos más seguros."""


scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
scores = scorer.score(textobase, resumen)
print(scores)