<!-- ES -->
# Representación y codificación: del bit al archivo

**D41 · T02–T03.** Amplía M02 y [D26](#/recurso/D26). Estudia primero los ejemplos y después ejecuta la práctica. Al terminar podrás convertir entre bases, distinguir desbordamiento y acarreo, interpretar bytes y calcular tamaños bajo supuestos explícitos.

## 1. La representación necesita un contrato

Una señal analógica varía de forma continua dentro de su modelo; una representación digital utiliza valores discretos. Digitalizar audio requiere muestreo temporal y cuantización de amplitud. Un bit distingue dos valores y un byte contiene ocho bits. El significado de una secuencia depende de su formato: `01000001` puede representar el número 65, la letra ASCII A o parte de una instrucción.

Los prefijos también forman parte del contrato: `1 kB = 1000 B`, `1 KiB = 1024 B`, `1 MB = 1000000 B` y `1 MiB = 1048576 B`. Una tasa en Mbit/s mide bits por segundo; divide entre ocho para obtener MB/s teóricos, antes de descontar sobrecargas. Capacidad, tasa y latencia describen magnitudes diferentes. (S1)

## 2. Bases y aritmética resueltas

Cada posición vale una potencia de la base. En binario, `10101101₂ = 128 + 32 + 8 + 4 + 1 = 173₁₀`. Agrupa desde la derecha: cuatro bits por dígito hexadecimal y tres por dígito octal. Así, `1010 1101₂ = AD₁₆` y `010 101 101₂ = 255₈`. Los prefijos de Python son `0b`, `0o` y `0x`; el valor no cambia al representarlo de otra forma.

Con n bits sin signo representas de 0 a `2^n − 1`. En complemento a dos, el intervalo es `−2^(n−1)` a `2^(n−1) − 1`. Para codificar −5 en ocho bits, calcula `256 − 5 = 251`, es decir, `11111011` o `FB`. El bit superior tiene peso negativo en esa interpretación.

La suma `01111111 + 00000001 = 10000000` produce 128 sin signo, pero −128 interpretado con signo: hay desbordamiento de la suma con signo porque 127 + 1 excede 127. En cambio, `11111111 + 1` necesita nueve bits; conservar ocho deja cero y un acarreo. Acarreo y desbordamiento con signo responden a preguntas distintas. Python usa enteros de precisión arbitraria; la máscara del ejercicio simula un registro de ocho bits y no define las reglas de otros lenguajes. (S2)

## 3. Caracteres, puntos de código y bytes

ASCII define 128 valores. Unicode asigna puntos de código y propiedades; UTF-8 es una codificación de esos puntos mediante secuencias de uno a cuatro bytes. `Añ🙂` contiene tres puntos de código y ocupa siete bytes UTF-8: `41 c3 b1 f0 9f 99 82`. Un carácter visible también puede combinar varios puntos de código: `ñ` y `n` más tilde combinante no tienen necesariamente los mismos bytes.

Antes de comparar textos, declara si comparas bytes, puntos de código o texto normalizado. Un hash distinto puede reflejar distinta codificación o un salto de línea. No demuestra por sí solo una alteración maliciosa. Decodificar bytes arbitrarios como UTF-8 puede fallar; reemplazar errores cambia la información analizada. (S2–S3)

## 4. Multimedia y compresión

Calcula primero una representación sin comprimir y declara canales, profundidad y duración:

| Ejemplo docente | Cálculo | Datos, sin cabeceras |
|---|---|---|
| Imagen 800 × 600, RGB, 8 bits/canal | `800 × 600 × 3` | 1440000 B: 1,44 MB |
| Audio PCM, 48 kHz, 16 bits, estéreo, 10 s | `48000 × 16 × 2 × 10 / 8` | 1920000 B: 1,92 MB |
| Vídeo de esa imagen RGB, 30 imágenes/s, 10 s | `1440000 × 30 × 10` | 432000000 B: 432 MB |

Son estimaciones de muestras, no tamaños garantizados de archivos. Formatos reales añaden metadatos, alineamiento y codificación. La compresión sin pérdida permite recuperar exactamente la entrada; con pérdida descarta información para una representación aproximada. PNG comprime sin pérdida las muestras que codifica. Un JPEG habitual puede perder detalle y un contenedor de vídeo no identifica por sí solo su códec. Comprimir no cifra ni anonimiza. (S4)

## 5. Práctica local: predicción y comprobación

En Bash/zsh con Python 3.8 o posterior y el módulo estándar `zlib` disponible, copia el bloque completo. Trabaja en memoria, sin leer documentos personales ni crear archivos. Predice cada salida antes de ejecutarlo.

```bash
python3 - <<'PY'
import zlib
n = 173
assert int('AD', 16) == int('255', 8) == n
print('bases:', n, format(n, '08b'), format(n, 'o'), format(n, 'X'))
stored = (127 + 1) & 0xff
signed = stored if stored < 128 else stored - 256
assert (stored, signed) == (128, -128)
print('8 bits:', stored, signed)
text = 'Añ🙂'
data = text.encode('utf-8')
assert len(text) == 3 and len(data) == 7
assert data.decode('utf-8') == text
print('texto:', len(text), len(data), data.hex(' '))
original = b'ABCD' * 1024
compressed = zlib.compress(original)
assert zlib.decompress(compressed) == original
assert len(compressed) < len(original)
print('compresion:', len(original), 'bytes; recuperacion exacta')
print('imagen:', 800 * 600 * 3, 'bytes')
PY
```

**Resultado:** bases `173 10101101 255 AD`; enteros `128 -128`; texto `3 7` y los bytes indicados; recuperación exacta de 4096 bytes; imagen de 1440000 bytes. El tamaño comprimido depende de la implementación y no se utiliza como respuesta fija. **Limpieza:** al terminar el proceso desaparecen sus datos de memoria.

## 6. Evidencia y evaluación

Entrega una conversión manual, la explicación del desbordamiento y los tres cálculos multimedia con unidades. Para comprobar transferencia, resuelve `3F₁₆ = 63₁₀ = 77₈` y −1 en ocho bits: `FF`. Explica por qué un archivo pequeño no siempre se comprime más y por qué longitud de texto y bytes difieren. Se evalúan razonamiento y supuestos, además del resultado numérico. Continúa con [lógica digital D42](#/recurso/D42).

<!-- EN -->
# Representation and encoding: from a bit to a file

**D41 · T02–T03.** Extends M02 and [D26](#/recurso/D26). Study the worked examples before running the exercise. You will convert between bases, distinguish overflow from carry, interpret bytes and calculate sizes under explicit assumptions.

## 1. Representation requires a contract

An analogue signal varies continuously within its model; a digital representation uses discrete values. Digitising audio involves sampling time and quantising amplitude. A bit distinguishes two values and a byte contains eight bits. A sequence acquires meaning through its format: `01000001` can represent the number 65, ASCII letter A or part of an instruction.

Prefixes also belong to the contract: `1 kB = 1000 B`, `1 KiB = 1024 B`, `1 MB = 1000000 B` and `1 MiB = 1048576 B`. Mbit/s measures bits per second; divide by eight for theoretical MB/s before accounting for overhead. Capacity, throughput and latency describe different quantities. (S1)

## 2. Worked bases and arithmetic

Each position represents a power of the base. In binary, `10101101₂ = 128 + 32 + 8 + 4 + 1 = 173₁₀`. Group from the right: four bits per hexadecimal digit and three per octal digit. Therefore, `1010 1101₂ = AD₁₆` and `010 101 101₂ = 255₈`. Python uses the prefixes `0b`, `0o` and `0x`; changing representation does not change the value.

An unsigned n-bit value ranges from 0 to `2^n − 1`. Two's complement ranges from `−2^(n−1)` to `2^(n−1) − 1`. To encode −5 in eight bits, calculate `256 − 5 = 251`: `11111011`, or `FB`. The highest bit has a negative positional weight in this interpretation.

The addition `01111111 + 00000001 = 10000000` yields unsigned 128, but signed −128: signed overflow occurs because 127 + 1 exceeds 127. Conversely, `11111111 + 1` needs nine bits; retaining eight leaves zero and a carry. Carry and signed overflow answer different questions. Python has arbitrary-precision integers; the exercise's mask simulates an eight-bit register and does not define another programming language's rules. (S2)

## 3. Characters, code points and bytes

ASCII defines 128 values. Unicode assigns code points and properties; UTF-8 encodes those points in sequences of one to four bytes. `Añ🙂` contains three code points and occupies seven UTF-8 bytes: `41 c3 b1 f0 9f 99 82`. A visible character can combine several code points: `ñ` and `n` followed by a combining tilde need not have identical bytes.

Before comparing text, state whether the comparison concerns bytes, code points or normalised text. A different hash can reflect another encoding or line ending. It does not establish malicious modification. Decoding arbitrary bytes as UTF-8 may fail; replacing errors changes the information being analysed. (S2–S3)

## 4. Multimedia and compression

Calculate an uncompressed representation first, specifying channels, depth and duration:

| Teaching example | Calculation | Data without headers |
|---|---|---|
| 800 × 600 image, RGB, 8 bits/channel | `800 × 600 × 3` | 1440000 B: 1.44 MB |
| PCM audio, 48 kHz, 16 bits, stereo, 10 s | `48000 × 16 × 2 × 10 / 8` | 1920000 B: 1.92 MB |
| Video of that RGB image, 30 frames/s, 10 s | `1440000 × 30 × 10` | 432000000 B: 432 MB |

These are sample-data estimates, not guaranteed file sizes. Real formats add metadata, alignment and encoding. Lossless compression allows exact recovery of its input; lossy compression discards information to obtain an approximate representation. PNG losslessly compresses the samples it encodes. A typical JPEG can lose detail, and a video container alone does not identify its codec. Compression does not encrypt or anonymise data. (S4)

## 5. Local exercise: predict and verify

In Bash/zsh with Python 3.8 or later and the standard `zlib` module available, copy the complete block. It works in memory, without reading personal documents or creating files. Predict each output before running it.

```bash
python3 - <<'PY'
import zlib
n = 173
assert int('AD', 16) == int('255', 8) == n
print('bases:', n, format(n, '08b'), format(n, 'o'), format(n, 'X'))
stored = (127 + 1) & 0xff
signed = stored if stored < 128 else stored - 256
assert (stored, signed) == (128, -128)
print('8 bits:', stored, signed)
text = 'Añ🙂'
data = text.encode('utf-8')
assert len(text) == 3 and len(data) == 7
assert data.decode('utf-8') == text
print('text:', len(text), len(data), data.hex(' '))
original = b'ABCD' * 1024
compressed = zlib.compress(original)
assert zlib.decompress(compressed) == original
assert len(compressed) < len(original)
print('compression:', len(original), 'bytes; exact recovery')
print('image:', 800 * 600 * 3, 'bytes')
PY
```

**Expected result:** bases `173 10101101 255 AD`; integers `128 -128`; text `3 7` and the stated bytes; exact recovery of 4096 bytes; image size 1440000 bytes. Compressed size depends on implementation and is not a fixed answer. **Cleanup:** process termination releases its in-memory data.

## 6. Evidence and assessment

Submit a manual conversion, the overflow explanation and the three multimedia calculations with units. To check transfer, solve `3F₁₆ = 63₁₀ = 77₈` and encode −1 in eight bits: `FF`. Explain why a small file does not always compress further and why text length differs from byte length. Assessment considers reasoning and assumptions as well as numerical correctness. Continue with [digital logic D42](#/recurso/D42).

<!-- COMMON -->
## Fuentes / Sources

- S1. NIST, [Prefixes for binary multiples](https://physics.nist.gov/cuu/Units/binary.html).
- S2. Python Software Foundation, [Built-in types: integers, strings and bytes](https://docs.python.org/3/library/stdtypes.html) y / and [zlib](https://docs.python.org/3/library/zlib.html).
- S3. Unicode Consortium, [UTF-8, UTF-16, UTF-32 and BOM](https://www.unicode.org/faq/utf_bom.html).
- S4. W3C, [Portable Network Graphics specification](https://www.w3.org/TR/png-3/).

Revisión técnica / Technical review: 2026-10-18. Ejemplos y ejercicios propios / Original examples and exercises.
