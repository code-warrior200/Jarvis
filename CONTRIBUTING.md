# Contributing to JARVIS

First off, thank you for considering contributing to JARVIS! It's people like you that make JARVIS such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python/styleguides
* Include appropriate test cases
* End all files with a newline

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (venv)

### Local Development

1. **Fork and Clone**
```bash
git clone https://github.com/yourusername/jarvis.git
cd jarvis
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

3. **Install Dependencies**
```bash
make install-dev
```

4. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

5. **Make Changes**
```bash
# Write your code
# Add tests for new features
# Update documentation
```

6. **Run Tests**
```bash
make test
```

7. **Format Code**
```bash
make format
make lint
```

8. **Commit and Push**
```bash
git add .
git commit -m "feat: Your feature description"
git push origin feature/your-feature-name
```

## Styleguides

### Python Code Style

We follow **PEP 8** with these additions:

```python
# Use type hints
def handle_command(self, text: str) -> str:
    """Process a voice command."""
    pass

# Use meaningful variable names
user_input = ""  # Good
ui = ""          # Bad

# Comment complex logic
# Threshold prevents false positives in noisy environments
if confidence < 0.7:
    continue

# Use docstrings for all functions
def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts.
    
    Args:
        text1: First text string
        text2: Second text string
        
    Returns:
        Similarity score between 0 and 1
    """
    pass
```

### Git Commit Messages

```bash
# Use the present tense ("add feature" not "added feature")
# Use the imperative mood ("move cursor to..." not "moves cursor to...")
# Limit the first line to 72 characters or less
# Reference issues and pull requests liberally after the first line

# Good examples:
git commit -m "feat: Add voice command processing"
git commit -m "fix: Handle microphone not found error"
git commit -m "docs: Update installation guide"
git commit -m "refactor: Extract window management to separate class"
```

### Documentation Style

* Use Markdown format
* Include code examples
* Add table of contents for long docs
* Use clear, concise language
* Include screenshots when helpful

## Project Structure

```
src/
├── core/           # Business logic
├── ui/             # User interface
└── utils/          # Utility functions

tests/
├── test_core.py    # Core tests
├── test_gui.py     # GUI tests
└── test_utils.py   # Utility tests

docs/               # Documentation
```

## Testing

### Writing Tests

```python
import pytest
from jarvis.core import Jarvis

class TestJarvis:
    def setup_method(self):
        """Setup test fixtures"""
        self.jarvis = Jarvis()
    
    def test_initialization(self):
        """Test Jarvis initialization"""
        assert self.jarvis is not None
        assert self.jarvis.is_listening is False
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_core.py

# Run with coverage
make coverage

# Run with verbose output
pytest -v
```

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested
* `wontfix` - This will not be worked on

### Recognition

We recognize contributors in:
* README.md
* GitHub Contributors page
* Release notes

## Questions?

Feel free to open an issue with the `question` label or check out our documentation.

## License

By contributing to JARVIS, you agree that your contributions will be licensed under its MIT License.

---

**Thank you for contributing!** 🎉
