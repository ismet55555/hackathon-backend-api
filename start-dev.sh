#!/usr/bin/env sh

###################################################################
# Start server in DEVELOPMENT mode
###################################################################

set -e

set_default_module_name() {
    if [ -f /app/app/main.py ]; then
        DEFAULT_MODULE_NAME="app.main"
    elif [ -f /app/main.py ]; then
        DEFAULT_MODULE_NAME="main"
    elif [ -f ./app/main.py ]; then
        DEFAULT_MODULE_NAME="app.main"
    else
        echo "No module found"
        exit 1
    fi
}

set_environment_variables() {
    export APP_ENV="dev"
    MODULE_NAME="${MODULE_NAME:-$DEFAULT_MODULE_NAME}"
    VARIABLE_NAME="${VARIABLE_NAME:-app}"
    export APP_MODULE="${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}"

    export HOST="${HOST:-127.0.0.1}"
    export PORT="${PORT:-9500}"
    export LOG_LEVEL="${LOG_LEVEL:-debug}"
}

run_pre_start_script() {
    PRE_START_PATH="${PRE_START_PATH:-/app/prestart.sh}"
    echo "Checking for script in $PRE_START_PATH"

    if [ -f "$PRE_START_PATH" ]; then
        echo "Running script $PRE_START_PATH"
        . "$PRE_START_PATH"
    else
        echo "There is no script $PRE_START_PATH"
    fi
}

start_uvicorn() {
    echo $LOG_LEVEL
    exec uvicorn \
        --reload \
        --host "$HOST" \
        --port "$PORT" \
        --log-level "$LOG_LEVEL" \
        "$APP_MODULE"
}

main() {
    set_default_module_name
    set_environment_variables
    # run_pre_start_script
    start_uvicorn
}

main
