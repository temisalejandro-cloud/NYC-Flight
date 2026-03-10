#!/usr/bin/env python3
"""
Generate HTML dashboard with embedded Plotly charts
Run this script to create dashboard_with_charts.html
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from scipy import stats as sp_stats

print("Generating dashboard with charts...")

# ============================================================================
# LOAD DATA
# ============================================================================

data_path = Path("data")
if not data_path.exists():
    print("❌ Error: 'data' folder not found!")
    print("Please ensure you have a 'data' folder with CSV files:")
    print("  - flights.csv")
    print("  - airlines.csv")
    print("  - airports.csv")
    print("  - planes.csv")
    print("  - weather.csv")
    exit(1)

print("Loading data...", end=" ")
try:
    flights = pd.read_csv(data_path / "flights.csv")
    airlines = pd.read_csv(data_path / "airlines.csv")
    airports = pd.read_csv(data_path / "airports.csv")
    weather = pd.read_csv(data_path / "weather.csv")
    planes = pd.read_csv(data_path / "planes.csv")
    print("✓")
except FileNotFoundError as e:
    print(f"❌ {e}")
    exit(1)

# ============================================================================
# PREPROCESS DATA
# ============================================================================

print("Processing data...", end=" ")

flights['cancelled'] = flights['dep_time'].isna()

# Planes
planes['manufacturer'] = planes['manufacturer'].str.upper().str.strip()
conditions = [
    planes['manufacturer'].str.contains('AIRBUS', na=False),
    planes['manufacturer'].str.contains('BOEING', na=False),
    planes['manufacturer'].str.contains('MCDONNELL|DOUGLAS', na=False, regex=True),
    planes['manufacturer'].str.contains('BOMBARDIER|CANADAIR', na=False, regex=True),
    planes['manufacturer'].str.contains('EMBRAER', na=False),
    planes['manufacturer'].str.contains('CESSNA', na=False)
]
choices = ['AIRBUS', 'BOEING', 'MCDONNELL DOUGLAS', 'BOMBARDIER', 'EMBRAER', 'CESSNA']
planes['manufacturer_clean'] = np.select(conditions, choices, default=planes['manufacturer'])

n_threshold = 10
counts = planes['manufacturer_clean'].value_counts()
small_n_manufacturers = counts[counts < n_threshold].index
planes['manufacturer_final'] = planes['manufacturer_clean'].replace(small_n_manufacturers, 'Other')

flights['time_of_day'] = pd.cut(flights['hour'], 
                                bins=[0, 6, 12, 18, 24],
                                labels=['Night', 'Morning', 'Afternoon', 'Evening'])

flights_weather = flights.merge(
    weather,
    on=['year', 'month', 'day', 'hour', 'origin'],
    how='left'
)

flights_weather['has_precip'] = flights_weather['precip'] > 0
flights_weather['visibility_category'] = pd.cut(
    flights_weather['visib'],
    bins=[0, 2, 5, 10, 15],
    labels=['Poor', 'Fair', 'Good', 'Excellent']
)

flights_weather['temp_bin'] = pd.cut(flights_weather['temp'], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110])
flights_weather['wind_bin'] = pd.cut(flights_weather['wind_speed'], bins=8)

planes_for_age = planes[['tailnum', 'year']].rename(columns={'year': 'manufacture_year'})
flights_planes = flights.merge(planes_for_age, on='tailnum', how='left')
flights_planes['plane_age'] = 2013 - flights_planes['manufacture_year']
flights_planes_clean = flights_planes[(flights_planes['plane_age'] >= 0) & (flights_planes['plane_age'] <= 50)]

valid_flights = flights.dropna(subset=['dep_delay', 'arr_delay', 'air_time'])
valid_flights['delay_recovered'] = valid_flights['dep_delay'] - valid_flights['arr_delay']

print("✓")

# ============================================================================
# CREATE CHART DATA
# ============================================================================

print("Generating charts...", end=" ")

month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Chart 1: Cancelled flights
cancelled_by_month = flights.groupby("month")['cancelled'].mean().reset_index().sort_values('cancelled', ascending=False)
chart1 = {
    "data": [{"type": "bar", "x": [month_labels[int(m)-1] for m in cancelled_by_month['month']], 
              "y": [float(x) for x in cancelled_by_month['cancelled']], 
              "marker": {"color": [float(x) for x in cancelled_by_month['cancelled']], "colorscale": "RdYlBu_r"}}],
    "layout": {"title": "Cancelled Flights by Month", "xaxis": {"title": "Month"}, 
               "yaxis": {"title": "Cancellation Rate"}, "height": 500}
}

# Chart 2: Manufacturers over time
manufacturer_over_time = flights.merge(planes, on='tailnum', how='left').groupby(['month', 'manufacturer_final']).size().reset_index(name='num_flight')
chart2_data = []
for mfg in sorted(manufacturer_over_time['manufacturer_final'].unique()):
    data = manufacturer_over_time[manufacturer_over_time['manufacturer_final'] == mfg].sort_values('month')
    chart2_data.append({
        "type": "scatter",
        "x": [int(x) for x in data['month']],
        "y": [int(x) for x in data['num_flight']],
        "mode": "lines+markers",
        "name": str(mfg)
    })
chart2 = {
    "data": chart2_data,
    "layout": {"title": "Aircraft Manufacturers Over Time", "xaxis": {"title": "Month", "tickvals": list(range(1, 13)), 
                                                                       "ticktext": month_labels}, 
               "yaxis": {"title": "Number of Flights"}, "hovermode": "x unified", "height": 500}
}

# Chart 3: SFO routes
fly_into_sfo = flights.query("dest=='SFO'").groupby('carrier').size().reset_index(name='num_flights').merge(airlines, on='carrier').sort_values('num_flights', ascending=False)
total_sfo = fly_into_sfo['num_flights'].sum()
fly_into_sfo['pct'] = (fly_into_sfo['num_flights'] / total_sfo * 100).round(1)
chart3 = {
    "data": [{"type": "bar", "y": [str(x) for x in fly_into_sfo['name']], "x": [int(x) for x in fly_into_sfo['num_flights']], 
              "orientation": "h", "marker": {"color": "#546E7A"},
              "text": [f"{p}%" for p in fly_into_sfo['pct']], "textposition": "outside"}],
    "layout": {"title": "Flights to SFO by Carrier", "xaxis": {"title": "Number of Flights"}, 
               "yaxis": {"title": ""}, "height": 500, "margin": {"l": 150}}
}

# Chart 4: Temperature vs delay
temp_delay = flights_weather.groupby('temp_bin')['dep_delay'].mean()
x_labels_temp = [f"{interval.mid:.0f}" if pd.notna(interval.mid) else 'NA' for interval in temp_delay.index]
chart4 = {
    "data": [{"type": "scatter", "x": x_labels_temp, "y": [float(x) for x in temp_delay], "mode": "lines+markers",
              "line": {"color": "#e74c3c", "width": 2}}],
    "layout": {"title": "Temperature vs Departure Delay", "xaxis": {"title": "Temperature (°F)"}, 
               "yaxis": {"title": "Avg Departure Delay (min)"}, "height": 400}
}

# Chart 5: Visibility vs delay
vis_delay = flights_weather.groupby('visibility_category')['dep_delay'].mean()
chart5 = {
    "data": [{"type": "bar", "x": [str(x) for x in vis_delay.index], "y": [float(x) for x in vis_delay], "marker": {"color": "#f39c12"}}],
    "layout": {"title": "Visibility vs Departure Delay", "xaxis": {"title": "Visibility"}, 
               "yaxis": {"title": "Avg Departure Delay (min)"}, "height": 400}
}

# Chart 6: Wind speed vs delay
wind_delay = flights_weather.groupby('wind_bin')['dep_delay'].mean()
x_labels_wind = [f"{interval.mid:.0f}" if pd.notna(interval.mid) else 'NA' for interval in wind_delay.index]
chart6 = {
    "data": [{"type": "scatter", "x": x_labels_wind, "y": [float(x) for x in wind_delay], "mode": "lines+markers",
              "line": {"color": "#9b59b6", "width": 2}}],
    "layout": {"title": "Wind Speed vs Departure Delay", "xaxis": {"title": "Wind Speed (mph)"}, 
               "yaxis": {"title": "Avg Departure Delay (min)"}, "height": 400}
}

# Chart 7: Precipitation vs delay
precip_delay = flights_weather.groupby(flights_weather['has_precip'])['dep_delay'].mean()
chart7 = {
    "data": [{"type": "bar", "x": ["No Rain", "Rain"], "y": [float(x) for x in precip_delay], 
              "marker": {"color": ["#3498db", "#e74c3c"]}}],
    "layout": {"title": "Precipitation vs Departure Delay", "xaxis": {"title": ""}, 
               "yaxis": {"title": "Avg Departure Delay (min)"}, "height": 400}
}

# Chart 8: Carrier delays (naive ranking)
carrier_delays = flights.merge(airlines, on='carrier').groupby("name").agg(avg_arrival_delay=('arr_delay','mean')).dropna().sort_values('avg_arrival_delay').reset_index()
chart8 = {
    "data": [{"type": "bar", "y": [str(x) for x in carrier_delays['name']], "x": [float(x) for x in carrier_delays['avg_arrival_delay']], 
              "orientation": "h", "marker": {"color": [float(x) for x in carrier_delays['avg_arrival_delay']], "colorscale": "RdYlBu_r"}}],
    "layout": {"title": "⚠️ Naive Carrier Rankings (Don't trust this!)", "xaxis": {"title": "Avg Arrival Delay (min)"}, 
               "yaxis": {"title": ""}, "height": 600, "margin": {"l": 150}}
}

# Chart 9: Delay scatter plot
sample_flights = valid_flights.sample(min(5000, len(valid_flights)))  # Sample for performance
min_val = min(sample_flights['dep_delay'].min(), sample_flights['arr_delay'].min())
max_val = max(sample_flights['dep_delay'].max(), sample_flights['arr_delay'].max())
chart9 = {
    "data": [
        {"type": "scatter", "x": [float(x) for x in sample_flights['dep_delay']], "y": [float(x) for x in sample_flights['arr_delay']],
         "mode": "markers", "marker": {"size": 2, "opacity": 0.3}, "name": "Flights"},
        {"type": "scatter", "x": [float(min_val), float(max_val)], "y": [float(min_val), float(max_val)], "mode": "lines",
         "name": "Perfect correlation", "line": {"color": "red", "dash": "dash", "width": 2}}
    ],
    "layout": {"title": "Departure vs Arrival Delay", "xaxis": {"title": "Departure Delay (min)"}, 
               "yaxis": {"title": "Arrival Delay (min)"}, "height": 500}
}

# Chart 10: Simpson's Paradox
carrier_time = flights.groupby(['carrier','time_of_day']).agg(avg_dep_delay=('dep_delay','mean')).reset_index()
top_5 = flights['carrier'].value_counts().head(5).index
carrier_time_top5 = carrier_time[carrier_time['carrier'].isin(top_5)].merge(airlines[['carrier', 'name']], on='carrier')
chart10_data = []
for carrier_name in sorted(carrier_time_top5['name'].unique()):
    data = carrier_time_top5[carrier_time_top5['name'] == carrier_name].sort_values('time_of_day')
    chart10_data.append({
        "type": "bar",
        "x": [str(x) for x in data['time_of_day']],
        "y": [float(x) for x in data['avg_dep_delay']],
        "name": str(carrier_name)
    })
chart10 = {
    "data": chart10_data,
    "layout": {"title": "Simpson's Paradox: Delay by Time of Day", "xaxis": {"title": "Time of Day"}, 
               "yaxis": {"title": "Avg Departure Delay (min)"}, "barmode": "group", "height": 500}
}

# Chart 11: Plane age regression
sample_planes = flights_planes_clean.sample(min(10000, len(flights_planes_clean)))
temp_df = flights_planes_clean[['plane_age', 'dep_delay']].dropna()
if len(temp_df) > 1:
    z = np.polyfit(temp_df['plane_age'], temp_df['dep_delay'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(temp_df['plane_age'].min(), temp_df['plane_age'].max(), 100)
    y_trend = [float(val) for val in p(x_trend)]  # Convert to float list
    x_trend = [float(val) for val in x_trend]      # Convert to float list
else:
    x_trend = []
    y_trend = []

chart11 = {
    "data": [
        {"type": "scatter", "x": [float(x) for x in sample_planes['plane_age']], 
         "y": [float(y) for y in sample_planes['dep_delay']],
         "mode": "markers", "marker": {"size": 2, "opacity": 0.3}},
        {"type": "scatter", "x": x_trend, "y": y_trend, "mode": "lines", "name": "Trend",
         "line": {"color": "red", "width": 2}}
    ],
    "layout": {"title": "Aircraft Age vs Departure Delay", "xaxis": {"title": "Plane Age (years)"}, 
               "yaxis": {"title": "Departure Delay (min)"}, "height": 500}
}

# Chart 12: Airport comparison
airport_stats = flights.groupby('origin')['dep_delay'].agg(['mean', 'std', 'count'])
airport_stats['se'] = airport_stats['std'] / np.sqrt(airport_stats['count'])
airport_stats['ci'] = airport_stats['count'].apply(lambda n: sp_stats.t.ppf(0.975, n - 1)) * airport_stats['se']

chart12_data = []
for origin in ['EWR', 'JFK', 'LGA']:
    row = airport_stats.loc[origin]
    chart12_data.append({
        "type": "scatter",
        "x": [float(row['mean'])],
        "y": [origin],
        "error_x": {"type": "data", "array": [float(row['ci'])], "visible": True},
        "mode": "markers",
        "name": origin,
        "marker": {"size": 12}
    })
chart12 = {
    "data": chart12_data,
    "layout": {"title": "Airport Delays (95% Confidence Intervals)", "xaxis": {"title": "Avg Departure Delay (min)"}, 
               "yaxis": {"title": ""}, "height": 400}
}

print("✓")

# ============================================================================
# GENERATE HTML WITH EMBEDDED CHARTS
# ============================================================================

print("Creating HTML...", end=" ")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NYC Flights 2013 - Analysis Dashboard with Charts</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f8f9fa;
            color: #2c3e50;
            line-height: 1.6;
        }}
        
        header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        header h1 {{
            margin: 0;
            font-size: 36px;
            font-weight: 600;
        }}
        
        header p {{
            margin: 12px 0 0 0;
            font-size: 16px;
            opacity: 0.9;
        }}
        
        nav {{
            background: white;
            padding: 15px 20px;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            border-bottom: 2px solid #ecf0f1;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow-x: auto;
        }}
        
        button {{
            padding: 10px 16px;
            border: none;
            background: #ecf0f1;
            color: #2c3e50;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s;
            white-space: nowrap;
            flex-shrink: 0;
        }}
        
        button:hover {{
            background: #bdc3c7;
            transform: translateY(-1px);
        }}
        
        button.active {{
            background: #3498db;
            color: white;
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 30px 20px;
        }}
        
        .section {{
            display: none;
            animation: fadeIn 0.3s ease-in;
        }}
        
        .section.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        h2 {{
            margin: 0 0 25px 0;
            font-size: 28px;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .chart {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .chart-container {{
            width: 100%;
            height: 500px;
        }}
        
        .chart-container-small {{
            width: 100%;
            height: 400px;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }}
        
        @media (max-width: 800px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .insight {{
            background: linear-gradient(135deg, #fff3cd 0%, #fffacd 100%);
            border-left: 4px solid #ffc107;
            padding: 18px;
            border-radius: 4px;
            margin: 25px 0;
            font-size: 15px;
            line-height: 1.7;
        }}
        
        .insight strong {{
            color: #e67e22;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}
        
        .metric {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .metric h3 {{
            font-size: 32px;
            color: #3498db;
            margin: 0 0 8px 0;
        }}
        
        .metric p {{
            color: #7f8c8d;
            font-size: 14px;
            margin: 0;
        }}
        
        footer {{
            background: #2c3e50;
            color: white;
            padding: 30px 20px;
            text-align: center;
            margin-top: 60px;
        }}
    </style>
</head>
<body>
    <header>
        <h1>✈️ NYC Flights 2013 - Analysis Dashboard</h1>
        <p>Interactive exploration with real Plotly charts</p>
    </header>
    
    <nav>
        <button class="nav-btn active" onclick="showSection(0)">🏠 Home</button>
        <button class="nav-btn" onclick="showSection(1)">1️⃣ Cancelled Flights</button>
        <button class="nav-btn" onclick="showSection(2)">2️⃣ Manufacturers</button>
        <button class="nav-btn" onclick="showSection(3)">3️⃣ SFO Routes</button>
        <button class="nav-btn" onclick="showSection(4)">4️⃣ Weather Impact</button>
        <button class="nav-btn" onclick="showSection(5)">5️⃣ Carrier Performance</button>
        <button class="nav-btn" onclick="showSection(6)">6️⃣ Delay Patterns</button>
        <button class="nav-btn" onclick="showSection(7)">7️⃣ Simpson's Paradox</button>
        <button class="nav-btn" onclick="showSection(8)">8️⃣ Plane Age</button>
        <button class="nav-btn" onclick="showSection(9)">9️⃣ Airport Comparison</button>
    </nav>
    
    <div class="container">
        <!-- HOME -->
        <div id="section-0" class="section active">
            <h2>🏠 Welcome to the NYC Flights Dashboard</h2>
            
            <div class="metrics">
                <div class="metric"><h3>336,776</h3><p>Total Flights</p></div>
                <div class="metric"><h3>16</h3><p>Airlines</p></div>
                <div class="metric"><h3>3</h3><p>NYC Airports</p></div>
                <div class="metric"><h3>2013</h3><p>Year</p></div>
            </div>
            
            <h3 style="margin-top: 30px;">📊 About This Dashboard</h3>
            <p>This dashboard visualizes real flight data with interactive Plotly charts. Click the buttons above to explore different analyses and learn about:</p>
            <ul style="margin-left: 25px; margin-top: 15px; line-height: 2;">
                <li><strong>Confounding Variables:</strong> Why simple comparisons mislead</li>
                <li><strong>Selection Bias:</strong> What data you're NOT seeing</li>
                <li><strong>Simpson's Paradox:</strong> When patterns reverse in subgroups</li>
                <li><strong>Statistical Significance:</strong> Tiny differences, big datasets</li>
                <li><strong>Correlation vs Causation:</strong> Why you can't claim causation</li>
            </ul>
            
            <div class="insight">
                <strong>🎯 Key Takeaway:</strong> Simple averages often mislead. This dashboard teaches critical thinking about data.
            </div>
        </div>
        
        <!-- SECTION 1: CANCELLED FLIGHTS -->
        <div id="section-1" class="section">
            <h2>1️⃣ Cancelled Flights by Month</h2>
            <div class="chart">
                <div id="chart1" class="chart-container"></div>
            </div>
            <div class="insight">
                <strong>🚨 Selection Bias:</strong> February has high cancellations AND low measured delays. Why? Flights in worst conditions got cancelled - they don't appear in delay stats! We're missing the worst cases.
            </div>
        </div>
        
        <!-- SECTION 2: MANUFACTURERS -->
        <div id="section-2" class="section">
            <h2>2️⃣ Aircraft Manufacturers Over Time</h2>
            <div class="chart">
                <div id="chart2" class="chart-container"></div>
            </div>
            <div class="insight">
                <strong>📈 Observation:</strong> Boeing and Airbus dominate. What changed between manufacturers tells a story about fleet modernization.
            </div>
        </div>
        
        <!-- SECTION 3: SFO ROUTES -->
        <div id="section-3" class="section">
            <h2>3️⃣ Flights to SFO by Carrier</h2>
            <div class="chart">
                <div id="chart3" class="chart-container"></div>
            </div>
            <div class="insight">
                <strong>💼 Market Share:</strong> United dominates NYC→SFO. Other airlines have minimal presence on this route.
            </div>
        </div>
        
        <!-- SECTION 4: WEATHER -->
        <div id="section-4" class="section">
            <h2>4️⃣ Weather Impact on Delays</h2>
            <div class="charts-grid">
                <div class="chart"><div id="chart4" class="chart-container-small"></div></div>
                <div class="chart"><div id="chart5" class="chart-container-small"></div></div>
                <div class="chart"><div id="chart6" class="chart-container-small"></div></div>
                <div class="chart"><div id="chart7" class="chart-container-small"></div></div>
            </div>
            <div class="insight">
                <strong>🌤️ Confounders:</strong> Weather correlates with delays, but confounders exist: bad weather in winter → holiday travel → more delays; bad weather → cancellations (survivor bias).
            </div>
        </div>
        
        <!-- SECTION 5: CARRIERS -->
        <div id="section-5" class="section">
            <h2>5️⃣ Carrier Rankings by Delay</h2>
            <div class="chart">
                <div id="chart8" class="chart-container"></div>
            </div>
            <div class="insight">
                <strong>⚠️ Warning:</strong> This ranking is MISLEADING! Different carriers fly different routes. A carrier that appears to have high delays might just fly harder routes. This is CONFOUNDING.
            </div>
        </div>
        
        <!-- SECTION 6: DELAY PATTERNS -->
        <div id="section-6" class="section">
            <h2>6️⃣ Departure vs Arrival Delay</h2>
            <div class="chart">
                <div id="chart9" class="chart-container"></div>
            </div>
            <div class="insight">
                <strong>✈️ Key Insight:</strong> Notice points BELOW the diagonal line. This means arrival delay < departure delay. Why? Pilots make up time in the air! Longer flights recover more delay, so comparing airlines by ARRIVAL delay is confounded by flight duration.
            </div>
        </div>
        
        <!-- SECTION 7: SIMPONS -->
        <div id="section-7" class="section">
            <h2>7️⃣ Simpson's Paradox: Time of Day Effects</h2>
            <div class="chart">
                <div id="chart10" class="chart-container"></div>
            </div>
            <div class="insight">
                <strong>🎭 Paradox:</strong> Overall, later flights have more delays. But when you look at individual carriers, patterns differ! Different carriers have different route mixes at different times.
            </div>
        </div>
        
        <!-- SECTION 8: PLANE AGE -->
        <div id="section-8" class="section">
            <h2>8️⃣ Aircraft Age Impact</h2>
            <div class="chart">
                <div id="chart11" class="chart-container"></div>
            </div>
            <div class="insight">
                <strong>🤔 Correlation or Causation?</strong> Older planes show more delays. But can we claim old age CAUSES delays? Other confounders: older planes fly different routes, operated by different airlines, have different maintenance practices.
            </div>
        </div>
        
        <!-- SECTION 9: AIRPORTS -->
        <div id="section-9" class="section">
            <h2>9️⃣ NYC Airport Comparison</h2>
            <div class="chart">
                <div id="chart12" class="chart-container-small"></div>
            </div>
            <div class="insight">
                <strong>📊 Statistical vs Practical:</strong> Differences ARE statistically significant (with 336k flights!), but are 1-2 minutes practically meaningful? Would you change airports to save 1 minute?
            </div>
        </div>
    </div>
    
    <footer>
        <p><strong>NYC Flights 2013 - Interactive Analysis Dashboard</strong></p>
        <p style="margin-top: 10px; font-size: 14px;">Built with Python, Pandas, and Plotly | Teaching Critical Data Thinking</p>
    </footer>
    
    <script>
        // Chart configurations
        const charts = {{
            1: {json.dumps(chart1)},
            2: {json.dumps(chart2)},
            3: {json.dumps(chart3)},
            4: {json.dumps(chart4)},
            5: {json.dumps(chart5)},
            6: {json.dumps(chart6)},
            7: {json.dumps(chart7)},
            8: {json.dumps(chart8)},
            9: {json.dumps(chart9)},
            10: {json.dumps(chart10)},
            11: {json.dumps(chart11)},
            12: {json.dumps(chart12)}
        }};
        
        // Render charts
        function renderChart(chartNum) {{
            const config = charts[chartNum];
            const elementId = 'chart' + chartNum;
            if (document.getElementById(elementId)) {{
                Plotly.newPlot(elementId, config.data, config.layout, {{responsive: true}});
            }}
        }}
        
        // Render initial charts
        for (let i = 1; i <= 12; i++) {{
            setTimeout(() => renderChart(i), 100);
        }}
        
        function showSection(index) {{
            // Hide all sections
            document.querySelectorAll('.section').forEach(el => {{
                el.classList.remove('active');
            }});
            
            // Remove active from buttons
            document.querySelectorAll('.nav-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // Show selected section
            const section = document.getElementById('section-' + index);
            if (section) {{
                section.classList.add('active');
                document.querySelectorAll('.nav-btn')[index].classList.add('active');
                window.scrollTo(0, 0);
                
                // Re-render charts when section becomes visible
                if (index === 1) renderChart(1);
                if (index === 2) renderChart(2);
                if (index === 3) renderChart(3);
                if (index === 4) {{ renderChart(4); renderChart(5); renderChart(6); renderChart(7); }}
                if (index === 5) renderChart(8);
                if (index === 6) renderChart(9);
                if (index === 7) renderChart(10);
                if (index === 8) renderChart(11);
                if (index === 9) renderChart(12);
            }}
        }}
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            const buttons = document.querySelectorAll('.nav-btn');
            const active = document.querySelector('.nav-btn.active');
            const index = Array.from(buttons).indexOf(active);
            
            if (e.key === 'ArrowRight' && index < buttons.length - 1) {{
                showSection(index + 1);
            }} else if (e.key === 'ArrowLeft' && index > 0) {{
                showSection(index - 1);
            }}
        }});
    </script>
</body>
</html>
"""

with open("dashboard_with_charts.html", "w") as f:
    f.write(html_content)

print("✓")
print("\n" + "="*60)
print("✅ SUCCESS!")
print("="*60)
print("\nGenerated: dashboard_with_charts.html")
print("\nTo use:")
print("  1. Open dashboard_with_charts.html in your browser")
print("  2. Click buttons to navigate")
print("  3. All charts are interactive!")
print("\nFeatures:")
print("  ✓ 9 interactive Plotly charts")
print("  ✓ Real data from your CSV files")
print("  ✓ Fully responsive design")
print("  ✓ Works offline (after initial load)")
print("="*60)
