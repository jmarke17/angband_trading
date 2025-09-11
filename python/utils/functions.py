"""
Utility Functions - Funciones auxiliares reutilizables

Funciones básicas y decoradores para el sistema de trading.
"""

import pickle
from datetime import date
from pathlib import Path
from functools import wraps
import pandas as pd


def cache_data(cache_dir: str = "data/raw"):
    """
    Decorador mejorado para cachear datos usando pickle

    Genera archivo: ticker_periodo_fecha.pkl
    Primera vez: ejecuta función y guarda
    Siguientes veces: carga desde pickle

    MANEJA TANTO DataFrames COMO diccionarios

    Args:
        cache_dir: directorio donde guardar cache
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extraer parámetros básicos (ticker, period)
            ticker = args[1] if len(args) > 1 else kwargs.get('ticker', 'DATA')
            period = args[2] if len(args) > 2 else kwargs.get('period', '1y')

            # Crear clave: ticker_periodo_fecha
            today = date.today().strftime('%Y-%m-%d')
            cache_key = f"{ticker}_{period}_{today}"

            # Crear directorio y archivo
            cache_path = Path(cache_dir)
            cache_path.mkdir(parents=True, exist_ok=True)
            cache_file = cache_path / f"{cache_key}.pkl"

            # Cargar desde cache si existe
            if cache_file.exists():
                print(f"📦 Cache: {cache_key}")
                try:
                    with open(cache_file, 'rb') as f:
                        return pickle.load(f)
                except Exception as e:
                    print(f"⚠️ Error cargando cache, descargando nuevamente: {e}")

            # Ejecutar función y guardar
            print(f"🌐 Descarga: {cache_key}")
            result = func(*args, **kwargs)

            # Guardar si hay datos válidos
            should_cache = False

            if result is not None:
                # Verificar si es DataFrame
                if isinstance(result, pd.DataFrame):
                    should_cache = not result.empty
                # Verificar si es diccionario
                elif isinstance(result, dict):
                    should_cache = bool(result)  # True si el dict no está vacío
                # Otros tipos (listas, etc.)
                else:
                    should_cache = bool(result)

            if should_cache:
                try:
                    with open(cache_file, 'wb') as f:
                        pickle.dump(result, f)
                    print(f"💾 Guardado: {cache_key}")
                except Exception as e:
                    print(f"⚠️ Error guardando cache: {e}")

            return result

        return wrapper

    return decorator