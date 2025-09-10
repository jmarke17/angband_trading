"""
Angband Trading - Main Entry Point

Este es el punto de entrada principal del proyecto de trading cuantitativo.
Aquí inicializamos y ejecutamos las diferentes funcionalidades del sistema.
"""

import time


def main():
    """
    Función principal del proyecto Angband Trading
    """
    print("🏰 Angband Trading - Quantitative Trading Platform")
    print("=" * 50)

    # Verificar que el entorno está configurado correctamente
    try:
        import sys
        print(f"✅ Python version: {sys.version}")

        # Verificar importaciones básicas
        import pandas as pd
        import numpy as np
        print(f"✅ Pandas version: {pd.__version__}")
        print(f"✅ NumPy version: {np.__version__}")

        print("\n🚀 Sistema inicializado correctamente!")
        print("📚 Listo para comenzar el aprendizaje de trading cuantitativo")

    except ImportError as e:
        print(f"❌ Error importing required libraries: {e}")
        print("💡 Make sure to install requirements: pip install -r requirements.txt")
        return False

    return True


def test_cache_system():
    """
    Probar el sistema de cache con datos reales
    """
    print("\n" + "=" * 50)
    print("🧪 PROBANDO SISTEMA DE CACHE")
    print("=" * 50)

    try:
        from python.data.collectors import stock_collector

        # Test 1: Primera descarga (desde yfinance)
        print("\n📊 Test 1: Primera descarga de AAPL")
        start_time = time.time()
        data1 = stock_collector.fetch_stock_data("AAPL", "1y")
        time1 = time.time() - start_time

        if data1 is not None:
            print(f"⏱️ Tiempo primera descarga: {time1:.2f} segundos")
            print(f"📈 Registros obtenidos: {len(data1)}")
            print(f"📅 Período: {data1.index[0]} a {data1.index[-1]}")

        # Test 2: Segunda descarga (desde cache)
        print("\n📦 Test 2: Segunda descarga de AAPL (cache)")
        start_time = time.time()
        data2 = stock_collector.fetch_stock_data("AAPL", "1y")
        time2 = time.time() - start_time

        if data2 is not None:
            print(f"⏱️ Tiempo desde cache: {time2:.2f} segundos")
            print(f"🚀 Aceleración: {time1 / time2:.1f}x más rápido")

        # Test 3: Datos múltiples
        print("\n📊 Test 3: Múltiples acciones")
        tickers = ["MSFT", "GOOGL", "TSLA"]
        start_time = time.time()
        multiple_data = stock_collector.fetch_multiple_stocks(tickers, "6mo")
        time3 = time.time() - start_time

        print(f"⏱️ Tiempo múltiples: {time3:.2f} segundos")
        print(f"✅ Acciones obtenidas: {len(multiple_data)}/{len(tickers)}")

        # Test 4: Información de empresa
        print("\n🏢 Test 4: Información de empresa")
        info = stock_collector.get_stock_info("AAPL")
        if info:
            print(f"📋 Empresa: {info.get('longName', 'N/A')}")
            print(f"🏭 Sector: {info.get('sector', 'N/A')}")
            print(f"💰 Precio actual: ${info.get('currentPrice', 'N/A')}")

        print("\n✅ TODOS LOS TESTS COMPLETADOS!")
        return True

    except Exception as e:
        print(f"❌ Error en tests de cache: {e}")
        return False


def test_project_structure():
    """
    Verificar que la estructura del proyecto está correcta
    """
    import os
    from pathlib import Path

    print("\n" + "=" * 50)
    print("🔍 VERIFICANDO ESTRUCTURA DEL PROYECTO")
    print("=" * 50)

    # Obtener el directorio raíz del proyecto
    project_root = Path(__file__).parent.parent

    # Directorios que deben existir
    required_dirs = [
        "python",
        "python/core",
        "python/data",
        "python/strategies",
        "python/backtesting",
        "python/utils",
        "python/visualization",
        "data",
        "configs",
        "tests",
        "scripts",
        "docs",
        "logs"
    ]

    missing_dirs = []

    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path}")
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"\n⚠️  Directorios faltantes: {missing_dirs}")
        return False
    else:
        print("\n✅ Estructura del proyecto verificada correctamente!")
        return True


def show_cache_status():
    """
    Mostrar estado actual del cache
    """
    print("\n" + "=" * 50)
    print("📦 ESTADO DEL CACHE")
    print("=" * 50)

    from pathlib import Path

    cache_dir = Path("data/raw")
    if not cache_dir.exists():
        print("📁 No existe directorio de cache")
        return

    cache_files = list(cache_dir.glob("*.pkl"))

    if not cache_files:
        print("🗂️ Cache vacío")
        return

    total_size = 0
    print(f"📦 Archivos en cache: {len(cache_files)}")

    for file in cache_files:
        size_mb = file.stat().st_size / (1024 * 1024)
        total_size += size_mb
        print(f"  📄 {file.name} ({size_mb:.2f} MB)")

    print(f"\n💾 Tamaño total del cache: {total_size:.2f} MB")


if __name__ == "__main__":
    print("Iniciando Angband Trading...")

    # 1. Verificar estructura
    structure_ok = test_project_structure()

    if not structure_ok:
        print("\n❌ Error en la estructura del proyecto")
        exit(1)

    # 2. Verificar entorno
    main_ok = main()

    if not main_ok:
        print("\n❌ Error en la inicialización del sistema")
        exit(1)

    # 3. Probar sistema de cache
    cache_ok = test_cache_system()

    # 4. Mostrar estado del cache
    show_cache_status()

    # 5. Resumen final
    print("\n" + "=" * 50)
    print("🎯 RESUMEN FINAL")
    print("=" * 50)

    if cache_ok:
        print("✅ Sistema de cache funcionando correctamente")
        print("✅ Colector de datos operativo")
        print("✅ Todas las pruebas pasaron")
        print("\n🚀 Sistema listo para el desarrollo!")
        print("\nPróximos pasos:")
        print("1. ✅ Estructura creada")
        print("2. ✅ Sistema de cache implementado")
        print("3. 📝 Crear análisis exploratorio")
        print("4. 📈 Implementar primera estrategia")
    else:
        print("❌ Problemas con el sistema de cache")
        print("💡 Revisa los errores anteriores")