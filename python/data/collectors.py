"""
Data Collectors - Sistema de recopilación de datos financieros COMPLETO

Este módulo proporciona colectores de datos con sistema de caché automático
para diferentes fuentes de datos financieros, descargando TODA la información disponible.
"""

from typing import Optional, Union, Dict, Any
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Importar funciones de utils
from python.utils.functions import cache_data


class ComprehensiveStockDataCollector:
    """
    Colector COMPLETO de datos de acciones con sistema de caché automático

    Descarga TODA la información disponible:
    - Datos históricos (múltiples períodos)
    - Información fundamental completa
    - Dividendos e historial de splits
    - Datos de opciones
    - Métricas financieras
    - Noticias y eventos
    """

    def __init__(self, cache_dir: str = "data/raw"):
        """
        Inicializar colector de datos completo

        Args:
            cache_dir: directorio para archivos de cache
        """
        self.cache_dir = cache_dir

    def _validate_ticker(self, ticker: str) -> bool:
        """
        Validación básica de ticker (función interna)
        """
        if not isinstance(ticker, str):
            return False

        ticker = ticker.strip().upper()

        if not ticker or len(ticker) > 10:
            return False

        import re
        pattern = r'^[A-Z0-9\.\-\^]+$'
        return bool(re.match(pattern, ticker))

    @cache_data(cache_dir="data/raw")
    def fetch_complete_stock_data(self, ticker: str, max_period: str = "max") -> Dict[str, Any]:
        """
        🚀 DESCARGA COMPLETA DE TODOS LOS DATOS DISPONIBLES

        Args:
            ticker: símbolo de la acción
            max_period: período máximo para datos históricos

        Returns:
            Dict con TODA la información disponible
        """
        # Validar ticker
        if not self._validate_ticker(ticker):
            print(f"❌ Ticker inválido: {ticker}")
            return {}

        print(f"🔍 DESCARGA COMPLETA: {ticker.upper()}")
        print("=" * 50)

        try:
            stock = yf.Ticker(ticker.upper())
            complete_data = {
                'ticker': ticker.upper(),
                'download_timestamp': datetime.now().isoformat(),
                'data_sources': []
            }

            # 1. DATOS HISTÓRICOS (MÚLTIPLES PERÍODOS)
            print("📈 Descargando datos históricos...")
            historical_data = {}

            periods = ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"]
            intervals = ["1d"]  # Puede expandirse a ["1d", "1wk", "1mo"]

            for period in periods:
                for interval in intervals:
                    try:
                        data = stock.history(period=period, interval=interval)
                        if data is not None and not data.empty:
                            key = f"{period}_{interval}"
                            historical_data[key] = {
                                'data': data,
                                'records': len(data),
                                'start_date': data.index[0].strftime('%Y-%m-%d'),
                                'end_date': data.index[-1].strftime('%Y-%m-%d')
                            }
                            print(f"  ✅ {key}: {len(data)} registros")
                    except Exception as e:
                        print(f"  ❌ Error {period}_{interval}: {e}")

            complete_data['historical'] = historical_data
            complete_data['data_sources'].append('historical_prices')

            # 2. INFORMACIÓN FUNDAMENTAL COMPLETA
            print("\n🏢 Descargando información fundamental...")
            try:
                info = stock.info
                complete_data['fundamental_info'] = info
                complete_data['data_sources'].append('fundamental_info')

                # Extraer métricas clave
                key_metrics = {
                    'basic_info': {
                        'symbol': info.get('symbol'),
                        'longName': info.get('longName'),
                        'sector': info.get('sector'),
                        'industry': info.get('industry'),
                        'country': info.get('country'),
                        'exchange': info.get('exchange'),
                        'currency': info.get('currency')
                    },
                    'market_data': {
                        'marketCap': info.get('marketCap'),
                        'currentPrice': info.get('currentPrice'),
                        'previousClose': info.get('previousClose'),
                        'open': info.get('open'),
                        'dayLow': info.get('dayLow'),
                        'dayHigh': info.get('dayHigh'),
                        'volume': info.get('volume'),
                        'averageVolume': info.get('averageVolume')
                    },
                    'valuation': {
                        'trailingPE': info.get('trailingPE'),
                        'forwardPE': info.get('forwardPE'),
                        'priceToBook': info.get('priceToBook'),
                        'enterpriseValue': info.get('enterpriseValue'),
                        'priceToSalesTrailing12Months': info.get('priceToSalesTrailing12Months')
                    },
                    'financial_health': {
                        'totalCash': info.get('totalCash'),
                        'totalDebt': info.get('totalDebt'),
                        'totalRevenue': info.get('totalRevenue'),
                        'grossMargins': info.get('grossMargins'),
                        'operatingMargins': info.get('operatingMargins'),
                        'profitMargins': info.get('profitMargins')
                    },
                    'dividends': {
                        'dividendYield': info.get('dividendYield'),
                        'dividendRate': info.get('dividendRate'),
                        'payoutRatio': info.get('payoutRatio'),
                        'exDividendDate': info.get('exDividendDate')
                    }
                }
                complete_data['key_metrics'] = key_metrics
                print(f"  ✅ Información fundamental: {len(info)} campos")
            except Exception as e:
                print(f"  ❌ Error info fundamental: {e}")

            # 3. DIVIDENDOS E HISTORIAL
            print("\n💰 Descargando historial de dividendos...")
            try:
                dividends = stock.dividends
                if dividends is not None and not dividends.empty:
                    complete_data['dividends'] = {
                        'data': dividends,
                        'total_payments': len(dividends),
                        'first_dividend': dividends.index[0].strftime('%Y-%m-%d'),
                        'last_dividend': dividends.index[-1].strftime('%Y-%m-%d'),
                        'total_amount': dividends.sum(),
                        'average_dividend': dividends.mean()
                    }
                    complete_data['data_sources'].append('dividends')
                    print(f"  ✅ Dividendos: {len(dividends)} pagos")
                else:
                    print(f"  ℹ️ No hay historial de dividendos")
            except Exception as e:
                print(f"  ❌ Error dividendos: {e}")

            # 4. SPLITS DE ACCIONES
            print("\n📊 Descargando historial de splits...")
            try:
                splits = stock.splits
                if splits is not None and not splits.empty:
                    complete_data['splits'] = {
                        'data': splits,
                        'total_splits': len(splits),
                        'first_split': splits.index[0].strftime('%Y-%m-%d'),
                        'last_split': splits.index[-1].strftime('%Y-%m-%d')
                    }
                    complete_data['data_sources'].append('splits')
                    print(f"  ✅ Splits: {len(splits)} eventos")
                else:
                    print(f"  ℹ️ No hay historial de splits")
            except Exception as e:
                print(f"  ❌ Error splits: {e}")

            # 5. ESTADOS FINANCIEROS
            print("\n📋 Descargando estados financieros...")

            # Balance Sheet
            try:
                balance_sheet = stock.balance_sheet
                if balance_sheet is not None and not balance_sheet.empty:
                    complete_data['balance_sheet'] = balance_sheet
                    complete_data['data_sources'].append('balance_sheet')
                    print(f"  ✅ Balance Sheet: {balance_sheet.shape}")
            except Exception as e:
                print(f"  ❌ Error Balance Sheet: {e}")

            # Income Statement
            try:
                financials = stock.financials
                if financials is not None and not financials.empty:
                    complete_data['income_statement'] = financials
                    complete_data['data_sources'].append('income_statement')
                    print(f"  ✅ Income Statement: {financials.shape}")
            except Exception as e:
                print(f"  ❌ Error Income Statement: {e}")

            # Cash Flow
            try:
                cashflow = stock.cashflow
                if cashflow is not None and not cashflow.empty:
                    complete_data['cashflow'] = cashflow
                    complete_data['data_sources'].append('cashflow')
                    print(f"  ✅ Cash Flow: {cashflow.shape}")
            except Exception as e:
                print(f"  ❌ Error Cash Flow: {e}")

            # 6. RECOMENDACIONES DE ANALISTAS
            print("\n🎯 Descargando recomendaciones...")
            try:
                recommendations = stock.recommendations
                if recommendations is not None and not recommendations.empty:
                    complete_data['recommendations'] = recommendations
                    complete_data['data_sources'].append('recommendations')
                    print(f"  ✅ Recomendaciones: {len(recommendations)} registros")
                else:
                    print(f"  ℹ️ No hay recomendaciones disponibles")
            except Exception as e:
                print(f"  ❌ Error recomendaciones: {e}")

            # 7. NOTICIAS RECIENTES
            print("\n📰 Descargando noticias...")
            try:
                news = stock.news
                if news:
                    complete_data['news'] = news
                    complete_data['data_sources'].append('news')
                    print(f"  ✅ Noticias: {len(news)} artículos")
                else:
                    print(f"  ℹ️ No hay noticias disponibles")
            except Exception as e:
                print(f"  ❌ Error noticias: {e}")

            # 8. DATOS DE OPCIONES (si están disponibles)
            print("\n🎲 Descargando datos de opciones...")
            try:
                options_dates = stock.options
                if options_dates:
                    options_data = {}
                    # Limitar a las primeras 3 fechas para no sobrecargar
                    for date in options_dates[:3]:
                        try:
                            option_chain = stock.option_chain(date)
                            options_data[date] = {
                                'calls': option_chain.calls,
                                'puts': option_chain.puts
                            }
                        except:
                            pass

                    if options_data:
                        complete_data['options'] = {
                            'available_dates': options_dates,
                            'chains': options_data
                        }
                        complete_data['data_sources'].append('options')
                        print(f"  ✅ Opciones: {len(options_dates)} fechas, {len(options_data)} cadenas descargadas")
                else:
                    print(f"  ℹ️ No hay datos de opciones disponibles")
            except Exception as e:
                print(f"  ❌ Error opciones: {e}")

            # RESUMEN FINAL
            print(f"\n" + "=" * 50)
            print(f"✅ DESCARGA COMPLETA FINALIZADA")
            print(f"📊 Fuentes de datos obtenidas: {len(complete_data['data_sources'])}")
            print(f"📁 Fuentes: {', '.join(complete_data['data_sources'])}")

            return complete_data

        except Exception as e:
            print(f"❌ Error general descargando {ticker}: {e}")
            return {}

    def fetch_stock_data(self, ticker: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Método simplificado para compatibilidad (descarga solo datos históricos)
        SIN DECORADOR CACHE para evitar conflictos
        """
        if not self._validate_ticker(ticker):
            print(f"❌ Ticker inválido: {ticker}")
            return None

        try:
            stock = yf.Ticker(ticker.upper())
            data = stock.history(period=period, interval=interval)

            if data is not None and not data.empty:
                data = data.dropna()
                data['Ticker'] = ticker.upper()
                data['Date'] = data.index

                print(f"✅ Datos obtenidos: {ticker} ({len(data)} registros)")
                return data
            else:
                print(f"❌ No se encontraron datos para {ticker}")
                return None

        except Exception as e:
            print(f"❌ Error obteniendo datos de {ticker}: {e}")
            return None

    def fetch_multiple_complete(self, tickers: list) -> Dict[str, Dict]:
        """
        Descarga completa para múltiples tickers
        """
        results = {}

        print(f"🚀 DESCARGA MASIVA: {len(tickers)} acciones")
        print("=" * 60)

        for i, ticker in enumerate(tickers, 1):
            print(f"\n[{i}/{len(tickers)}] Procesando {ticker}...")

            if self._validate_ticker(ticker):
                data = self.fetch_complete_stock_data(ticker)
                if data:
                    results[ticker] = data
                    print(f"✅ {ticker} completado")
            else:
                print(f"❌ {ticker} inválido - omitido")

        print(f"\n🎯 RESUMEN MASIVO:")
        print(f"✅ Acciones procesadas: {len(results)}/{len(tickers)}")

        return results

    def get_cache_status(self) -> dict:
        """
        Obtener estado del sistema de cache
        """
        import os
        import glob
        from datetime import datetime

        cache_pattern = os.path.join(self.cache_dir, "*.pkl")
        cache_files = glob.glob(cache_pattern)

        status = {
            'cache_dir': self.cache_dir,
            'cache_exists': os.path.exists(self.cache_dir),
            'total_files': len(cache_files),
            'files': []
        }

        for cache_file in cache_files:
            try:
                stat = os.stat(cache_file)
                file_info = {
                    'name': os.path.basename(cache_file),
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                }
                status['files'].append(file_info)
            except Exception as e:
                print(f"❌ Error leyendo archivo {cache_file}: {e}")

        return status

    def clear_cache(self) -> None:
        """
        Limpiar archivos de cache del directorio
        """
        import os
        import glob

        cache_pattern = os.path.join(self.cache_dir, "*.pkl")
        cache_files = glob.glob(cache_pattern)

        for cache_file in cache_files:
            try:
                os.remove(cache_file)
                print(f"🗑️ Cache eliminado: {os.path.basename(cache_file)}")
            except Exception as e:
                print(f"❌ Error eliminando cache {cache_file}: {e}")

        print(f"✅ Limpieza de cache completada")


# Instancia global para uso fácil - NUEVA CLASE COMPLETA
stock_collector = ComprehensiveStockDataCollector()

# Mantener compatibilidad con código existente
StockDataCollector = ComprehensiveStockDataCollector