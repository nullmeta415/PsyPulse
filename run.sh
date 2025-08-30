#!/bin/bash
echo "================================"
echo "   Running PsyPulse"
echo "================================"

# Step 1: Setup environment if not already done
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup_env.sh..."
    ./setup_env.sh "$1"
else
    echo "Virtual environment already exists. Skipping setup."
fi

# Step 2: Activate virtual environment
source .venv/bin/activate

# Step 3: Create logs folder if not exists
mkdir -p logs

# Step 4: Generate timestamp for log filename
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE="logs/run_$TIMESTAMP.log"

# Step 5: Run the app and log output
echo "Starting PsyPulse (logging to $LOGFILE)..."
python main.py | tee "$LOGFILE"
