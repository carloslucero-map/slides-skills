# Plan: sistema de diseño de slides + recorte de tokens
**wpp-es-html-deck · deck-content-builder · slides_map**

---

## 1. Diagnóstico

**El defecto raíz es de procedencia, no de tamaño.** Los 51 snippets del skill no se trazaron desde las slides reales de MAP: se trazaron desde el PPT template en blanco, con sus páginas de *lorem ipsum*. La propia guía lo confirma en su encabezado — `CORE.md:665`: *"12.15 Composition recipes (mined from the template)"*. La slide 95 del template dice `$2M | Place text here lorem ipsum | 24K | 8%` y encaja exacta con la receta R1; la slide 95 real del banco es una banda y una elipse sin ninguna relación. Solo 3 de 18 recetas citan el banco real.

Todo lo demás se deriva de esa sustitución, y es medible:

| Constante | Lo que dice el skill | Lo que miden las 205 slides reales |
|---|---|---|
| pt → px | `CORE.md:46`: "× 1.5" | 12192000 EMU / 1920 px = 6350 EMU/px → 13,33 in = **960 pt** → **× 2,0**. Toda traducción pt→px va un 25 % corta |
| Borde de contenido | `build_shell.py:608` `--m-edge:80px` | moda del texto real x=**57** (207 hits); el template oficial modea en **39/40** (105 hits); x=80 no aparece en el top-8 |
| Banda de titular | `build_shell.py:636` `top:28px` | los titulares reales arrancan en y≈96–125; el template oficial en y=73 |
| Capacidad | snippet mayor = 670 car. | banco: mediana 494, p75 989; la selección curada del usuario: mediana 665, media 825 → el modelo es **2,4× demasiado fino** |
| Piso tipográfico | 20 px mínimo, FAIL bajo 15 | 36 % de las tiradas reales están bajo 20 px, 15,5 % bajo 15 px. La slide 203: 47 de 54 tiradas a 16 px |

Y hay un agujero de vocabulario: 4 de los 25 target ids que tú mismo escribiste (`comp-matrix-2x2`, `rel-layered-stack`, `rel-taxonomy-columns`, `enum-index-2col`) **no tienen ninguna representación** en el kit — `grep -rli matrix|taxonomy assets/snippets/` devuelve cero. Con las 5 parciales, el 40 % de tu selección curada no está cubierta.

**El segundo defecto: el kit nunca se ha renderizado.** `verify_deck.py` no toca `assets/snippets/` en ninguna línea; hay 0 PNGs por variante. Por eso `stats` acumuló 7 formas no relacionadas (cuarteto héroe, hub-and-spokes, burbujas √, fila de KPIs, scorecard, diagrama de clusters, rampa de intensidad) bajo un solo `data-archetype` sin que nadie lo viera. Tu propio `map_library` dispara 948 frames y falla el build si alguno desborda. Aquí: cero.

**El coste en tokens, medido en disco hoy** (deck de 15 slides = 4 estructurales + 11 de contenido):

```
SKILL.md                33.450 ch =  9.040 tok   siempre
CORE.md                 60.216 ch = 16.274 tok   siempre
SNIPPET-INDEX.md         5.648 ch =  1.526 tok   siempre
sections/ condicionales            ≈ 4.800 tok   (§9 3.018 + §10 722 + §14 1.064)
11 lecturas de variante × 614      =  6.754 tok
─────────────────────────────────────────────
renderer, retrieval                = 38.394 tok
+ emisión del markup al deck       ≈ 5.995 tok de salida
+ deck-content-builder                3.310 tok
```

El 68 % de eso son dos ficheros de prosa. `deck-content-builder` con sus 3.310 tok **no es el problema** — es el 8 % del total y está bien dimensionado. Dentro de SKILL.md, 4.940 tok (55 % del fichero) es procedimiento del paso 4/5 o un manifiesto de recursos que el modelo no puede usar hasta 40 llamadas de herramienta después: es un manual al que le han dado el trabajo de un router.

Dos bombas latentes que cuestan 0 hoy:
- `references/capacity.json` son **11.668 tok** listados en "Bundled resources" (`SKILL.md:497`) entre dos ficheros que al modelo **sí** se le dice que lea, sin marca de "solo scripts". Una lectura equivocada = 30 % del presupuesto de un deck.
- La tabla de `SKILL.md:315-345` nombra ficheros canónicos (`stats.html` = 6.326 tok) mientras la prosa 25 líneas antes dice que abras `variants/` (614 tok de media). Seguir la tabla literalmente en 4 familias cuesta 17.529 tok donde deberían ser 2.456.

---

## 2. La decisión de Figma

**No. Ni ahora ni después, y no como paso intermedio.** Cinco razones, en orden de fuerza:

1. **Ya tienes lo que Figma produciría, con más fidelidad.** `_audit/inventory2.json` son 1.303.733 bytes con cada shape como `{k, nm, box:[x,y,w,h] px sobre 1920×1080, g, ph, fill, ln, rot, p:[{t,sz,b,bu,c}]}` para las 205 slides, grupos ya aplanados, 0,2 % de geometría faltante. Un import PPTX→Figma es un conversor con pérdidas encima de esa misma fuente: reagrupa, rasteriza efectos y te devuelve una copia peor de un fichero que ya consultas con tres líneas de Python.

2. **Nada de Figma llega jamás a un deck.** La regla §2a (`references/sections/2a-self-contained-file-rule-non-negotiable.md`) prohíbe toda referencia externa. Un humano retranscribe a mano lo que salga de Figma — y la transcripción a mano es exactamente el error que produjo el problema actual, reintroducido en el último paso, después de la parte cara, donde es más difícil de detectar.

3. **Convierte tu peor problema en uno insoluble.** Tu propia nota de memoria registra que la guía vive en tres copias mantenidas a mano. Confirmado: `WPP-ES-DESIGN-GUIDELINE.md` es MD5-idéntico a la concatenación de `references/sections/` (`3399394dd2d8e60e50ec14b6ed1545d1`, 104.432 ch en ambos lados). Figma la convierte en cuadruplicación, y la cuarta copia es la única sobre la que **ningún `--check` puede correr**.

4. **Tu propio precedente maduro no tiene Figma.** `map_library` son 45 templates, 158 estados, 6 theme packs, 948 frames verificados — y cero Figma. Funciona.

5. **El 5 % útil de Figma se compra en una tarde.** Lo único que Figma haría genuinamente mejor es *colocar cosas a ojo contra el original*. Eso se llama `canon/_tools/tracer.html`: una página estática de ~150 líneas, un stage de 1920×1080, el PNG de referencia debajo al 40 % de opacidad, tu fragmento HTML encima dentro del CSS real del shell, nudge con flechas, lectura en vivo de x/y/w/h del elemento bajo el cursor, y un toggle que dibuja las cajas de `inventory2` de esa slide como outlines. Verdad al píxel contra la slide real, en el mismo navegador que renderiza el deck, sin paso de exportación y sin segunda fuente de verdad.

**El contrapunto honesto** (y es real): para slides dirigidas por imagen el inventario devuelve casi nada. La slide 14 — la primera de la familia A — tiene 6 shapes, 82 caracteres y **cero tamaños de tipo registrados**. Ahí la geometría no da nada y el PNG lo da todo. Por eso el tracer lleva el PNG debajo: es precisamente el hueco que cierra.

**Única concesión:** si algún día hay que discutir la taxonomía de 8 familias con gente que no abre un terminal, un board de FigJam con los tiles del contact sheet es una hora bien gastada. Es un artefacto de reunión. Nada aguas abajo puede leer de ahí.

**Y la pregunta adyacente — "¿convierto a HTML primero?" — la respuesta es: conviertes el *spec*, no la slide.** Ya se intentó convertir slides: `~/Downloads/MAPslidesSELECCION25.html`, 4,2 MB de Tailwind en un fichero, sin fronteras de template, sin modelo de capacidad, sin nada consultable, y violando §2a de entrada. Bórralo (fase 0) para que nadie lo mine.

---

## 3. Arquitectura objetivo

Cuando esté terminado:

**El canon.** ~30 templates en `wpp-es-html-deck/canon/<id>/`, cada uno con:

```
canon/enum-numbered-4/
  spec.json      # árbol regions/children: roles, repeat, arity, capacityRole.
                 # SIN color, SIN px, SIN copy. approvedBy + approvedAt obligatorios.
  template.html  # el fragmento. Generado o escrito a mano en el tracer, siempre revisado.
  meta.json      # family, form, arity, ground[], density, focal, states, source, useWhen
  measure.json   # la cinta métrica: extraída de inventory2.json para su slide origen
  ref.png        # el original del banco
  preview.png    # el nuestro, disparado por shoot_canon.py
```

**El vocabulario** — nueve ejes cerrados, validados por `canon/_tools/spec_lint.py` y por `verify_deck.py`, documentables en ~300 tok:

- `family` (9): las tuyas — `A-narrative · B-enumeration · C-sequence · D-quantitative · E-comparison · F-relational · G-media · H-entities` + `structural` (cover/agenda/divider/outro, que hoy `verify_deck.py:882 _locked_slide` identifica olfateando el id).
- `secondaryFamily` (mismas, nullable): tú ya nombraste los dos casos, #2 y #12.
- `form` (~23): `columns · numbered · bento · index · steps · phases · timeline · kpi-row · kpi-grid · stat-circles · score-circles · matrix · colour-block · orbit · stack · zones · taxonomy · image-bleed · annotated · card-grid · team-grid · logo-wall · statement · quote`.
- `arity`: `2|3|4|5|6|n`.
- `ground` (4): `cream|white|tint|navy` — **declarado y disparado, nunca asumido**. `build_shell.py:801` ya trata la furniture a blanco sobre paneles navy: eso es evidencia directa de que cambiar el fondo rompe cosas.
- `density` (3): `airy ≤350 · standard 350-750 · dense 750-1250` caracteres netos, bandas medidas sobre la selección curada (mediana 583, p75 1003).
- `mediaRole` (5): `none|motif|photo|screenshot|logo`.
- `focal`: qué rol lleva el momento display y su ratio contra el cuerpo. **Este eje no estaba en ninguna propuesta y hace falta**: las slides 86 y 103 son misma familia, misma forma, aridad contigua, densidad parecida — y compositivamente opuestas. 86 tiene el numeral a 192 px sobre un titular alineado a izquierda (ratio 3,0); 103 tiene el numeral a 32 px como etiqueta bajo un titular centrado (ratio 0,5). Ningún eje de esqueleto las distingue.
- `source`: `bank:<n>[,<n>] | tpl:<n> | synth`, resoluble en `inventory2.json` y comprobado en CI. Hoy 37 de 51 filas no citan fuente alguna.
- `states`: `ideal | max` (+ `min` donde colapsa al quedarse corto). `max` es tu `test-brutal`: la rotura barata deliberada.

**Cómo se construye un deck.** El modelo lee `SKILL.md` (router, ~3.400 tok) + `BRAND.md` (lo que sobreviva de CORE) + `CATALOG.md` (≤1.600 tok, tope asertado en CI). Elige por `useWhen` — una frase que nombra el problema, no la construcción — abre **un** fragmento por slide, lo rellena, corre `check_capacity.py` y `verify_deck.py`, hace el pase de arte mirando el contact sheet. Lo que ya no lleva en contexto: el esqueleto CSS (`build_shell.py` lo emite), las recetas de composición (el canon *es* el recetario, y una receta que pegas gana a una receta que sigues), las 17 constantes de la tabla §4.3 (pasan a custom properties), y el paso de relleno completo (vive en `references/FILL.md`, disparado tras `build_shell.py`).

**Lo que el skill sigue llevando y no se toca:** la sección STOP / gate de plan (`SKILL.md:33-63`, 522 tok) — es la prosa de más valor del fichero y nombra su propio modo de fallo; §15.3 alineación y §15.4 aritmética de encaje — dan forma a la clase y al tamaño que eliges *antes* de que exista DOM, y el verificador solo los marca como WARN; NN7 (el nombre es *WPP Enterprise Solutions | MAP*, nunca *VML MAP*) y los cinco defaults bloqueados de NN2 — un grep confirma que CORE no los tiene.

---

## 4. Plan por fases

### Fase 0 — Higiene y la espina dorsal (medio día)

**Qué se construye.** Cuatro ediciones y un fichero.

1. `SKILL.md:497` → `**references/capacity.json** — SCRIPT INPUT ONLY, nunca lo leas; ~11.700 tokens. check_capacity.py lo lee por ti.` Misma marca para `assets/exemplars/` y `assets/photos/`.
2. `SKILL.md:315-345` → sustituir en todas las filas `stats.html V5` por `variants/stats-v5.html`. `SKILL.md:290-291` → prohibición dura: *"Nunca abras `assets/snippets/*.html` en tiempo de relleno — son la fuente de autoría; el deck lee solo `variants/`."* Y en `check_capacity.py`, aserción de que toda fila de `SNIPPET-INDEX.md` resuelve a un `variants/` existente (si no, un `--split` fallido deja el kit inalcanzable).
3. `rm ~/Downloads/MAPslidesSELECCION25.html`.
4. `canon/_ref/manifest.json` — 25 filas `{page, original, family, targetId, rag, notes}` transcritas **a mano** desde `SELECCION-25-indice.md`, más `canon/_tools/check_join.py`, que prueba la unión página↔slide comparando por fuzzy el texto de la página del PDF contra las tiradas de `inventory2` y falla cualquier fila bajo 0,6.

**Verificación.** `check_join.py` en verde para las 25 filas. Un deck de prueba que no abre ningún `.html` canónico.

**Esfuerzo.** 4 h.

**Si paras aquí:** ~2.000 tok/deck recuperados del defecto de rutas, una cola de riesgo de 11.668 tok eliminada, un callejón sin salida de 4,2 MB borrado, y la unión que sostiene todo lo demás demostrada mecánicamente.

---

### Fase 1 — Ver lo que ya tienes (1–2 días)

**Qué se construye.** `wpp-es-html-deck/scripts/shoot_snippets.py`: por cada variante, genera un spec de una slide, corre `build_shell.py --spec --out`, empalma el fragmento sobre el placeholder de `.content-band` (`build_shell.py:402 content_placeholder`) y captura a 1920×1080. Reutiliza tal cual `verify_deck.py:92 _find_chrome`, `:887 _geo_capture`, `:992 _geo_violations` y `:588 build_contact_sheet` — los cuatro existen y Chrome está instalado en `/Applications/Google Chrome.app`.

Salidas: `canon/_shots/<id>.png` × 51 (~2,5 MB en total; los exemplars del propio skill pesan 33–70 KB cada uno, así que la alarma de git-LFS de la auditoría es falsa) y un contact sheet por archetype.

**Primera aserción**, tomada de una promesa que el skill ya hace por escrito y nunca ha probado — `CORE.md §12.15`: *"la primera variante de cada snippet es una receta a canvas completo; pegarla sin modificar debe pasar §12.15a"*. Dispara esas 13 y corre C2 (mitad inferior muerta) contra ellas.

**Aterriza como WARN, no FAIL.** Varias violarán §15 el primer día; si bloquea, se apaga el gate y se acabó.

Aquí se crea `.github/workflows/` — el repo no tiene ninguno hoy.

**Verificación.** El script sale distinto de cero ante desbordamiento horizontal. Tú lees los contact sheets.

**Esfuerzo.** 1,5 días.

**Si paras aquí:** por primera vez puedes *ver* el kit. Sabrás cuáles de los 51 sobreviven y cuáles son ruido — es conocimiento irreversible, y no puedes des-ver que hay siete formas distintas escondidas bajo `stats`. Además el repo tiene CI.

---

### Fase 2 — Cirugía de tokens (4–5 días, en paralelo con todo)

**Esta fase se adelanta a propósito.** El plan que ganó la evaluación agregada la ponía en el paso 6 de 7, a cinco semanas vista. Es su fallo: es el único ahorro del proyecto con **cero dependencia** de que el canon funcione, y retenerlo seis semanas es seis semanas de decks pagando la tarifa completa a cambio de nada. La tabla completa está en §5.

Lo estructural dentro de esta fase:

- **`scripts/build_docs.py`** — un manifiesto, **dos** salidas (`CORE.md` y el master `WPP-ES-DESIGN-GUIDELINE.md`, emitido a un `build/` gitignoreado), un solo `--check`, cableado en `verify_deck.py` como `check_docs()`. Confirmado por MD5 que el master ya es un producto de build mantenido a mano. Si el gate cubre CORE pero no el master, el master deriva en silencio en la siguiente edición de sección y la triplicación que registra tu memoria vuelve con un `--check` que prueba la mitad equivocada. Y quita el lenguaje de arbitraje en `SKILL.md:86`, `:501-502`, `CORE.md:4` y `:21` que invita a una lectura de 28.645 tok.
- **Partir `sections/12-slide-archetype-library.md`** en `12-archetypes.md` (§12.0–12.13 + §12.16) y `12-composition.md` (§12.14/12.15/12.15a). Abrir el fichero hoy recarga 2.861 tok que CORE ya puso en contexto — el 37,6 % del fichero es duplicado garantizado.
- **Acuñar el `id` en `derive_capacity.py:344 write_index_and_variants`** (`{stem}-{vtag}` → `boxes-v1`, `stats-v3`), escrito en la misma pasada al registro de capacidad, a la etiqueta de apertura del fragmento como `data-template=` y al meta. Hoy los 51 registros de `capacity.json` comparten solo 13 valores de `file` y se discriminan por un `label` de texto libre. Propagarlo por `build_shell.py:404`. `check_capacity.py` prefiere el registro exacto y cae al comportamiento actual (el más permisivo) cuando falta, para que las slides a medida no den falsos positivos.
- **Números de línea**: `check_capacity.py` y `verify_deck.py` imprimen `deck.html:<línea>` junto a cada slide marcada — el `HTMLParser` ya rastrea `getpos()`. El bucle de corrección pasa de una lectura del fichero completo (862 líneas, 640 KB) a `Read deck.html offset=<línea> limit=40`. Enseña también que la línea es una pista a confirmar contra `data-slide-id` en la ventana devuelta, no una coordenada de fiar.

**Verificación.** `build_docs.py --check` en verde; un deck de regresión sobre una narrativa cruda y otro sobre un fichero aprobado de `deck-content-builder`, confirmando que ambos siguen parando en el gate de dirección antes de cualquier `build_shell.py` (el recorte del gate de plan es el de más riesgo de toda la tabla).

**Esfuerzo.** 40 h ≈ 5 días.

**Si paras aquí:** −9.227 tok/deck (24 %), la triplicación terminada mecánicamente, el bucle de corrección de desbordamiento de ~1.940 a ~800 tok. Y sigues con el kit viejo, que es exactamente lo que tienes hoy: no has empeorado nada.

---

### Fase 3 — Las constantes del marco, en un commit (2–3 días)

**Va después del disparo y antes de autorar.** Antes del disparo no tendrías el before/after con que revisar el reflow; después de autorar habrías construido 30 templates sobre una constante mala y un generador propaga una constante mala a 30 templates en vez de a 1.

Un solo commit tocando `CORE.md` §2/§4.5/§15.1, los tokens de `:root` en `build_shell.py:608`, y la constante §15.9.1 de `verify_deck.py`:

- **`px = pt × 2`** en `CORE.md:46`. Verificable de forma independiente desde EMU: 12192000/1920 = 6350 EMU/px = 144 px/in; 13,33 in × 72 = 960 pt; 1920/960 = 2,0. No admite discusión.
- **El borde de contenido — aquí los evaluadores no coinciden y la decisión es tuya.** Lo único inequívoco es que **80 está mal**: los dos candidatos son aproximadamente la mitad. Las dos posiciones:
  - **x=40** — es la moda del template oficial (105 ocurrencias de 39/40), está sobre el módulo de 40 px que ya usas (`--grid:40px`), y según la auditoría el playbook de marca lo dice literalmente. *Esa última afirmación no está verificada con una cita literal en ninguna parte del expediente.*
  - **x=57** — es la moda del texto real del banco (207 hits; el siguiente valor no-canaleta es 113 con 50), es el leftmost por slide en 47 slides, y es la x del titular en 12 de las 24 slides medibles de tu selección curada. Es lo que los diseñadores de MAP hicieron de verdad.
  - **Regla de decisión, 10 minutos:** abre `WPP Enterprise Solutions Guidelines_0.2JULY2026.pdf` y busca la línea. **Si el playbook dice 40 literalmente, ve a 40** — es simultáneamente marca-declarado, template-modal y modular, y expresas la práctica de MAP como un `--m-text:56px` opcional para slides densas de texto. **Si no lo dice, ve a 57**, porque la moda de 40 se midió sobre *placeholders*, y preferir el placeholder al contenido real es literalmente el error que causó todo este problema.
- **Banda de titular** de y=28 a y=73, y **suelo de contenido** de 960 a 1020 **en el mismo commit** — si no, encoges la banda 97 px.
- **Piso tipográfico.** Añade un nivel de referencia declarado a **16 px** (no 14) sobre una **lista cerrada de clases**: etiqueta de celda de matriz, hoja de taxonomía, etiqueta de banda de stack, segundo nivel actividad/entregable, etiqueta de categoría de logo-wall. `verify_deck.py` **FALLA** cualquier elemento bajo 20 px que no lleve una de esas clases. 16 es la moda del segundo nivel en las tres slides que motivan el cambio (203 = 47 tiradas a 16 px, 129 = 43, 32 = 33); solo la 175 necesita 14, y esa se rediseña en vez de acomodarla. Prosa libre a 16 px tiene que ser mecánicamente imposible, no desaconsejada.
- **Sube C4** de "≤2 escalas de texto" a "≤3 + 1 momento display". La mediana real de la selección curada son 4 tamaños distintos por slide (7 en las 189 y 148). Con ≤2, un canon trazado honestamente falla su propio criterio en 21 de 24 slides.
- **§4.3 → custom properties** (`--fs-*`, `--lh-*`, `--tr-*`). Edita los **13 ficheros canónicos** de `assets/snippets/`, nunca los 51 de `variants/` (se regeneran). Y **sube los tamaños a clases del shell**, no los cambies por `style="font-size:var(--fs-x)"` — hay 233 literales inline y `var()` es ~12 caracteres más largo cada uno, lo que engordaría cada fragmento ~195 tok/deck. Decide la exención de `stats-v3` (68 px/46 px son proporcionales al dato, no pasos de escala) **antes** de empezar, no durante.

**Verificación.** Re-disparo completo con `shoot_snippets.py` y diff de contact sheets contra la línea base de la fase 1. Un cambio de rejilla mueve todo; la fase 1 existe para que ese diff sea revisable.

**Esfuerzo.** 2,5 días + medio día mirando qué se movió.

**Si paras aquí:** todos los decks están sobre la rejilla real, y cualquier medición futura es fiable. Es la fase que hace que trazar valga la pena.

---

### Fase 4 — Un template de punta a punta, y el tracer (3–4 días)

**Antes de construir infraestructura para 30, camina uno.** El error que evita: dibujar 51 `meta.json` mecánicamente y descubrir que el esquema está mal en los 51.

1. `pdftoppm -r 144 -png "/Users/carlos/Desktop/slides_map/MAP_slides_SELECCION_25.pdf" canon/_ref/slide` → 25 PNGs a 1920×1080 en menos de un minuto (`pdftoppm` está en `/opt/homebrew/bin`; **`soffice` NO está instalado**, así que renderizar el pptx de 640 MB no es una opción sin una instalación — y no hace falta, el PDF de la selección ya está en disco a 13,5 MB. `MAP_PPTTemplate_v2.pdf` también, si quieres el template oficial).
2. `canon/_tools/measure.py` → `canon/<id>/measure.json` desde `inventory2.json`: bordes izquierdos de shapes de texto, paso de columna detectado, tamaños px distintos (a pt×2), caracteres netos sobre y=985, conteo por tipo de shape, cajas de imagen. **Con el stripper de furniture aplicado primero**: cajas cuya box exacta aparece en ≥20 slides son mobiliario — el detector aísla limpiamente los dos logos (146 y 144 slides), el número de página (81) y ocho marcas de registro (59 cada una), y baja la mediana de shapes por slide de 31 a 17. Medir sin limpiar es medir ruido. De regalo, `canon/_ref/furniture.json` te da la especificación medida de la banda de pie que el shell dibuja a mano hoy.
3. `canon/_tools/tracer.html`, como se describe en §2.
4. Camina la fila 3 / slide original 86 (VERDE, 15 shapes, 483 car., titular en x=61, cuerpo en x=57, enumeración numerada limpia): `measure.json` → escribir `spec.json` a mano → construir `template.html` en el tracer hasta que superponga → `meta.json` (con `useWhen` **a mano**: el esquema de `map_library` dice por qué — generado desde los otros campos degenera en el mismo boilerplate que ya lleva la descripción) → disparar → fila de catálogo.
5. **Escribe qué reveló el paseo como faltante.** Ese documento es el input de la fase 5.

**Verificación.** `spec_lint.py` valida vocabulario y roles, nunca estructura (esa es la puerta humana). `shoot_canon.py` empalma y dispara. Tú superpones `preview.png` sobre `ref.png`.

**Esfuerzo.** 3,5 días.

**Si paras aquí:** tienes el instrumento (que sirve para siempre), 25 PNGs de referencia, la cinta métrica automatizada, y un template medido y revisado en el kit. Y sabes si el proceso es sostenible antes de comprometer un mes.

---

### Fase 5 — El canon, VERDE primero (3–4 semanas, incremental)

Repite el paseo, medio día por template, en orden RAG. Los 11 VERDE primero (originales 86, 73, 44, 203, 74, 37, 27, 151, 148, 2, 36) porque validan el proceso barato; luego los AMARILLO, donde muerden tus notas de rediseño; los cuatro sin vocabulario **los últimos** (32 → `comp-matrix-2x2`, 175 → `rel-layered-stack`, 157 → `rel-taxonomy-columns`, 58 → `enum-index-2col`), porque la 175 son 188 shapes y 1.955 caracteres y va a romper el modelo de capacidad y el piso tipográfico — quieres esos modelos asentados por 20 templates previos antes de encontrártela.

**Tus notas de rediseño se aplican como decisiones de spec, registradas donde son auditables:**
- **#13 (orig. 189)** → forma declarada `score-circles`: círculos de diámetro fijo donde el diámetro **no codifica nada** y el número es el dato. Legal precisamente porque no se reclama codificación. **No hagas condicional la ley del √**: mantenla obligatoria para toda forma que declare codificación por tamaño, y que `verify_deck.py` compruebe la forma declarada contra el bloque de datos — una forma con codificación cuyos diámetros no casan con √valor FALLA; una `score-circles` cuyos diámetros no son todos iguales FALLA. Ambas condiciones son mecánicamente comprobables; un umbral de ratio no lo es.
- **#10 (orig. 65)** → gana el eje temporal que falta, conserva la banda inferior a todo el ancho.
- **#8 (orig. 203)** → pierde los chevrons como ornamento, pero su segundo nivel Activities/Deliverables lo salva el nivel de referencia de 16 px de la fase 3, no una excepción de ornamento. Aparte: añade una cláusula a `CORE §1.3` diciendo que la prohibición de ornamento cubre reglas decorativas y barras de acento, **no** los conectores funcionales de §5.
- **#25 (orig. 36)** → conserva las etiquetas de categoría a la izquierda.

**Tres correcciones a la propuesta original que vienen de los evaluadores:**

- **`matrix`, `layered-stack` y `taxonomy` NO son fragmentos de aridad fija — son generadores parametrizados** (`--rows 3 --cols 4`). La slide 32 son 37 roundRects + 29 rects + 2 conectores; la 175, 188 shapes con 49 conectores. Son diagramas construidos, no placeholders rellenables. Un fragmento a mano con una sola aridad no sobrevive al segundo deck que necesite un 3×3.
- **No borres CORE §5 (vocabulario de formas) — extiéndelo.** Los tres candidatos lo reubicaban o lo borraban, y los tres se equivocan: el lenguaje de formas es buena parte de lo que hace reconocibles a estas slides, y ninguno de los ejes `form` lo lleva. Medido sobre las 25 curadas: donut+arc (27), leftBrace (189), chevron y homePlate como **contenedores** de paso (203), flowChartAlternateProcess (175), round2SameRect (143), straightConnector (32/129/143). Los siete valores actuales de §5 incluyen `bracket` pero no donut, arc ni contenedor-banda.
- **No retires los 51 variants por bloque.** Un variant sale de rutas solo cuando una entrada de canon cubre su `family+form+arity`. Retirar 51 para poner 30 encoge la cobertura y hace que `FREEHAND.md` dispare más — y eso es un bucle de realimentación al alza sobre el coste por deck.

**Las reglas de crecimiento, codificadas en CI, no escritas en un README:**
1. **Cupo de familia** — un template que declare un `family+form+arity+density` ya existente se rechaza; extiendes los `states` del existente. Esto es exactamente lo que impide que `stats` vuelva a acumular siete formas.
2. **Procedencia o nada** — `source` debe resolver en `inventory2.json`; `synth` exige justificación escrita en `spec.json` y firma.
3. **Anclado a su original** — `ref.png` junto a `preview.png`; un diff de preview no aprobado falla CI (con tolerancia y versión de Chrome fijada, o la gente aprende a aprobar diffs sin mirar).
4. **Presupuesto de tokens, no de filas** — `CATALOG.md` topado en 1.600 tok, asertado en el build. Un template nuevo que rompa el tope obliga a acortar una fila o a retirar un template.
5. **Retiro** — el build escribe `lastUsed`; 12 meses sin uso y sin ser la única entrada de su familia a esa aridad → `canon/_attic/`, nunca borrado.
6. **Toda slide freehand es candidata** — cuando `FREEHAND.md` dispara, se registra. Una forma que dispara tres veces se gana un spec. **Así se minan las otras 180 slides: por demanda, nunca por clustering.**

**Verificación.** `shoot_canon.py` en verde (promovido de WARN a FAIL cuando el canon esté limpio) + tú leyendo los contact sheets con el original al lado. `approvedBy`/`approvedAt` en `spec.json`, y `codegen` se niega a construir sin ellos: una puerta humana que se salta es peor que ninguna puerta, porque deja el fichero con aspecto de revisado.

**Esfuerzo.** 3–4 semanas, una persona, no paraleliza (el valor es un ojo aplicado consistentemente).

**Si paras aquí (en cualquier punto):** tienes N templates medidos, renderizados y revisados, conviviendo con los 51. Cada medio día añade uno usable. Es la única fase del plan cuya unidad de trabajo es una cosa terminada.

---

### Fase 6 — El catálogo generado (1 semana)

`canon/_tools/derive_canon.py` emite tres vistas de una sola fuente: `references/CATALOG.md` (la superficie de elección, ≤1.600 tok, ocho secciones por familia, una línea por template), `references/catalog.json` (family/form/arity/density/capacity/source/focal — solo lo lee el paso de planificación) y `canon/gallery/index.html` (los mismos registros con su `preview.png` inline, para que el catálogo visual y el textual no puedan discrepar). `--check` regenera en memoria y sale distinto de cero ante deriva.

**El presupuesto se mantiene sustituyendo, no añadiendo**: `useWhen` reemplaza la columna "qué es". Hoy 22 de 51 filas truncan a mitad de palabra (`derive_capacity.py:341 desc[:64]`, `:339 label[:60]`, `:385`) — `cards-v1` acaba en *"one card expand"*, `stats-v3` corta *"NEVER one dominant centr"* a mitad de una prohibición. Arregla las tres cortes uniendo las dos primeras líneas del comentario antes de normalizar, y luego quita los slices.

**Migración de `data-archetype` a los ejes cerrados: cuatro puntos de llamada, no dos** — el matcher de `check_capacity.py`, `verify_deck.py:554` (ritmo), `verify_deck.py:735` (el suavizador de mitad-inferior-muerta para statement/quote, que es otro check), y `build_shell.py:404` (el emisor). Y **el check de ritmo C6 se indexa por `form`, no por `family`**: su propio comentario en `verify_deck.py:509-511` dice que persigue igualdad visual, y dos slides de enumeración en formas distintas no son repetitivas. El matcher de capacidad sí va por `family`+`form`.

**Si paras aquí:** el modelo elige por problema en vez de por nombre de clase CSS, y el coste del catálogo es fijo por construcción.

---

### Fase 7 — El segundo corte de CORE, con puerta (2–3 días, condicionado)

**Solo después de que la instrumentación lo pruebe.** Desde el primer deck construido sobre el canon, registra por slide: `matched` / `unmatched` / `hand-edited`. Diez decks son el punto de decisión. Si el canon cubre ≥8 de 11 slides de contenido, borras:

- **§13.1 Skeleton (780 tok)** — `build_shell.py` lo emite y nada se ensambla a mano.
- **§12.15 recetas de composición (1.614 tok)** — el canon *es* el recetario, con preview.

Total ≈ 2.294 tok. **Y nada más.** Aquí discrepo del plan ganador, y el evaluador de economía tiene razón: su propuesta de bajar CORE de 16.274 a 4.500 no cuadra. Su lista de borrado suma ~4.179, no ~6.900, y deja CORE en ~12.100; los 7.600 restantes están afirmados, no derivados. Concretamente, **§15 no se puede borrar**: mientras el modelo siga rellenando fragmentos a mano en tiempo de deck, §15.3 (alineación) y §15.4 (aritmética de encaje) siguen dando forma a la clase y al tamaño que elige antes de que exista DOM, y `shoot_canon.py` solo ve copy de placeholder en tiempo de build de librería — nunca el copy real, las fotos ni los campos de puntos del deck. **§12.14 son guardarraíles, no recetas.** **§3.8** (qué color significa positivo) es política que ninguna custom property codifica.

**Si paras aquí:** CORE en ~11.700, y sabes por medición —no por esperanza— que el canon cubre.

---

### Fase 8 — `render_slide.py` (opcional, con go/no-go duro)

La idea: un script lee el fragmento y escribe la `<section>` rellena en el deck; el modelo solo produce `slots.json` (~130 tok/slide). Eliminaría a la vez las 6.754 tok de lectura y las ~5.995 de emisión.

**No la construyas sin medir primero.** Coge cinco decks entregados, extrae a mano su `slots.json` y mide qué fracción rellena limpiamente. **Si es <70 %, no la construyas** — recorta a un linter que valide slots. Dos razones para dudar: (a) la propia auditoría de retrieval midió que el 82 % de una lectura de variante es markup que el modelo tiene que emitir de todos modos, lo que deja el techo en ~1.441 tok/deck si solo cuentas lectura; (b) el relleno por slots asume un esqueleto fijo con carga de texto variable, y eso es falso exactamente para las formas que más quieres (matrix, layered-stack, taxonomy: son diagramas construidos). Y necesita escotilla declarada (`--emit` a stdout para editar a mano), porque el pase de arte C1–C7 es visual y su repertorio de arreglos no puede estrecharse a valores de slot.

---

## 5. Optimización de tokens

Ordenado por tokens ahorrados por hora de trabajo. Todo son cifras medidas en disco, no proyecciones.

| # | Cambio | tok/deck | Horas | tok/h | Riesgo |
|---|---|---|---|---|---|
| 1 | Rutas de snippet `SKILL.md:315-345` → `variants/` + prohibición dura en `:290` + aserción en `check_capacity.py` | **2.000\*** | 1,0 | 2.000 | bajo |
| 2 | Partir `sections/12` en `12-archetypes.md` + `12-composition.md` (2 ediciones de ruta) | **1.500** | 1,0 | 1.500 | bajo |
| 3 | **Fase 7**: borrar CORE §13.1 + §12.15 (condicionado al canon) | **2.294** | 3,0 | 765 | alto sin canon |
| 4 | Borrar "Bundled resources" `:489-538` (reubicar 3 cosas: rutas de fotos duotonadas, comando de regeneración, `assets/textures/`) | **780** | 1,5 | 520 | medio |
| 5 | Borrar tabla "Locked vs free" `:123-141` (guardar §14 motion y §13.4 como NN 9 y 10) | **390** | 0,75 | 520 | medio |
| 6 | Borrar historial de versiones `:19-32` + `:473-474` → `CHANGELOG.md` (ya existe) + arreglar puntero obsoleto de REVISING | **244** | 0,5 | 488 | ninguno |
| 7 | CORE §2a/§6/§13.1/§3.7/§3.6/§3.8 → ficheros condicionales **propios y pequeños** (no dentro de `sections/3` ni `sections/13`) | **2.777** | 6,0 | 463 | medio-alto |
| 8 | Variants: bloque `capacity` de una línea + quitar banner + `.gitattributes linguist-generated` + `variants/README.md` | **1.441** | 4,0 | 360 | bajo |
| 9 | Borrar restatement de §15 en `SKILL.md:360-376` + comprimir non-negotiables (**conservar NN2 y NN7 enteros**) | **620** | 2,0 | 310 | medio |
| 10 | Paso de relleno → `references/FILL.md` (solo lo post-shell: `:346-352`, `:353-359`, `:377-388`) con disparo explícito "después de `build_shell.py`" | **300** | 1,0 | 300 | medio |
| 11 | Ejemplo de `spec.json` `:251-270` → `references/SPEC.md` (**los enums se quedan**, G1 los imprime) | **150** | 0,5 | 300 | bajo |
| 12 | Gate de plan: borrar `:201-205`, reducir `:233-236` a una línea (**conservar `:33-63` intacto**) | **144** | 0,5 | 288 | **ALTO** — test de regresión obligatorio |
| 13 | CORE §13.2 borrado + §11 divider recortado en sitio | **435** | 1,5 | 290 | bajo |
| 14 | CORE §4.5↔§15.10 fusionados, §15.9.2 y escotilla §15.2 → punteros de una línea | **290** | 1,5 | 193 | bajo |
| 15 | CORE dedup interno (los 6 restatements más débiles) | **230** | 3,0 | 77 | medio |
| 16 | `capacity.json` / `exemplars/` / `photos/` marcados SCRIPT INPUT ONLY | 0\*\* | 0,25 | — | ninguno |
| 17 | `data-template` acuñado + `deck.html:<línea>` en ambos scripts | 0\*\*\* | 3,0 | — | bajo |
| 18 | `CATALOG.md` sustituye `SNIPPET-INDEX.md` (`useWhen` **reemplaza** la descripción; tope 1.600 en CI) | ~0 | 10,0 | 0 | medio |

\* No es ahorro sostenido: la línea base ya asume que abres `variants/`. Es un defecto que cuesta hasta 2.000 tok/deck cuando la tabla te manda al canónico (`stats.html` = 6.326 tok).
\*\* 0 sostenido; elimina una cola de riesgo de 11.668 tok — el 30 % del presupuesto de un deck — si el modelo lo lee una vez. Es la edición de mayor ROI del proyecto.
\*\*\* 0 en retrieval; baja el bucle de corrección de desbordamiento de ~1.940 a ~800 tok por slide afectada.

### Aritmética honesta, deck de 15 slides (4 estructurales + 11 de contenido)

```
                          HOY        Tras Fase 2      Tras Fase 7
SKILL.md                 9.040          6.412            6.412
CORE.md                 16.274         12.542           10.248
SNIPPET-INDEX / CATALOG  1.526          1.526            1.600
sections/ condicionales  4.800          3.300            3.300
11 lecturas de variante  6.754          5.313            5.313
─────────────────────────────────────────────────────────────
renderer, retrieval     38.394         29.093           26.873
                                       −24,2 %          −30,0 %

+ deck-content-builder   3.310          3.310            3.310
dos skills, total       41.704         32.403           30.183
                                       −22,3 %          −27,6 %
```

**Tres cosas que esta tabla no dice y deberías saber:**

1. **El titular de 58 % del plan ganador no sobrevive a la recomputación.** Su línea que lo sostiene —CORE de 16.274 a 4.500— se apoya en una lista de borrado que suma ~4.179, no ~6.900. El número defendible es 30 %, no 58 %. Prefiero dártelo así que verte descubrirlo en la semana cinco.
2. **No se cuentan las ~5.995 tok de *salida* que cuesta emitir el markup al deck.** Solo desaparecen si un script hace la emisión — fase 8, y solo si la medición de fill-rate la autoriza. En una tarifa real, salida cuesta 3–5× entrada, así que si esa fase pasa la puerta es el mayor ahorro individual que queda.
3. **La extracción no ahorra un token y el recorte no arregla un layout.** Son dos hilos. Manténlos separados en revisión: es como uno acaba justificando al otro.

---

## 6. Lo primero que hacer

**Una sesión, 60–90 minutos, tres ediciones en `wpp-es-html-deck/SKILL.md` y una en `check_capacity.py`.** Útil aunque nada más de este plan ocurra nunca.

```bash
cd /Users/carlos/Desktop/map/map_projects/slides_skills
git checkout -b tokens/first-cut
```

1. **`SKILL.md:497`** — sustituir la línea de `capacity.json` por:
   `**references/capacity.json** — SCRIPT INPUT ONLY, never read it; ~11,700 tokens. check_capacity.py reads it for you.`
   Añadir la misma marca a `assets/exemplars/` y `assets/photos/` en esa lista. Borrar el paréntesis de `SKILL.md:296` que lo ofrece como fuente alternativa. Y en `derive_capacity.py:370`, quitar `and in references/capacity.json` de la cabecera generada de `SNIPPET-INDEX.md`.

2. **`SKILL.md:315-345`** — find-replace mecánico en las 31 filas: `stats.html V5` → `variants/stats-v5.html`, etc. Cero cambio neto de tokens, cero riesgo.

3. **`SKILL.md:290-291`** — sustituir por la prohibición dura:
   `Never open assets/snippets/*.html at fill time — they are the authoring source; the deck reads variants/ only.`

4. **`check_capacity.py`** — aserción nueva: toda fila de `SNIPPET-INDEX.md` resuelve a un fichero existente en `assets/snippets/variants/`. Sin esto, un `--split` fallido deja variantes inalcanzables y la prohibición del punto 3 es irrecuperable.

5. **`rm ~/Downloads/MAPslidesSELECCION25.html`** — 4,2 MB, un fichero, Tailwind (viola §2a de entrada), sin fronteras de template, nunca revisado. Dejarlo ahí invita a que alguien lo mine.

**Rendimiento de la sesión:** hasta 2.000 tok/deck de defecto corregido, una cola de riesgo de 11.668 tok eliminada, un callejón sin salida borrado. Después de eso, el lunes sigue con `shoot_snippets.py` (fase 1) — es el mejor primer día del proyecto: renderiza cosas que ya existen con scripts que ya existen, no requiere ningún juicio de diseño y no cierra ninguna puerta.

---

## 7. Riesgos y lo que NO hacer

### Riesgos reales, con su mitigación

**1. La tasa de acierto del canon no está medida, y de ella depende la fase 7.** Si los decks reales solo casan el 60 % de las slides, `FREEHAND.md` dispara constantemente y el ahorro cae. Instrumenta `matched/unmatched/hand-edited` por slide desde el primer deck construido sobre el canon; diez decks es el punto de decisión; no borres nada de §15 hasta tener ese dato.

**2. Los defectos del banco llegan disfrazados de mediciones.** El número más peligroso es el piso tipográfico: un fitter que reporte "el p10 real es 14 px" se leerá como autorización, cuando lo que significa es que un tercio de esas slides nunca fueron legibles. Si el nivel de 16 px se despliega sin lista cerrada de clases con FAIL en `verify_deck.py`, la prosa libre llega a 16 px en dos decks y la principal defensa de legibilidad del skill desaparece. Valídalo contra un render proyectado real de las slides 203 y 175 antes de enviarlo: 16 px en navegador con zoom no es el mismo problema que 8 pt impresos.

**3. La puerta humana de la fase 5 se salta.** Un `spec.json` que nadie leyó es idéntico a uno aprobado, y es peor que ninguna puerta porque parece revisado. `approvedBy` + `approvedAt` obligatorios, y `codegen` se niega a construir sin ellos.

**4. Los gates que aterrizan como FAIL el primer día bloquean todo el trabajo.** Varios templates violarán §15 inmediatamente. WARN primero, FAIL cuando el canon esté limpio, y que la promoción nunca ocurra en silencio.

**5. Un `--check` de CORE generado sobrescribe ediciones a mano en silencio.** El banner GENERATED mitiga pero no impide. Quien escriba en `CORE.md` pierde su trabajo en el siguiente build.

**6. Un gate de diff de preview produce fallos falsos** por cambios de renderizado de fuente o versión de Chrome. Compara con tolerancia y fija la versión de Chrome en CI, o la gente aprende a aprobar diffs sin mirar, que es peor que no tener gate.

**7. La disciplina de la cinta métrica se degrada.** En cuanto alguien con `inventory2.json` abierto piense "voy a scriptear la familia de enumeración", vuelves a un conjunto derivado sin revisar, con los costes de la curación y ninguno de sus beneficios. La defensa estructural es que ningún template se admite sin `spec.json` y `useWhen` escritos a mano. Es honestamente un problema de disciplina con solo respuesta mecánica parcial.

**8. Las 25 son una selección de lo que MAP ha hecho, no de lo que MAP necesita.** Es retrospectiva por construcción. La regla de crecimiento 6 (tres disparos de freehand ganan un spec) es la única defensa, y es reactiva a propósito.

### Lo que este plan rechaza deliberadamente

**Figma, en cualquier punto de la tubería.** Ver §2. La excepción de FigJam es un artefacto de reunión del que nada aguas abajo puede leer.

**Convertir las 205 slides a HTML.** Ya se hizo y el artefacto está en disco. Convierte el *spec*, no la slide, y solo para los huecos.

**Clustering no supervisado sobre las 205.** Se midió: 65 buckets, 33 singletons, y un bucket de 51 slides que fusiona tres de tus ocho familias (la 14, narrativa de 3 shapes; la 183, bloque de color comparativo; la 151, lista con imagen a sangre — las tres bajo "tiene una foto grande, aridad 1"). El etiquetado ya lo hiciste tú a mano; gastar cómputo en recuperar parcialmente un juicio que se lee gratis en una tabla markdown es la peor operación del expediente.

**Ajustar por mediana a través de slides "hermanas".** Este es el fallo fatal del plan de extracción, y su propio caso de validación lo demuestra: la 86 son tres columnas a x=61/645/1251 (paso ~590) con numerales a 192 px; la 103 son cuatro a x=123/565/1005/1446 (paso ~442) con numerales a 32 px como etiquetas. El paso mediano ajustado es ~516, que no casa con ninguna, y el numeral —elemento focal en una, etiqueta en la otra— se promedia hasta desaparecer. Usa recuperación con semilla **solo como informe de cobertura**, nunca como asignación y nunca como input de ajuste.

**Construir `render_slide.py` antes de medir la tasa de relleno.** Un mes de trabajo cuyo techo demostrado puede ser 1.441 tok/deck si la premisa es falsa.

**Borrar §15.3, §15.4, la sección STOP (`SKILL.md:33-63`), NN7 o los cinco defaults de NN2.** Los cuatro últimos no existen en CORE — un grep lo confirma. §15.3/§15.4 dan forma a la decisión antes de que exista DOM y el verificador solo los marca como WARN, así que confiar en él es enviar deriva.

**Borrar `WPP-ES-DESIGN-GUIDELINE.md`.** Degrádalo a producto de build en un `build/` gitignoreado con un stub en la ruta vieja. Es la única cosa que prueba que el orden de las secciones sigue siendo correcto, y la única forma de fichero único que un revisor humano o un diff contra un playbook futuro necesita. Lo que hay que quitar es el **lenguaje de arbitraje** que invita a una lectura de 28.645 tok, no el fichero.

**Instalar LibreOffice para renderizar el pptx de 640 MB.** `soffice` no está en esta máquina y no hace falta: `MAP_slides_SELECCION_25.pdf` (13,5 MB) y `MAP_PPTTemplate_v2.pdf` (5,4 MB) ya están en disco, y `pdftoppm` está en `/opt/homebrew/bin`. 25 renders de referencia en menos de un minuto.

**Editar `SNIPPET-INDEX.md` o `assets/snippets/variants/` a mano.** Ambos son generados; la siguiente ejecución de `derive_capacity.py` borra tu trabajo. Se edita `assets/snippets/*.html` (los 13 canónicos) o el generador.

**Cambiar el favicon del skill, retirar los 51 variants en bloque, o añadir matemática de 5 columnas.** La última no reproduce bajo dos mediciones independientes: mídela bien o deja la rejilla en 4.