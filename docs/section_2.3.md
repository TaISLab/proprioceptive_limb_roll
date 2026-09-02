# Section 2.3 — Percepción táctil propioceptiva

Transcription from *Sistema multisensorial para la interacción física
humano-robot* (R. Castro Ochoa, TFM, Universidad de Málaga, 2026), §2.3.
Kept for reference; the running text of this repo is in English in
[`method.md`](method.md).

---

Ante las limitaciones que presentan los métodos estrictamente visuales de
detección de pose, se plantea el uso de una percepción multimodal basada en la
percepción táctil propioceptiva de la garra durante el acoplamiento. Esta
percepción consiste en el uso del estado interno de las posiciones articulares de
las falanges pasivas durante el acoplamiento para modelar geométricamente el
antebrazo.

## 2.3.1 Modelo geométrico de la sección del antebrazo humano

El estudio [4] revela que la sección transversal del antebrazo se puede modelar
como una elipse con una alta correlación. Realizaron un escaneo 3D de 6 sujetos y
ajustaron las nubes de puntos a una elipse (figura 2.7). Demostraron:

- **Ajuste casi perfecto:** las ecuaciones que modelan los ejes mayor y menor de
  la elipse lograron R² entre 0.898 y 0.980.
- **Bajo error:** el RMSE representa entre el 0.21 % y el 0.64 % de la
  circunferencia del antebrazo; la desviación media entre el brazo escaneado y el
  modelo de la elipse fue de menos de 1.5 mm.

Estos resultados demuestran la viabilidad de usar la envolvente mecánica generada
por los eslabones de la garra subactuada para estimar la elipse anatómica y, con
ello, extraer el eje mayor para la estimación del último grado de libertad q5 y
el eje longitudinal del antebrazo, aprovechando la doble pinza de la garra.

*(Figura 2.7: ajuste de modelos elípticos sobre escaneos 3D del antebrazo humano,
sección transversal al 20 % de la longitud del radio con origen en el codo.
Adaptada de [4].)*

## 2.3.2 Problema del MVIE

Se busca la elipse que maximiza el área dentro del polígono de contacto. En la
literatura de optimización, este problema se conoce como el **Elipsoide Inscrito
de Máximo Volumen** (Maximum Volume Inscribed Ellipsoid, MVIE) [36]. Se formula
como un problema de optimización convexa donde el log-determinante de la matriz
de forma de la elipse se maximiza sujeto a las restricciones lineales que imponen
las caras del polígono.

### 2.3.2.1 Parametrización de la elipse

Se parte del círculo unitario centrado en el origen,
`B = { u ∈ R² | ‖u‖₂ ≤ 1 }` (2.5). Se transforma mediante una matriz de forma
`G ∈ R^{2×2}`: si `G` es identidad no se modifica; diagonal escala los ejes X e Y
por separado; los elementos fuera de la diagonal introducen rotación. Se impone
`G` simétrica definida positiva (`G ≻ 0`), de modo que sus autovalores
`(λ1, λ2)` son las magnitudes físicas de los semiejes. Se aplica un vector de
traslación `c` para situar el centro.

    E = { x ∈ R² | x = G u + c }          (2.6)

- `c ∈ R²`: centro geométrico de la elipse.
- `G ∈ S²₊₊`: simétrica definida positiva 2×2; autovalores = semiejes,
  autovectores = orientación.

### 2.3.2.2 Restricciones de contorno

Los vértices del polígono se ordenan en sentido antihorario (interior a la
izquierda). Cada arista define una recta que divide el plano en dos semiespacios;
el semiespacio interior (zona válida del agarre) se formula como:

    aᵢᵀ x ≤ bᵢ                            (2.7)

- `x`: cualquier punto del semiespacio interior.
- `aᵢ`: vector normal a la pared.
- `bᵢ`: límite escalar del semiespacio.

El polígono `P` es la intersección de los `m` semiespacios:
`P = { x | aᵢᵀ x ≤ bᵢ, i = 1…m }`. Sustituyendo (2.6) en (2.7):
`aᵢᵀ (G u + c) ≤ bᵢ` → `aᵢᵀ G u + aᵢᵀ c ≤ bᵢ`. En el caso más desfavorable
(la elipse toca la arista), `max aᵢᵀ G u = ‖Gᵀ aᵢ‖₂`. Asumiendo `G = Gᵀ`:

    ‖G aᵢ‖₂ + aᵢᵀ c ≤ bᵢ                  (2.8)

### 2.3.2.3 Formulación del problema de optimización

El área de la elipse escala con `det(G)` (`Área(E) ∝ det(G)`), luego maximizar el
área equivale a maximizar `det(G)`. Como `det` no es cóncava, se usa
`log det(G)`, que es monótona creciente (mismo maximizador) y cóncava sobre
`G ≻ 0`. El problema es entonces convexo (resoluble en milisegundos, máximo
global):

    maximizar   log det(G)                (2.9)
    sobre       G, c
    sujeto a    G ⪰ 0
                ‖G aᵢ‖₂ + aᵢᵀ c ≤ bᵢ,   i = 1,…,m

---

**Referencias citadas:** `[4]` estudio del ajuste elíptico de la sección del
antebrazo (escaneo 3D, 6 sujetos); `[36]` MVIE / elipsoide de John.
*(Completar las citas bibliográficas exactas desde la bibliografía del TFM.)*
