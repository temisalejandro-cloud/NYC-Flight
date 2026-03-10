# 📖 User Guide - NYC Flights Dashboard

Complete guide to exploring and understanding the interactive dashboard.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Navigation](#navigation)
3. [Understanding Charts](#understanding-charts)
4. [Key Concepts](#key-concepts)
5. [Tips & Tricks](#tips--tricks)
6. [Frequently Asked Questions](#frequently-asked-questions)

## Getting Started

### Opening the Dashboard

**Method 1: Direct Open**
```bash
# On Windows
dashboard_with_charts.html (double-click)

# On Mac
open dashboard_with_charts.html

# On Linux
xdg-open dashboard_with_charts.html
```

**Method 2: Web Server**
```bash
python -m http.server 8000
# Visit: http://localhost:8000/dashboard_with_charts.html
```

**Method 3: Online**
- Visit the GitHub repository
- Use htmlpreview.github.io to view the HTML file

### First Look

When you open the dashboard, you'll see:
- **Header** - Title and description
- **Navigation Bar** - Buttons to switch between sections
- **Content Area** - Charts and explanations
- **Yellow Boxes** - Key insights and lessons

## Navigation

### Using Buttons

Click any button in the navigation bar to jump to that section:

```
🏠 Home
1️⃣ Cancelled Flights
2️⃣ Manufacturers
3️⃣ SFO Routes
4️⃣ Weather Impact
5️⃣ Carrier Rankings
6️⃣ Delay Patterns
7️⃣ Simpson's Paradox
8️⃣ Plane Age
9️⃣ Airport Comparison
```

### Using Keyboard

```
Arrow Left  (←)  - Previous section
Arrow Right (→)  - Next section
```

### Page Scroll

You can also scroll down to see full content in each section.

## Understanding Charts

### Interactive Features

All charts are powered by Plotly and include:

#### Hover Information
- Position mouse over data point
- See exact values in a tooltip
- Works on all chart types

#### Legend Toggle
- Click legend items to show/hide data series
- Double-click to isolate one series
- Useful for comparing specific groups

#### Zoom & Pan
- **Zoom:** Drag to select area, double-click to reset
- **Pan:** Hold Shift and drag to pan around
- **Box Select:** Click icon in toolbar to select regions

#### Download
- Click camera icon in Plotly toolbar
- Downloads chart as PNG image
- Perfect for presentations or reports

#### Toolbar Options
The Plotly toolbar (top right of each chart) includes:
- 📷 Download as PNG
- 🔍 Zoom in/out
- 🎯 Box select / Lasso select
- 🔄 Pan tool
- ⚙️ Settings
- ❓ Info

### Chart Types Used

**Bar Charts**
- Show categorical comparisons
- Click bars to highlight
- Useful for rankings

**Line Charts**
- Show trends over time
- Hover to see monthly values
- Multiple lines = multiple groups

**Scatter Plots**
- Show relationships between variables
- Each point = one observation
- Trend lines show patterns

**Error Bars**
- Show uncertainty/confidence intervals
- Wider bars = more uncertainty
- Used in airport comparison

## Key Concepts

### 1. Cancelled Flights - Selection Bias

**What to observe:**
- February has HIGH cancellations (3%+)
- February has LOW delays (compared to other winter months)

**Why?**
- High cancellations = flights in worst weather got cancelled
- Cancelled flights don't appear in delay stats
- You're only seeing "survivors" (flights that flew)

**The Lesson:**
- **Selection Bias:** Missing data isn't random
- Always ask: "What data am I NOT seeing?"

### 2. Manufacturers - Fleet Trends

**What to observe:**
- Boeing and Airbus dominate throughout the year
- Smaller manufacturers have lower volumes
- Seasonal patterns in flight volume

**The Lesson:**
- Different aircraft types have different uses
- Market dominated by major manufacturers

### 3. SFO Routes - Market Share

**What to observe:**
- United Airlines dominates (70%+ of flights)
- Other carriers have small share
- One airline clearly specializes in this route

**The Lesson:**
- Routes are dominated by specific carriers
- This matters for "confounding" in next sections

### 4. Weather Impact - Confounders

**Four Weather Dimensions:**

1. **Temperature**
   - Extreme temps (very cold/hot) correlate with delays
   - But: Winter also has holiday travel

2. **Visibility**
   - Poor visibility clearly increases delays
   - But: Rain/fog often happen in winter

3. **Wind Speed**
   - High winds correlate with delays
   - But: Strong winds are seasonal

4. **Precipitation**
   - Rainy days have noticeably higher delays
   - But: Rain in winter confounded with season

**The Lesson:**
- Weather CORRELATES with delays
- But other confounders exist (season, travel patterns, cancellations)
- Can we claim weather CAUSES delays? Not without controlling for confounders

### 5. Carrier Rankings - Confounding

**The Question:**
"Rank airlines by average delay"

**The Problem:**
- Different airlines fly different routes!
- Long-haul specialists might appear slower due to route difficulty
- Not comparing apples-to-apples

**The Observation:**
- Look at which airlines rank best/worst
- Note: You don't know these airlines' actual routes
- Different routes have different inherent delays

**The Lesson:**
- **Confounding:** Route difficulty confounds carrier performance
- Simple rankings are misleading
- Always ask: "What else could explain this?"

### 6. Delay Recovery - Flight Duration

**The Finding:**
- Departure delays < Arrival delays
- Points fall BELOW the diagonal line
- Pilots "make up time" in the air

**Why?**
- Short flights: Can't recover much delay
- Long flights: Hours in the air to catch up
- Longer flight = more recovery opportunity

**The Impact:**
- If you rank airlines by ARRIVAL delay, you bias toward longer routes
- Airlines with longer flights will appear better
- Flight duration CONFOUNDS the comparison

**The Lesson:**
- Different metrics measure different things
- Always be aware of confounders in your choice of metric

### 7. Simpson's Paradox - Time of Day

**The Overall Pattern:**
- Later flights have MORE delays
- Evening flights are worst

**By Carrier:**
- Some carriers: Pattern holds
- Other carriers: Pattern reverses!
- Different carriers have different route mixes

**Why?**
- Carrier A might fly short routes in evening (low delay)
- Carrier B might fly long routes in evening (high delay)
- Aggregate pattern doesn't hold for all subgroups

**The Lesson:**
- **Simpson's Paradox:** Check if patterns hold across subgroups!
- Aggregate conclusions can be wrong for specific groups

### 8. Plane Age - Correlation Not Causation

**The Question:**
"Do older planes cause delays?"

**The Observation:**
- Older planes show more delays
- Trend line shows positive relationship

**The Problem:**
- Causation is unclear!
- Could be:
  - Older planes fly harder routes (route bias)
  - Different maintenance practices (operator bias)
  - Selection bias (really old planes already retired)
  - Actual mechanical issues (true causation)

**The Lesson:**
- **Correlation ≠ Causation**
- Multiple explanations possible
- Need controlled experiments or more investigation

### 9. Airport Comparison - Stat vs Practical Sig

**The Numbers:**
- EWR: 13.1 min average delay
- JFK: 13.3 min average delay
- LGA: 12.6 min average delay

**Statistical Significance:**
- With 336k flights, differences ARE statistically significant
- p-value < 0.05 (very likely real, not random)

**Practical Significance:**
- Difference is ~1 minute
- Would YOU change airports to save 1 minute?
- Cost/convenience probably outweighs 1-minute difference

**The Lesson:**
- **Stat vs Practical:** Large data makes tiny differences "significant"
- Always ask: "Does this matter in practice?"
- Statistical significance ≠ Practical importance

## Tips & Tricks

### Making the Most of the Dashboard

#### Exploration Tips

1. **Start with Home** - Read the context
2. **Follow the flow** - Sections build on each other
3. **Read yellow boxes** - They highlight key lessons
4. **Interact with charts** - Hover, zoom, toggle

#### Chart Interaction Tips

- **Hover slowly** - Let tooltips appear fully
- **Double-click legend** - Isolate one data series
- **Zoom strategically** - Zoom on interesting regions
- **Use box select** - Select specific data points

#### Learning Tips

1. **Pause and reflect** - After each section, think about the lesson
2. **Ask yourself** - "Why is this pattern happening?"
3. **Consider alternatives** - "What else could explain this?"
4. **Take notes** - Write down key takeaways

### Keyboard Shortcuts

```
Arrow Keys (← →)  Navigate between sections
Hover            See exact values
Double-click     Reset zoom
Shift + Drag     Pan around chart
```

### Mobile Tips

- Dashboard works on phones/tablets
- Use portrait orientation for better viewing
- Tap and hold for tooltips
- Pinch to zoom on charts

## Frequently Asked Questions

### Q1: Why are cancelled flights important?

**A:** They show **selection bias**. Cancelled flights represent the WORST conditions but don't appear in delay analysis. You're only seeing "survivors."

### Q2: Why does weather correlate with delays if it doesn't cause them?

**A:** Multiple factors happen together:
- Bad weather in winter
- Winter also has holiday travel
- Both cause delays
- Weather might not be the direct cause

### Q3: Why are different carriers' statistics not comparable?

**A:** They fly different routes! Routes have different inherent delays due to:
- Distance
- Airport congestion
- Time zones
- Weather patterns
- Connecting complexity

### Q4: What's Simpson's Paradox?

**A:** When an overall trend reverses in subgroups. Example:
- Overall: Later flights = more delays ✓
- Carrier A: Later flights = fewer delays ✗
- Carrier B: Later flights = more delays ✓

### Q5: Can we say old planes cause delays?

**A:** Not definitively! Could be:
- Older planes fly different routes (confounding)
- Different maintenance (confounding)
- True mechanical issues (causation)
Need more investigation to determine cause.

### Q6: Why do 1-minute airport differences matter?

**A:** They don't! This teaches **statistical vs practical significance**:
- **Statistical:** Real difference, not random
- **Practical:** Too small to matter
- Large data makes tiny differences significant

### Q7: Can I download the data?

**A:** The HTML dashboard contains aggregated results. For raw data, use the [nycflights13](https://github.com/hadley/nycflights13) package.

### Q8: Can I modify the dashboard?

**A:** Yes! See the Python script `generate_dashboard_html.py` to:
- Change data source
- Modify analyses
- Update visualizations
- Customize styling

### Q9: Which sections are most important?

**A:** All sections build on each other:
1. Start with **Cancelled Flights** (selection bias)
2. Learn about **Confounding** (weather, carriers)
3. Understand **Simpson's Paradox** (subgroup reversal)
4. Internalize lessons in remaining sections

### Q10: How long should I spend on the dashboard?

**A:** 
- Quick overview: 10 minutes (skim all sections)
- Thorough understanding: 30 minutes (read all explanations)
- Deep learning: 1 hour+ (interact with charts, take notes)

## Next Steps

1. ✅ **Explore the dashboard** - Click through all sections
2. ✅ **Interact with charts** - Hover, zoom, download
3. ✅ **Reflect on lessons** - Think about your own data
4. ✅ **Apply concepts** - Use critical thinking in your work
5. ✅ **Share** - Tell others about data literacy!

---

**Happy exploring! If you have questions, check TROUBLESHOOTING.md**
