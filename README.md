# 🚀 NYC Flights 2013 - Interactive Analysis Dashboard

[![Open Dashboard](https://img.shields.io/badge/Open-Dashboard-brightgreen?style=for-the-badge)](https://htmlpreview.github.io/?https://github.com/YOUR_USERNAME/nyc-flights-analysis/blob/main/dashboard_with_charts.html)

A comprehensive interactive dashboard analyzing 336,776 flights from NYC in 2013. Learn about **confounding variables**, **selection bias**, **Simpson's Paradox**, and critical data thinking through real visualizations.

## ✨ Features

- 📊 **9 Interactive Plotly Charts** - Fully responsive and zoomable
- 🎯 **Real Data Analysis** - 336,776 flights, 16 airlines, 3 airports
- 📚 **Educational** - Learn critical thinking about data
- 🌐 **Standalone HTML** - No server needed, works offline
- 📱 **Responsive Design** - Desktop, tablet, and mobile
- ⌨️ **Easy Navigation** - Buttons and keyboard shortcuts (arrow keys)

## 🎓 What You'll Learn

### Key Concepts

| Concept | What It Is | Example |
|---------|-----------|---------|
| **Confounding Variables** | 3rd variable affects both X and Y | Weather correlates with delays, but winter also has holiday travel |
| **Selection Bias** | Systematically missing data | Cancelled flights don't appear in delay statistics |
| **Simpson's Paradox** | Pattern reverses in subgroups | Later flights delayed overall, but not for all carriers |
| **Stat vs Practical Significance** | Huge data makes tiny differences "significant" | 1-minute airport difference is statistically but not practically significant |
| **Correlation ≠ Causation** | Relationship doesn't imply causation | Plane age correlates with delays but doesn't cause them |

## 📊 Dashboard Sections

1. **Home** - Dataset overview (336,776 flights)
2. **Cancelled Flights** - Selection bias example
3. **Manufacturers** - Fleet composition trends
4. **SFO Routes** - Market share analysis
5. **Weather Impact** - 4 visualizations (temperature, visibility, wind, precipitation)
6. **Carrier Rankings** - Why naive rankings mislead
7. **Delay Patterns** - Departure vs arrival delay recovery
8. **Simpson's Paradox** - Time of day effects by carrier
9. **Plane Age** - Aircraft age vs performance
10. **Airport Comparison** - Statistical vs practical significance

## 🚀 Quick Start

### Option 1: View Online
[Click here to view the dashboard!](https://htmlpreview.github.io/?https://github.com/YOUR_USERNAME/nyc-flights-analysis/blob/main/dashboard_with_charts.html)

### Option 2: Clone & Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/nyc-flights-analysis.git
cd nyc-flights-analysis

# Open the dashboard
open dashboard_with_charts.html
# or use Python server
python -m http.server 8000
# Visit http://localhost:8000/dashboard_with_charts.html
```

### Option 3: Generate Your Own

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure you have data folder with CSV files
mkdir data
cp flights.csv airlines.csv airports.csv planes.csv weather.csv data/

# Run the generator script
python generate_dashboard_html.py

# This creates: dashboard_with_charts.html
```

## 📁 Repository Structure

```
nyc-flights-analysis/
├── README.md                          # Main documentation
├── dashboard_with_charts.html         # 🎯 Interactive dashboard (MAIN FILE)
├── generate_dashboard_html.py         # Python script to regenerate
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── LICENSE                            # MIT License
├── docs/
│   ├── GUIDE.md                      # Detailed user guide
│   ├── CONCEPTS.md                   # Concepts explained
│   ├── DATA_DICTIONARY.md            # Data descriptions
│   └── TROUBLESHOOTING.md            # Common issues
├── data/
│   ├── flights.csv                   # 336,776 flight records
│   ├── airlines.csv                  # 16 airlines
│   ├── airports.csv                  # Airport info
│   ├── planes.csv                    # Aircraft specs
│   └── weather.csv                   # Weather data
└── images/
    └── dashboard-preview.png         # Dashboard screenshot
```

## 📊 Data Overview

**Source:** nycflights13 (All NYC departures in 2013)

### Statistics
- **Total Flights:** 336,776
- **Airlines:** 16
- **Departure Airports:** 3 (JFK, LGA, EWR)
- **Destination Airports:** 100+
- **Aircraft:** 3,323 unique planes
- **Time Period:** January-December 2013

### Key Metrics
- **Avg Departure Delay:** 12.6 minutes
- **Avg Arrival Delay:** 6.9 minutes  
- **Cancellation Rate:** 1.5%
- **Avg Flight Distance:** 1,037 miles

## 🎯 Learning Outcomes

After exploring this dashboard, you'll understand:

✅ How to identify confounding variables  
✅ What selection bias means and why it matters  
✅ Simpson's Paradox and when it occurs  
✅ Statistical vs practical significance  
✅ Why correlation doesn't equal causation  
✅ Critical thinking framework for data analysis  

## 💡 Key Insights

### Real Examples from the Data

1. **February Paradox** - High cancellations but LOW delays
   - **Why?** Flights in worst weather got cancelled
   - **Lesson:** You're missing the worst cases (selection bias)

2. **Carrier Rankings** - Airlines appear to have different performance
   - **Why?** Different airlines fly different routes
   - **Lesson:** Route difficulty is a confounder

3. **Weather Impact** - Bad weather correlates with delays
   - **Why?** Winter has both weather AND holiday travel
   - **Lesson:** Multiple causes can create correlations

4. **Time of Day** - Later flights delayed, but pattern reverses by carrier
   - **Why?** Different carriers have different route mixes
   - **Lesson:** Aggregate patterns can reverse in subgroups (Simpson's Paradox)

5. **Plane Age** - Older planes show more delays
   - **Why?** Could be routes, maintenance, or selection
   - **Lesson:** Correlation doesn't prove causation

## 🛠️ Technical Details

### How It Works

1. **Data Processing** - Python with pandas/numpy
2. **Analysis** - Groupby aggregations and calculations
3. **Visualization** - Plotly chart generation
4. **Delivery** - Embedded in standalone HTML
5. **Viewing** - Works in any modern browser

### Technologies

```
Python 3.7+
├── pandas (data manipulation)
├── numpy (numerical computing)
├── plotly (interactive charts)
├── scipy (statistics)
└── json (data serialization)

Frontend
├── HTML5
├── CSS3
├── JavaScript
└── Plotly.js (from CDN)
```

### Generate Your Own Dashboard

```bash
python generate_dashboard_html.py
```

This script:
- ✅ Loads CSV data
- ✅ Processes with pandas
- ✅ Creates Plotly charts
- ✅ Embeds in HTML
- ✅ Outputs standalone file

## 📚 Documentation

### For Users
- **[User Guide](docs/GUIDE.md)** - How to use the dashboard
- **[Concepts Explained](docs/CONCEPTS.md)** - Deep dive into each idea
- **[Data Dictionary](docs/DATA_DICTIONARY.md)** - What each variable means
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Fix common issues

### For Developers
- **[Technical Overview](docs/TECHNICAL.md)** - Architecture and code
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Development Setup](docs/DEV_SETUP.md)** - Set up development environment

## 🔧 Development Setup

### Prerequisites
- Python 3.7 or higher
- pip or conda
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/nyc-flights-analysis.git
cd nyc-flights-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python generate_dashboard_html.py --help
```

### Generate Dashboard

```bash
# Create/update dashboard
python generate_dashboard_html.py

# Output: dashboard_with_charts.html (200KB, fully standalone)
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Ideas for Contributions

- 📊 Add more analyses or visualizations
- 📝 Improve documentation
- 🐛 Fix bugs or issues
- 🌍 Translate to other languages
- 📱 Enhance mobile experience
- ♿ Improve accessibility

## 📋 Requirements

### For Running HTML Dashboard
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for initial Plotly library load)
- No installation needed!

### For Generating Dashboard
- Python 3.7+
- See `requirements.txt` for packages

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

**In short:** You're free to use, modify, and distribute this project, as long as you include the license.

## 🙏 Credits

- **Data Source:** [nycflights13](https://github.com/hadley/nycflights13) package
- **Inspired by:** Hadley Wickham's R for Data Science
- **Built with:** Python, Pandas, Plotly
- **Educational Philosophy:** Critical thinking about data

## 📞 Support & Questions

### Getting Help

1. **📖 Documentation** - Check [docs/](docs/) folder
2. **🔍 Issues** - Search [existing issues](https://github.com/YOUR_USERNAME/nyc-flights-analysis/issues)
3. **❓ Questions** - [Create a new issue](https://github.com/YOUR_USERNAME/nyc-flights-analysis/issues/new) with question label
4. **🐛 Bugs** - [Report bugs](https://github.com/YOUR_USERNAME/nyc-flights-analysis/issues/new) with bug label

### Resources

- [Simpson's Paradox - Wikipedia](https://en.wikipedia.org/wiki/Simpson%27s_paradox)
- [Confounding Variable - Wikipedia](https://en.wikipedia.org/wiki/Confounding)
- [R for Data Science - Book](https://r4ds.had.co.nz/)
- [Spurious Correlations](https://www.tylervigen.com/spurious-correlations)

## 🚀 Roadmap

- [ ] Add more flight analysis scenarios
- [ ] Create interactive exercises
- [ ] Add video explanations
- [ ] Support for other datasets
- [ ] Multilingual support
- [ ] Mobile app version
- [ ] API for data access

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/nyc-flights-analysis?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/nyc-flights-analysis?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/YOUR_USERNAME/nyc-flights-analysis?style=social)

## ⭐ Show Your Support

If you find this project helpful, please:
- ⭐ **Star** the repository
- 🍴 **Fork** it for your own use
- 🤝 **Share** with others learning about data
- 💬 **Contribute** with improvements

---

**Made with ❤️ for data literacy and critical thinking**

Happy analyzing! 🚀✈️📊

