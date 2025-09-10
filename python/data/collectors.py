"""
Data Collectors - Sistema de recopilación de datos financieros

Este módulo proporciona colectores de datos con sistema de caché automático
para diferentes fuentes de datos financieros.
"""

from typing import Optional, Union
import pandas as pd
import yfinance as yf

# Importar funciones de utils
from python.utils.functions import cache_data, validate_ticker


class StockDataCollector:
    """
    Colector de datos de acciones con sistema de caché automático

    Utiliza yfinance como fuente principal y cachea automáticamente
    los resultados para optimizar consultas repetidas.
    """

    def __init__(self, cache_dir: str = "data/raw"):
        """
        Inicializar colector de datos

        Args:
            cache_dir: directorio para archivos de cache
        """
        self.cache_dir = cache_dir

    @cache_data(key_params=['ticker', 'period'], prefix="stock")
    def fetch_stock_data(self, ticker: str, period: str = "1y",
                        interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Obtener datos históricos de una acción

        Args:
            ticker: símbolo de la acción (ej: "AAPL", "MSFT")
            period: período de datos ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
            interval: intervalo de datos ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")

        Returns:
            DataFrame con datos OHLCV o None si hay error
        """
        # Validar ticker
        if not validate_ticker(ticker):
            print(f"❌ Ticker inválido: {ticker}")
            return None

        try:
            # Crear objeto ticker
            stock = yf.Ticker(ticker.upper())

            # Obtener datos históricos
            data = stock.history(period=period, interval=interval)

            if data.empty:
                print(f"❌ No se encontraron datos para {ticker}")
                return None

            # Limpiar datos
            data = data.dropna()

            # Añadir información útil
            data['Ticker'] = ticker.upper()
            data['Date'] = data.index

            print(f"✅ Datos obtenidos: {ticker} ({len(data)} registros)")
            return data

        except Exception as e:
            print(f"❌ Error obteniendo datos de {ticker}: {e}")
            return None

    def fetch_multiple_stocks(self, tickers: list, period: str = "1y",
                             interval: str = "1d") -> dict:
        """
        Obtener datos de múltiples acciones

        Args:
            tickers: lista de símbolos de acciones
            period: período de datos
            interval: intervalo de datos

        Returns:
            diccionario con ticker como clave y DataFrame como valor
        """
        results = {}

        print(f"📊 Obteniendo datos de {len(tickers)} acciones...")

        for ticker in tickers:
            data = self.fetch_stock_data(ticker, period, interval)
            if data is not None:
                results[ticker] = data

        print(f"✅ Completado: {len(results)}/{len(tickers)} acciones obtenidas")
        return results

    def get_stock_info(self, ticker: str) -> dict:
        """
        Obtener información fundamental de una acción (sin cache)

        Args:
            ticker: símbolo de la acción

        Returns:
            diccionario con información de la empresa
        """
        try:
            stock = yf.Ticker(ticker.upper())
            info = stock.info

            # Extraer información relevante
            relevant_info = {
                'symbol': info.get('symbol'),
                'longName': info.get('longName'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'marketCap': info.get('marketCap'),
                'currentPrice': info.get('currentPrice'),
                'currency': info.get('currency'),
                'exchange': info.get('exchange'),
                'country': info.get('country')
            }

            return relevant_info

        except Exception as e:
            print(f"❌ Error obteniendo info de {ticker}: {e}")
            return {}


# Instancia global para uso fácil
stock_collector = StockDataCollector()