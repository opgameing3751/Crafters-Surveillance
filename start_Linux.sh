#!/bin/bash

# Start the Main.py file with Python

python3 --version
echo "waiting 5 seconds"
sleep 5
echo "Starting Main.py..."
python3 Main.py

# Optional: Log exit status
echo "Main.py exited with code $?"