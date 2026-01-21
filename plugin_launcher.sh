#!/usr/bin/env bash
# cosmographia.sh
# Runs Cosmographia with selectable subcommands and persistent COSMO_PATH.

export LC_ALL="en_US.UTF-8"

CONFIG_FILE="$HOME/.cosmo_path"

show_help() {
    echo "Usage: $(basename "$0") [OPTION]"
    echo
    echo "Run Cosmographia plugin or one of its related commands."
    echo
    echo "Options:"
    echo "  juice_ptr     JUICE pointing request plugin"
    echo "  juice_mk      JUICE metakernel loader plugin"
    echo "  cosmo_main    Multi-mission plugin (default)"
    echo "  stardb        Run the stardb database utility"
    echo
    echo "If this is your first time running the script, you’ll be prompted"
    echo "to enter the path where Cosmographia is installed."
    echo
}

# Detect platform
OS_TYPE="$(uname -s)"
case "$OS_TYPE" in
    Darwin*)
        PLATFORM="macos"
        ;;
    Linux*)
        PLATFORM="linux"
        ;;
    *)
        echo "Unsupported OS: $OS_TYPE"
        exit 1
        ;;
esac

# Load or set COSMO_PATH
if [ -z "$COSMO_PATH" ]; then
    if [ -f "$CONFIG_FILE" ]; then
        COSMO_PATH=$(cat "$CONFIG_FILE")
    else
        echo "COSMO_PATH is not set."
        read -rp "Please enter the full path to the Cosmographia directory: " COSMO_PATH

        if [ "$PLATFORM" = "macos" ]; then
            EXECUTABLE="$COSMO_PATH/Cosmographia.app/Contents/MacOS/Cosmographia"
        else
            EXECUTABLE="$COSMO_PATH/Cosmographia.sh"
        fi

        if [ ! -x "$EXECUTABLE" ]; then
            echo "Error: Cosmographia executable not found at that location."
            exit 1
        fi

        echo "$COSMO_PATH" > "$CONFIG_FILE"
        echo "Saved COSMO_PATH to $CONFIG_FILE"
    fi
fi

# Handle arguments
CMD="$1"

case "$CMD" in
    juice_ptr)
        PY_SCRIPT="juice_ptr.py"
        ;;
    juice_mk)
        PY_SCRIPT="juice_mk.py"
        ;;
    cosmo_main|"")
        PY_SCRIPT="cosmo_main.py"
        ;;
    stardb)
         PY_SCRIPT="stardb_conf.py"
        ;;
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        echo "Error: Unknown option '$CMD'"
        show_help
        exit 1
        ;;
esac


if [ "$PLATFORM" = "macos" ]; then
    EXECUTABLE="$COSMO_PATH/Cosmographia.app/Contents/MacOS/Cosmographia"
else
    EXECUTABLE="$COSMO_PATH/Cosmographia.sh"
fi


# Run the selected command
echo "Launching Cosmographia"
FOLDER=`pwd`
"$EXECUTABLE" -p "${FOLDER}/${PY_SCRIPT}"

