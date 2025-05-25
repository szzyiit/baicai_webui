# Baicai WebUI

A modern web interface for the Baicai AI agent system, built with Streamlit.

## Overview

Baicai WebUI provides an intuitive and interactive web interface for interacting with the Baicai AI agent system. It offers visualization capabilities for agent workflows, real-time interaction with AI agents, and a user-friendly environment for managing and monitoring agent activities.

## Features

- 🎨 Modern, responsive web interface built with Streamlit
- 📊 Interactive workflow visualization with Mermaid diagrams
- 🔄 Real-time agent interaction and monitoring
- 📈 Flow-based agent workflow visualization
- 🔌 Seamless integration with Baicai Base framework

## Requirements

- Python 3.10 or higher (but less than 3.12)
- Poetry for dependency management
- Baicai Base package installed

## Installation(Not really like this)

1. Ensure you have Baicai Base installed:

```bash
cd ../baicai_base
poetry install
```

2. Install Baicai WebUI:

```bash
cd ../baicai_webui
poetry install
```

3. Set up your environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

1. Activate the virtual environment:

```bash
poetry shell
```

2. Start the web interface:

```bash
baicai-webui
```

Or alternatively:

```bash
streamlit run baicai_webui/app.py
```

## Development

### Setup Development Environment

1. Install development dependencies:

```bash
poetry install --with dev
```

2. Run tests:

```bash
pytest
```

### Project Structure

```
baicai_webui/
├── baicai_webui/    # Main package directory
│   ├── app.py       # Main Streamlit application
│   ├── components/  # UI components
│   └── utils/       # Utility functions
├── docs/            # Documentation
├── tests/           # Test files
└── pyproject.toml   # Project configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## License

This project is licensed under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) License.
