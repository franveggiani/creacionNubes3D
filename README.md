# 📸 Creación de Nubes 3D a partir de Video

Este proyecto permite generar **nubes de puntos 3D** a partir de un video grabado con una cámara calibrada, utilizando códigos QR como referencia espacial y detección de objetos (como bayas). Está pensado para aplicaciones como **agricultura de precisión**, reconstrucción de escenas y análisis espacial.

---

## 🚀 Características

- Detección de códigos QR para referencia espacial.
- Segmentación de objetos por umbral (color/luminosidad).
- Proyección espacial y generación de nube de puntos.
- Soporte para múltiples distancias y configuraciones.
- Totalmente configurable mediante archivo JSON.

---

## 📁 Estructura del Proyecto

```
creacionNubes3D/
├── input/                   # Carpeta con los videos de entrada
├── output/                  # Carpeta para resultados y nubes generadas
├── calibraciones/           # Archivos de calibración (YAML)
├── reproyecciones/          # CSV con reproyecciones (opcional)
├── main.py                  # Script principal
├── utils/                   # Funciones auxiliares
├── config.json              # Ejemplo de configuración
└── requirements.txt         # Dependencias de Python
```

---

## 🧪 Requisitos

- Python 3.8 o superior
- ffmpeg (instalado en el sistema)

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Cómo usar

1. Colocá tu video en la carpeta `input/`.
2. Verificá que tengas la calibración de cámara en formato YAML.
3. Creá tu archivo `config.json` con la configuración deseada.
4. Ejecutá el script:

```bash
python main.py config.json
```

---

## 🧾 Ejemplo de configuración (`config.json`)

```json
{
  "input_path": "./input",
  "video_name": "VID_20230322_173621",
  "baya_threshold": 105,
  "qr_threshold": 120,
  "output_path": "./output",
  "calib_file": "MotorolaG200_Javo_Vertical.yaml",
  "qr_dist": 2.1,
  "dists_list": [
    10,
    20,
    5
  ],
  "min_mer": 10,
  "min_dist": 0,
  "min_path": "",
  "input_csv_name": "Reproyecciones.csv"
}
```

---

## 🧷 Descripción de parámetros

| Parámetro          | Descripción                                                                 |
|--------------------|------------------------------------------------------------------------------|
| `input_path`       | Ruta a la carpeta que contiene el video.                                    |
| `video_name`       | Nombre del archivo de video sin extensión (ej. `video1` para `video1.mp4`). |
| `baya_threshold`   | Umbral de detección para las bayas u objetos segmentables.                  |
| `qr_threshold`     | Umbral para la detección de códigos QR.                                     |
| `output_path`      | Carpeta donde se guardarán los resultados.                                  |
| `calib_file`       | Archivo de calibración de cámara en formato YAML.                           |
| `qr_dist`          | Distancia real entre los códigos QR en metros.                              |
| `dists_list`       | Lista de distancias (en cm) a usar en cada escena/cuadro.                   |
| `min_mer`          | Área mínima de los objetos detectados (en píxeles).                         |
| `min_dist`         | Valor mínimo de distancia para considerar detecciones válidas.              |
| `min_path`         | Ruta a nube base mínima opcional.                                           |
| `input_csv_name`   | Nombre del CSV con reproyecciones previas si se desea reusar datos.         |

---

## 🖼️ Salidas Generadas

- Imágenes con detecciones superpuestas.
- CSV con coordenadas reproyectadas.
- Nube de puntos 3D en formato `.ply` o `.xyz`.
- Estadísticas y gráficos de procesamiento.

---

## 📦 Ejemplo de uso

```bash
python main.py config.json
```

> Asegurate de tener tu video en `./input/`, la calibración en `./calibraciones/` y de haber configurado correctamente los valores del JSON.

---

## 🛠 Autor

**Franco Veggiani**  
🔗 [github.com/franveggiani](https://github.com/franveggiani)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.  
Consultá el archivo `LICENSE` para más información.

---
