"""
Angband Trading - ETL Principal

ETL sencilla: Extract (descargar), Transform (procesar), Load (guardar)
"""

import time
from datetime import datetime


def extract_data(ticker: str = "AAPL"):
    """
    EXTRACT: Descargar todos los datos disponibles del ticker
    """
    print(f"🔽 EXTRACT: Descargando datos completos de {ticker}")
    print("-" * 50)

    try:
        from python.data.collectors import stock_collector

        start_time = time.time()

        # Descarga completa de todos los datos
        complete_data = stock_collector.fetch_complete_stock_data(ticker)

        extract_time = time.time() - start_time

        if complete_data and complete_data.get('data_sources'):
            print(f"✅ Extract completado en {extract_time:.2f}s")
            print(f"📊 Fuentes obtenidas: {len(complete_data['data_sources'])}")
            return complete_data
        else:
            print("❌ Error en Extract: No se obtuvieron datos")
            return None

    except Exception as e:
        print(f"❌ Error en Extract: {e}")
        return None


def transform_data(raw_data):
    """
    TRANSFORM: Procesar y estructurar los datos básicos
    """
    print(f"\n🔄 TRANSFORM: Procesando datos")
    print("-" * 50)

    if not raw_data:
        print("❌ No hay datos para transformar")
        return None

    try:
        transformed = {
            'ticker': raw_data['ticker'],
            'processed_at': datetime.now().isoformat(),
            'summary': {}
        }

        # Procesar datos históricos principales
        if 'historical' in raw_data:
            historical = raw_data['historical']

            # Usar el período más largo disponible
            main_data = None
            for period in ['max_1d', '10y_1d', '5y_1d', '3y_1d', '1y_1d']:
                if period in historical:
                    main_data = historical[period]['data']
                    transformed['summary']['data_period'] = period
                    break

            if main_data is not None:
                # Calcular métricas básicas
                latest_price = main_data['Close'].iloc[-1]
                first_price = main_data['Close'].iloc[0]
                total_return = ((latest_price - first_price) / first_price) * 100

                transformed['summary']['price_data'] = {
                    'current_price': round(latest_price, 2),
                    'first_price': round(first_price, 2),
                    'max_price': round(main_data['High'].max(), 2),
                    'min_price': round(main_data['Low'].min(), 2),
                    'total_return_pct': round(total_return, 2),
                    'avg_volume': int(main_data['Volume'].mean()),
                    'total_records': len(main_data)
                }
                print(f"  ✅ Datos históricos procesados: {len(main_data)} registros")

        # Procesar información fundamental
        if 'key_metrics' in raw_data:
            metrics = raw_data['key_metrics']

            basic_info = metrics.get('basic_info', {})
            market_data = metrics.get('market_data', {})

            transformed['summary']['company_info'] = {
                'name': basic_info.get('longName', 'N/A'),
                'sector': basic_info.get('sector', 'N/A'),
                'market_cap': market_data.get('marketCap'),
                'current_price': market_data.get('currentPrice')
            }
            print(f"  ✅ Información fundamental procesada")

        # Procesar dividendos si existen
        if 'dividends' in raw_data:
            div_data = raw_data['dividends']
            transformed['summary']['dividends'] = {
                'total_payments': div_data['total_payments'],
                'total_amount': round(div_data['total_amount'], 2),
                'avg_dividend': round(div_data['average_dividend'], 2)
            }
            print(f"  ✅ Dividendos procesados: {div_data['total_payments']} pagos")

        print(f"✅ Transform completado")
        return transformed

    except Exception as e:
        print(f"❌ Error en Transform: {e}")
        return None


def load_summary(processed_data):
    """
    LOAD: Mostrar resumen final de los datos procesados
    """
    print(f"\n📤 LOAD: Generando resumen final")
    print("-" * 50)

    if not processed_data or not isinstance(processed_data, dict):
        print("❌ No hay datos procesados válidos para mostrar")
        return False

    try:
        ticker = processed_data.get('ticker', 'UNKNOWN')
        summary = processed_data.get('summary', {})

        print(f"\n🏢 EMPRESA: {ticker}")
        print("=" * 30)

        # Información de la empresa
        if 'company_info' in summary:
            company = summary['company_info']
            print(f"📋 Nombre: {company.get('name', 'N/A')}")
            print(f"🏭 Sector: {company.get('sector', 'N/A')}")
            print(f"🔧 Industria: {company.get('industry', 'N/A')}")

            market_cap = company.get('market_cap')
            if market_cap and market_cap > 0:
                market_cap_b = market_cap / 1e9
                print(f"💰 Capitalización: ${market_cap_b:.1f}B")

        # Datos de precios
        if 'price_data' in summary:
            prices = summary['price_data']
            print(f"\n📊 DATOS DE PRECIOS:")
            print(f"💵 Precio actual: ${prices.get('current_price', 'N/A')}")
            print(f"📈 Máximo histórico: ${prices.get('max_price', 'N/A')}")
            print(f"📉 Mínimo histórico: ${prices.get('min_price', 'N/A')}")
            print(f"🎯 Retorno total: {prices.get('total_return_pct', 'N/A')}%")
            print(f"📊 Volumen promedio: {prices.get('avg_volume', 'N/A'):,}")
            print(f"📅 Registros históricos: {prices.get('total_records', 'N/A'):,}")
            print(f"📆 Período: {prices.get('date_range', 'N/A')}")

            # Mostrar el período de datos usado
            data_period = summary.get('data_period', 'N/A')
            print(f"⏰ Período usado: {data_period}")

        # Dividendos
        if 'dividends' in summary:
            div = summary['dividends']
            print(f"\n💰 DIVIDENDOS:")
            print(f"💸 Total pagos: {div.get('total_payments', 0)}")
            print(f"💵 Monto total: ${div.get('total_amount', 0)}")
            print(f"📊 Promedio por pago: ${div.get('avg_dividend', 0)}")
        else:
            print(f"\n💰 DIVIDENDOS: Sin historial de dividendos")

        # Splits
        if 'splits' in summary:
            splits = summary['splits']
            print(f"\n📊 SPLITS: {splits.get('total_splits', 0)} eventos de división")

        print(f"\n✅ Resumen generado exitosamente")
        return True

    except Exception as e:
        print(f"❌ Error en Load: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_etl(ticker: str = "AAPL"):
    """
    Ejecutar el proceso ETL completo
    """
    print("🏰 Angband Trading - ETL Pipeline")
    print("=" * 60)
    print(f"🎯 Procesando: {ticker}")
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # ETL Pipeline
    raw_data = extract_data(ticker)
    processed_data = transform_data(raw_data)
    success = load_summary(processed_data)

    # Resultado final
    print("\n" + "=" * 60)
    print("🎯 RESULTADO ETL")
    print("=" * 60)

    if success:
        print("✅ ETL completado exitosamente")
        print("📊 Datos extraídos, transformados y cargados")
        print("🚀 Sistema listo para análisis avanzado")
    else:
        print("❌ ETL falló")
        print("🔧 Revisa los errores anteriores")

    print(f"⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return success


if __name__ == "__main__":
    # Ejecutar ETL para AAPL
    run_etl("AAPL")