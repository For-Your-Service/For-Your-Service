#!/bin/bash
# Quick start script for new developers

echo "🚀 For Your Service - Quick Start"
echo "=================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 required"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git required"; exit 1; }
echo "✅ Prerequisites OK"
echo ""

# Clone repository
if [ ! -d ".git" ]; then
    echo "📥 Cloning repository..."
    git clone https://github.com/For-Your-Service/For-Your-Service.git
    cd For-Your-Service
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment
echo "⚙️  Setting up environment..."
cp .env.example .env
echo "Edit .env with your API keys"

# Run tests
echo ""
echo "🧪 Running tests..."
pytest tests/unit/ -v

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with API credentials"
echo "2. Configure Databricks CLI"
echo "3. Run: make test"
echo ""
