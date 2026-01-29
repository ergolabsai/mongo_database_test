#!/bin/bash

# Formula Database Setup Script
# Automates the installation and setup process

echo "================================================"
echo "Formula Database MongoDB Setup"
echo "================================================"
echo

# Check Python version
echo "1. Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "   Found: $python_version"

# Check if MongoDB is installed
echo
echo "2. Checking MongoDB installation..."
if command -v mongod &> /dev/null; then
    echo "   ✓ MongoDB is installed"
    mongod --version | head -n 1
else
    echo "   ✗ MongoDB not found"
    echo
    echo "   Please install MongoDB:"
    echo "   - macOS: brew install mongodb-community"
    echo "   - Ubuntu: sudo apt-get install mongodb"
    echo "   - Or use MongoDB Atlas: https://www.mongodb.com/cloud/atlas"
    echo
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install Python dependencies
echo
echo "3. Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "   ✓ Dependencies installed"
else
    echo "   ✗ Failed to install dependencies"
    exit 1
fi

# Check MongoDB connection
echo
echo "4. Testing MongoDB connection..."
python3 -c "
from db_config import MongoDBConnection
try:
    mongo = MongoDBConnection()
    mongo.connect()
    mongo.close()
    print('   ✓ Successfully connected to MongoDB')
except Exception as e:
    print(f'   ✗ Connection failed: {e}')
    print()
    print('   Make sure MongoDB is running:')
    print('   - Local: brew services start mongodb-community')
    print('   - Or set MONGODB_URI environment variable')
    exit(1)
"

if [ $? -ne 0 ]; then
    exit 1
fi

# Run migration
echo
echo "5. Running migration..."
echo "   This will populate the database with your formulas..."
echo
read -p "   Proceed with migration? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 migrate.py
    
    if [ $? -eq 0 ]; then
        echo
        echo "   ✓ Migration completed successfully"
    else
        echo
        echo "   ✗ Migration failed"
        exit 1
    fi
else
    echo "   Skipped migration"
fi

# Success message
echo
echo "================================================"
echo "✓ Setup Complete!"
echo "================================================"
echo
echo "Next steps:"
echo "  1. Try the CLI:       python3 cli.py"
echo "  2. Run examples:      python3 examples.py"
echo "  3. Test MCP:          python3 mcp_integration.py"
echo
echo "Documentation: See README.md"
echo
