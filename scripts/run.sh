
    
  
#!/usr/bin/env bash

set -o pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"

mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/load_products_${TIMESTAMP}.log"

START_TIME=$(date +%s)

{
    echo "========================================"
    echo "LAB 1 - TIKI JSON -> POSTGRESQL"
    echo "========================================"
    echo "Started at: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Project dir: $PROJECT_DIR"
    echo "Log file: $LOG_FILE"
    echo "========================================"
    echo
} | tee -a "$LOG_FILE"

cd "$PROJECT_DIR" || exit 1

if [ -f "$PROJECT_DIR/venv/bin/activate" ]; then
    source "$PROJECT_DIR/venv/bin/activate"
else
    echo "ERROR: venv not found at $PROJECT_DIR/venv" | tee -a "$LOG_FILE"
    exit 1
fi

python3 -u load_products.py 2>&1 | tee -a "$LOG_FILE"
PIPE_STATUS=("${PIPESTATUS[@]}")
EXIT_CODE="${PIPE_STATUS[0]}"

END_TIME=$(date +%s)
RUNTIME=$((END_TIME - START_TIME))

HOURS=$((RUNTIME / 3600))
MINUTES=$(((RUNTIME % 3600) / 60))
SECONDS=$((RUNTIME % 60))

{
    echo
    echo "========================================"
    echo "LAB 1 FINISHED"
    echo "========================================"
    echo "Finished at: $(date '+%Y-%m-%d %H:%M:%S')"
    printf "Runtime: %02d:%02d:%02d\n" "$HOURS" "$MINUTES" "$SECONDS"
    echo "Exit code: $EXIT_CODE"
    echo "Log file: $LOG_FILE"
    echo "========================================"
} | tee -a "$LOG_FILE"

exit "$EXIT_CODE"


