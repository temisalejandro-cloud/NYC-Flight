# Contributing to NYC Flights Analysis Dashboard

First off, thanks for taking the time to contribute! ❤️

This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please read and abide by our Code of Conduct.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing opinions and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community

### Unacceptable Behavior

- Use of sexualized language or imagery
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct inappropriate for a professional setting

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating a bug report, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment** (OS, browser, Python version, etc.)

### Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests 🚀

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include appropriate test cases
* Document any new features
* Keep commits clean and organized
* Update documentation as needed

## Development Setup

### Prerequisites
- Python 3.7+
- Git
- pip or conda

### Setting Up Your Development Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/nyc-flights-analysis.git
   cd nyc-flights-analysis
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Make your changes**
   ```bash
   # Edit files as needed
   ```

7. **Test your changes**
   ```bash
   python generate_dashboard_html.py
   # Open dashboard_with_charts.html in browser to verify
   ```

8. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add description of your changes"
   ```

9. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

10. **Create a Pull Request**
    - Go to GitHub and click "New Pull Request"
    - Fill in the PR template
    - Submit!

## Style Guide

### Python Code Style

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.

```python
# Good
def calculate_average_delay(flights_data):
    """Calculate average departure delay in minutes."""
    return flights_data['dep_delay'].mean()

# Bad
def calcAvgDelay(fd):
    return fd['dep_delay'].mean()
```

### Commit Messages

- Use the imperative mood ("Add feature" not "Added feature")
- Limit the first line to 72 characters
- Reference issues and pull requests liberally after the first line
- Consider starting with an emoji:
  - 🎨 for style/formatting changes
  - 📝 for documentation
  - 🐛 for bug fixes
  - ✨ for new features
  - 🔧 for configuration
  - 📊 for data/analysis changes

Examples:
```
✨ Add new weather analysis section
📝 Update README with troubleshooting guide
🐛 Fix chart rendering on mobile
🔧 Update requirements.txt versions
```

### Documentation

- Use clear, concise language
- Include code examples where appropriate
- Keep documentation up to date with code changes
- Use markdown for README and guides

## Areas for Contribution

### 📊 Data & Analysis
- [ ] Add new analyses
- [ ] Improve data processing
- [ ] Add more visualizations
- [ ] Optimize performance

### 📖 Documentation
- [ ] Expand guides and tutorials
- [ ] Add more examples
- [ ] Improve explanations
- [ ] Translate to other languages

### 🎨 Frontend
- [ ] Improve UI/UX
- [ ] Enhance responsiveness
- [ ] Add dark mode
- [ ] Improve accessibility

### 🔧 Development
- [ ] Add unit tests
- [ ] Improve error handling
- [ ] Refactor code
- [ ] Optimize algorithms

### 🌍 Community
- [ ] Share the project
- [ ] Help others with issues
- [ ] Write blog posts
- [ ] Create video tutorials

## Pull Request Process

1. Ensure any install or build dependencies are removed
2. Update the README.md with details of changes if applicable
3. Increase version numbers if applicable
4. Write clear commit messages
5. Request review from maintainers
6. Address any feedback or changes requested

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested
* `wontfix` - This will not be worked on

### Project Structure

```
nyc-flights-analysis/
├── dashboard_with_charts.html      # Main interactive dashboard
├── generate_dashboard_html.py      # Generator script
├── requirements.txt                # Dependencies
├── README.md                       # Main documentation
├── LICENSE                         # MIT License
├── .gitignore                     # Git ignore rules
├── docs/                          # Documentation folder
│   ├── GUIDE.md
│   ├── CONCEPTS.md
│   ├── DATA_DICTIONARY.md
│   └── TROUBLESHOOTING.md
└── data/                          # Data folder (to be added)
    ├── flights.csv
    ├── airlines.csv
    ├── airports.csv
    ├── planes.csv
    └── weather.csv
```

### Running Tests

```bash
# Generate dashboard with current code
python generate_dashboard_html.py

# Open in browser and verify:
open dashboard_with_charts.html
```

## Questions?

Don't hesitate to ask! You can:
- 📖 Read the [documentation](docs/)
- 💬 Open an issue with your question
- 📧 Contact the maintainers

---

Thank you for contributing! 🎉
