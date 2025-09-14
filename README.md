# Angband Trading

Una plataforma educativa de *quantitative trading* para desarrollar, evaluar y comparar estrategias de trading cuantitativo de forma reproducible.

---

## Tabla de contenidos

1. [Descripción](#descripción)  
2. [Características](#características)  
3. [Estructura del proyecto](#estructura-del-proyecto)  
4. [Requisitos previos](#requisitos-previos)  
5. [Instalación](#instalación)  
6. [Uso](#uso)  
7. [Ejecutar tests](#ejecutar-tests)  
8. [Roadmap](#roadmap)  
9. [Cómo contribuir](#cómo-contribuir)  
10. [Licencia](#licencia)

---

## Descripción

Angband Trading es una herramienta educativa para:

- Recolección y procesamiento de datos históricos de mercado (OHLCV, dividendos, splits, etc.)  
- Cálculo de indicadores técnicos básicos  
- Definición, implementación y evaluación de estrategias de trading  
- Backtesting con métricas clave (Sharpe, Sortino, drawdown, VaR, etc.)  
- Generación de reportes visuales y comparación frente a benchmarks  

---

## Características

- Configuración declarativa mediante archivos YAML  
- Arquitectura modular: **datos → indicadores → estrategias → backtesting → reportes**  
- Métricas de rendimiento ya integradas  
- Notebooks de ejemplo disponibles para exploración interactiva  
- Bajo licencia MIT, lo que permite contribuciones abiertas  

---

## Estructura del proyecto

.
├── configs/                  # Archivos de configuración YAML  
├── data/                     # Datos raw / procesados / caché  
├── logs/                     # Archivos de log de ejecución  
├── notebooks/                # Notebooks de exploración / análisis  
├── src/angband/              # Código fuente  
│   ├── core/                 # Configuración, utilidades comunes  
│   ├── data/                 # Módulos para recolectar y procesar datos  
│   ├── indicators/           # Cálculos de indicadores técnicos  
│   ├── strategies/           # Implementaciones de estrategias de trading  
│   ├── backtesting/          # Motor de simulación de trading  
│   └── reports/              # Generación de reportes visuales  
├── tests/                    # Tests automatizados  
├── requirements.txt          # Dependencias para correr el proyecto  
├── requirements-dev.txt      # Dependencias para desarrollo (tests, linters, etc.)  
├── pyproject.toml            # Metadatos para instalación como paquete (si aplica)  
└── README.md  

---

## Requisitos previos

- Python 3.8 o superior  
- Git  
- Dependencias que se indican en `requirements.txt`  
- (Opcional) Jupyter Notebook para exploración interactiva  

---

## Instalación

```bash
git clone https://github.com/jmarke17/angband_trading.git
cd angband_trading

# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.\.venv\Scripts\activate    # Windows

# Instalar dependencias principales
pip install -r requirements.txt

# Para desarrollo (linters, tests, etc.)
pip install -r requirements-dev.txt

# Si existe pyproject.toml o setup.py, también se puede instalar como paquete editable
pip install -e .
```

---

## Uso

Algunos ejemplos de comandos / flujo de trabajo:

```bash
# Descargar datos para un símbolo en un rango de fechas
python -m angband.data --symbol AAPL --start 2020-01-01 --end 2023-01-01

# Ejecutar estrategia (por ejemplo, cruce de medias móviles)
python -m angband.backtesting --strategy sma_crossover --symbol AAPL --config configs/sma_config.yaml

# Generar reporte visual
python -m angband.reports --output reports/aapl_sma.html
```

También hay notebooks en `notebooks/` que muestran ejemplos completos de descarga de datos, ejecución de estrategia y visualización de resultados.

---

## Ejecutar tests

```bash
pytest
```

Se recomienda que los tests cubran:

- Indicadores técnicos con valores conocidos  
- Comportamiento del motor de backtesting en escenarios básicos (sin comisiones / slippage)  
- Prueba end-to-end pequeña que recorra todo el pipeline  

---

## Roadmap

- ✅ Fase 1: Recolección de datos & procesamiento  
- ✅ Fase 2: Implementación de indicadores básicos  
- ✅ Fase 3: Motor de backtesting simple  
- Próxima: manejo de riesgo, slippage, optimización de parámetros  
- Próxima: soporte para múltiples benchmarks  
- Próxima: CLI más robusta / interfaz de usuario  
- Próxima: generación de reportes en HTML/PDF  

---

## Cómo contribuir

1. Haz *fork* del repositorio  
2. Crea una rama nueva para tu feature o corrección (`git checkout -b mi-feature`)  
3. Añade tests que cubran tus cambios  
4. Asegúrate de que el código pase linters / formateo (black, ruff, etc.)  
5. Abre un *pull request* explicando claramente qué haces y por qué  

---

## Licencia

Este proyecto está bajo la licencia **MIT**. Ver archivo [LICENSE](LICENSE) para más detalles.
