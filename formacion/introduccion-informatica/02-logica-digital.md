<!-- ES -->
# Lógica digital: decisiones, circuitos y memoria

**D42 · T04.** Continúa [D41](#/recurso/D41) y conecta las condiciones de M11 con la CPU de [D43](#/recurso/D43). Al terminar construirás tablas de verdad, comprobarás equivalencias y distinguirás circuitos combinacionales de circuitos con estado. La notación booleana utiliza 0 y 1; los circuitos físicos representan esos valores mediante intervalos eléctricos. (S1)

## 1. Puertas y tabla de verdad

AND devuelve 1 cuando ambas entradas son 1. OR lo hace cuando al menos una vale 1. NOT invierte una entrada. XOR, con dos entradas, vale 1 cuando son diferentes. NAND y NOR niegan, respectivamente, AND y OR. El OR de lógica digital es inclusivo; no debe confundirse con «una u otra, pero no ambas».

| A | B | AND | OR | XOR | NAND | NOR |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 |

Para NOT, `NOT 0 = 1` y `NOT 1 = 0`. Una función de n entradas binarias tiene `2^n` combinaciones posibles. Comprobar solo el caso «feliz» no verifica toda la función. Un esquema de cuatro entradas necesita dieciséis filas si se quiere enumerar su comportamiento completo. (S1)

## 2. Álgebra que conserva el resultado

Con A y B booleanos, valen identidad (`A AND 1 = A`), anulación (`A AND 0 = 0`), idempotencia (`A OR A = A`) y doble negación. AND y OR son conmutativos y asociativos; la distribución permite transformar expresiones conservando sus salidas.

Las leyes de De Morgan son especialmente útiles: `NOT(A AND B) = (NOT A) OR (NOT B)` y `NOT(A OR B) = (NOT A) AND (NOT B)`. Al negar, cambian la operación y ambas entradas. Es incorrecto transformar la primera en `(NOT A) AND (NOT B)`.

Ejemplo resuelto: una alarma se activa cuando no se cumplen simultáneamente «sensor disponible» y «lectura válida». Si A=1 y B=0, `NOT(A AND B)=1`. La expresión equivalente también vale 1. La expresión incorrecta anterior daría 0 y ocultaría el fallo. Este modelo es docente; un sistema real debe definir cómo representa un dato ausente o desconocido.

NAND es universal: `NOT A = NAND(A,A)`; negando una NAND obtienes AND; `NAND(NOT A, NOT B)` implementa OR. NOR también permite construir cualquier función booleana combinacional. Universalidad describe capacidad lógica, no eficiencia ni seguridad del circuito. (S1)

## 3. De suma a circuito

Un semisumador combina dos bits: suma `S = A XOR B` y acarreo `C = A AND B`. Para A=B=1 produce C=1, S=0, que representa `10₂`, es decir, dos. Un sumador completo incorpora el acarreo entrante: `S = A XOR B XOR Cin`; el acarreo saliente vale 1 cuando al menos dos de las tres entradas valen 1.

Las señales requieren tiempo para propagarse. Encadenar puertas aumenta el retardo y pueden aparecer transitorios antes de estabilizarse. Una tabla describe la función estable; no contiene por sí sola su comportamiento temporal. Por eso un simulador de expresiones no mide frecuencia máxima ni prueba electrónica real. (S1–S2)

## 4. Combinacional frente a secuencial

En un circuito combinacional, la salida estable depende de las entradas actuales. En uno secuencial interviene también el estado almacenado. Un biestable o flip-flop D ideal captura D en un flanco activo de reloj y mantiene Q entre flancos. Un latch sensible a nivel tiene un comportamiento temporal distinto.

Con Q inicial=0, si D pasa a 1 sin flanco, Q permanece 0. En el flanco de captura, Q pasa a 1; después puede conservar ese valor aunque D cambie. Un registro agrupa varios elementos de memoria. En hardware real se respetan tiempos de establecimiento y mantenimiento; violarlos puede causar metastabilidad. La simulación siguiente modela estados discretos ideales. (S2)

## 5. Práctica: enumerar y contrastar

Ejecuta en Bash/zsh con Python 3. No hay archivos ni conexiones. Calcula primero las cuatro filas y predice los estados del registro.

```bash
python3 - <<'PY'
from itertools import product
print('A B AND OR XOR NAND NOR')
for a, b in product((False, True), repeat=2):
    values = (a, b, a and b, a or b, a != b,
              not (a and b), not (a or b))
    print(*(int(v) for v in values))
    assert (not (a and b)) == ((not a) or (not b))
    assert (not (a or b)) == ((not a) and (not b))
    assert int(a) + int(b) == 2 * int(a and b) + int(a != b)
q = 0
observed = []
for d, rising_edge in [(1, False), (1, True), (0, False), (0, True)]:
    if rising_edge:
        q = d
    observed.append(q)
assert observed == [0, 1, 1, 0]
print('Q:', observed)
print('De Morgan y semisumador: cuatro casos comprobados')
PY
```

**Resultado:** la tabla coincide con la anterior y Q recorre `[0, 1, 1, 0]`. Cambiar D sin flanco no actualiza Q. **Limpieza:** cerrar el proceso libera los datos; no se ha cambiado configuración del equipo.

## 6. Evidencia y evaluación

Entrega la tabla de `(A AND B) OR NOT C`: vale 0 únicamente en `A,B,C = 0,0,1; 0,1,1; 1,0,1`. Dibuja las puertas y marca dónde haría falta memoria para contar eventos. Explica el semisumador con A=B=1 y demuestra una ley de De Morgan mediante las cuatro filas. Se valora distinguir función, estado y tiempo; una tabla correcta no acredita tiempos eléctricos. Continúa con [arquitectura D43](#/recurso/D43).

<!-- EN -->
# Digital logic: decisions, circuits and memory

**D42 · T04.** Continue from [D41](#/recurso/D41) and connect M11's conditions with the CPU in [D43](#/recurso/D43). You will build truth tables, verify equivalences and distinguish combinational circuits from circuits with state. Boolean notation uses 0 and 1; physical circuits represent those values through electrical ranges. (S1)

## 1. Gates and a truth table

AND returns 1 when both inputs are 1. OR does so when at least one is 1. NOT inverts one input. With two inputs, XOR is 1 when they differ. NAND and NOR negate AND and OR, respectively. Digital logic's OR is inclusive; it must not be confused with «either one, but not both».

| A | B | AND | OR | XOR | NAND | NOR |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 |

For NOT, `NOT 0 = 1` and `NOT 1 = 0`. A function with n binary inputs has `2^n` possible combinations. Checking only the successful path does not verify the entire function. Four inputs require sixteen rows to enumerate their complete behaviour. (S1)

## 2. Algebra that preserves results

For Boolean A and B, identity (`A AND 1 = A`), annihilation (`A AND 0 = 0`), idempotence (`A OR A = A`) and double negation hold. AND and OR are commutative and associative; distribution transforms expressions while retaining their outputs.

De Morgan's laws are particularly useful: `NOT(A AND B) = (NOT A) OR (NOT B)` and `NOT(A OR B) = (NOT A) AND (NOT B)`. Negation changes the operator and both inputs. Transforming the first expression into `(NOT A) AND (NOT B)` is incorrect.

Worked example: an alarm activates when «sensor available» and «reading valid» do not both hold. For A=1 and B=0, `NOT(A AND B)=1`. The equivalent expression also returns 1. The incorrect expression above would return 0 and conceal the fault. This is a teaching model; a real system must define how it represents missing or unknown data.

NAND is universal: `NOT A = NAND(A,A)`; negating a NAND gives AND; `NAND(NOT A, NOT B)` implements OR. NOR can also construct any combinational Boolean function. Universality describes logical capability, not efficiency or circuit security. (S1)

## 3. From addition to a circuit

A half-adder combines two bits: sum `S = A XOR B` and carry `C = A AND B`. For A=B=1 it produces C=1, S=0, representing `10₂`, or two. A full-adder includes incoming carry: `S = A XOR B XOR Cin`; outgoing carry is 1 when at least two of the three inputs are 1.

Signals take time to propagate. Chaining gates increases delay, and transients can occur before settling. A truth table describes the stable function; it does not, by itself, specify temporal behaviour. An expression simulator therefore does not measure maximum clock frequency or test real electronics. (S1–S2)

## 4. Combinational versus sequential

In a combinational circuit, the stable output depends on current inputs. A sequential circuit also depends on stored state. An ideal D flip-flop captures D at an active clock edge and holds Q between edges. A level-sensitive latch behaves differently in time.

With initial Q=0, changing D to 1 without an edge leaves Q at 0. At the sampling edge, Q becomes 1; afterwards it can retain this value even if D changes. A register groups several storage elements. Real hardware must respect setup and hold times; violations can cause metastability. The following simulation models ideal discrete states. (S2)

## 5. Exercise: enumerate and cross-check

Run in Bash/zsh with Python 3. No files or connections are involved. Calculate the four rows and predict register states first.

```bash
python3 - <<'PY'
from itertools import product
print('A B AND OR XOR NAND NOR')
for a, b in product((False, True), repeat=2):
    values = (a, b, a and b, a or b, a != b,
              not (a and b), not (a or b))
    print(*(int(v) for v in values))
    assert (not (a and b)) == ((not a) or (not b))
    assert (not (a or b)) == ((not a) and (not b))
    assert int(a) + int(b) == 2 * int(a and b) + int(a != b)
q = 0
observed = []
for d, rising_edge in [(1, False), (1, True), (0, False), (0, True)]:
    if rising_edge:
        q = d
    observed.append(q)
assert observed == [0, 1, 1, 0]
print('Q:', observed)
print('De Morgan and half-adder: four cases verified')
PY
```

**Expected result:** the table matches the earlier one and Q follows `[0, 1, 1, 0]`. Changing D without an edge does not update Q. **Cleanup:** ending the process releases its data; host configuration remains unchanged.

## 6. Evidence and assessment

Submit the table for `(A AND B) OR NOT C`: it is 0 only for `A,B,C = 0,0,1; 0,1,1; 1,0,1`. Draw the gates and identify where memory would be needed to count events. Explain the half-adder for A=B=1 and prove a De Morgan law using all four rows. Assessment rewards the distinction between function, state and time; a correct table does not verify electrical timing. Continue with [architecture D43](#/recurso/D43).

<!-- COMMON -->
## Fuentes / Sources

- S1. MIT OpenCourseWare, [6.004, Combinational logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c2/c2s1/).
- S2. MIT OpenCourseWare, [6.004, Sequential logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c5/c5s1/).
- S3. Python Software Foundation, [itertools.product](https://docs.python.org/3/library/itertools.html#itertools.product).

Revisión técnica / Technical review: 2026-10-18. Ejemplos y ejercicios propios / Original examples and exercises.
