# Angband Trading

> *A comprehensive quantitative trading learning platform*

**Angband Trading** is a structured educational project designed to progressively build quantitative trading skills from data collection to strategy deployment. This repository follows a methodical approach to learning algorithmic trading concepts.

## 📚 Learning Objectives

This project serves as a hands-on learning journey through quantitative finance, covering:

- **Data Engineering**: Market data collection, cleaning, and storage
- **Exploratory Analysis**: Statistical analysis and pattern recognition
- **Strategy Development**: Implementation of trading algorithms
- **Backtesting**: Performance evaluation and risk assessment
- **Optimization**: Parameter tuning and strategy refinement
- **Risk Management**: Portfolio construction and risk metrics

## 🎯 Project Structure

The repository is organized to support progressive learning:

```
angband-trading/
├── src/angband/              # Core library modules
│   ├── core/                 # Configuration and utilities
│   ├── data/                 # Data collection and processing
│   ├── strategies/           # Trading strategy implementations
│   ├── backtesting/          # Performance testing framework
│   └── utils/                # Common utilities
├── notebooks/                # Jupyter notebooks for exploration
│   ├── 01_exploration/       # Data exploration and analysis
│   ├── 02_research/          # Strategy research and development
│   └── 03_backtesting/       # Strategy testing and validation
├── data/                     # Data storage
│   ├── raw/                  # Original market data
│   ├── processed/            # Cleaned and transformed data
│   └── external/             # External datasets
├── configs/                  # Configuration files
└── docs/                     # Documentation and research notes
```

## 🚀 Getting Started

### Environment Setup
```bash
# Clone the repository
git clone https://github.com/jmarke17/angband_trading.git
cd angband_trading

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### First Steps
```python
from angband.data.collectors import DataCollector
from angband.core.config import Config

# Initialize data collector
collector = DataCollector()
data = collector.fetch_data("AAPL", period="1y")

print("Angband Trading environment ready for learning")
```

## 📈 Learning Roadmap

### Phase 1: Data Foundation (Weeks 1-2)
- **Market Data Collection**: Learn to gather reliable financial data
- **Data Quality Assessment**: Understand data issues and cleaning
- **Exploratory Data Analysis**: Statistical properties of financial time series
- **Visualization**: Create meaningful charts and plots

### Phase 2: Technical Analysis (Weeks 3-4)
- **Indicators Implementation**: Moving averages, RSI, MACD, etc.
- **Signal Generation**: Convert indicators into trading signals
- **Pattern Recognition**: Identify common market patterns
- **Correlation Analysis**: Understand asset relationships

### Phase 3: Strategy Development (Weeks 5-8)
- **Simple Strategies**: Moving average crossovers, mean reversion
- **Strategy Framework**: Modular strategy implementation
- **Parameter Optimization**: Grid search and walk-forward analysis
- **Multi-asset Strategies**: Portfolio-based approaches

### Phase 4: Risk and Performance (Weeks 9-12)
- **Backtesting Engine**: Realistic simulation framework
- **Performance Metrics**: Sharpe ratio, maximum drawdown, etc.
- **Risk Management**: Position sizing and portfolio constraints
- **Statistical Testing**: Significance of results

## 🛠️ Configuration

The system uses YAML configuration files for easy experimentation:

```yaml
# configs/settings.yaml
data:
  primary_source: "yfinance"
  cache_enabled: true
  update_frequency: "daily"

trading:
  initial_capital: 100000
  commission: 0.001
  risk_per_trade: 0.02

backtesting:
  start_date: "2020-01-01"
  benchmark: "SPY"
  rebalance_frequency: "monthly"
```

## 📊 Key Metrics and Analysis

### Performance Metrics
- **Returns**: Total and annualized returns
- **Risk-Adjusted Returns**: Sharpe ratio, Sortino ratio
- **Drawdown Analysis**: Maximum drawdown, recovery time
- **Statistical Tests**: T-tests, autocorrelation analysis

### Risk Metrics
- **Volatility**: Historical and realized volatility
- **Value at Risk (VaR)**: Potential losses at confidence levels
- **Beta**: Market sensitivity analysis
- **Correlation**: Asset and strategy correlations

## 🧪 Testing and Validation

```bash
# Run all tests
pytest tests/ -v

# Test specific components
pytest tests/test_strategies/ -k "moving_average"

# Coverage analysis
pytest --cov=src/angband tests/
```

## 📝 Documentation and Learning Notes

- **Research Notes**: Document learning insights and market observations
- **Strategy Ideas**: Maintain a backlog of strategy concepts to explore
- **Performance Reviews**: Regular analysis of what works and what doesn't
- **Literature Reviews**: Summaries of relevant academic papers and books

## 🤝 Contributing to Learning

This is primarily a learning project, but contributions that enhance the educational value are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-learning-module`)
3. Implement educational enhancements
4. Submit a pull request with clear documentation

## 📚 Recommended Reading

- **"Quantitative Trading" by Ernest Chan**
- **"Algorithmic Trading" by Jeffrey Bacidore**
- **"Machine Learning for Asset Managers" by Marcos López de Prado**
- **"Advances in Financial Machine Learning" by Marcos López de Prado**

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact and Discussion

- **Issues**: For bug reports and technical questions
- **Discussions**: For strategy ideas and learning discussions
- **Wiki**: For detailed documentation and tutorials

---

> *"The best way to learn quantitative trading is by building, testing, and iterating."*

**Happy Learning and Trading! 📈**