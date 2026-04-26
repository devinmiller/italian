#!/usr/bin/env bash
# vocabolario_tools.sh - Utilities for managing Italian vocabulary YAML files.
#
# Requires: mikefarah yq (https://github.com/mikefarah/yq) v4.18+
#
# Usage:
#   ./vocabolario_tools.sh find-null-hints [DIRECTORY]
#   ./vocabolario_tools.sh list-words [DIRECTORY]
#   ./vocabolario_tools.sh count-entries [DIRECTORY]
#   ./vocabolario_tools.sh list-tags [--show-files] [DIRECTORY]

set -euo pipefail

# --- Helper Functions ---

check_yq() {
    if ! command -v yq >/dev/null 2>&1; then
        echo "Error: yq is not in PATH. Please install mikefarah/yq." >&2
        exit 1
    fi
}

get_dir() {
    local provided_dir="${1:-}"
    if [[ -n "$provided_dir" ]]; then
        echo "$provided_dir"
    else
        # Default to the directory where the script is located
        cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" && pwd
    fi
}

# --- Commands ---

# Command: find-null-hints
# Prints the filename (minus extension) for YAML files where 'hints' is null.
cmd_find_null_hints() {
    local dir
    dir=$(get_dir "${1:-}")
    
    if [[ ! -d "$dir" ]]; then
        echo "Error: Not a directory: $dir" >&2
        exit 1
    fi

    shopt -s nullglob
    for f in "$dir"/*.yaml; do
        local count
        count=$(yq e '[.. | select(type == "!!map" and has("hints") and .hints == null)] | length' "$f" 2>/dev/null || echo "0")
        
        if [[ "$count" -gt 0 ]]; then
            local filename
            filename=$(basename -- "$f")
            echo "${filename%.yaml}"
        fi
    done
}

# Command: list-words
# Lists the 'word' field from all YAML files in the directory.
cmd_list_words() {
    local dir
    dir=$(get_dir "${1:-}")
    
    shopt -s nullglob
    for f in "$dir"/*.yaml; do
        yq e '.word' "$f" 2>/dev/null || true
    done
}

# Command: count-entries
# Counts the number of YAML files in the directory.
cmd_count_entries() {
    local dir
    dir=$(get_dir "${1:-}")
    
    shopt -s nullglob
    local files=("$dir"/*.yaml)
    echo "${#files[@]}"
}

# Command: list-tags
# Lists unique tags found directly under the 'word' structure,
# showing how many files contain each tag and optionally which files.
cmd_list_tags() {
    local show_files=false
    local dir=""

    # Parse arguments for this command
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --show-files)
                show_files=true
                shift
                ;;
            *)
                dir="$1"
                shift
                ;;
        esac
    done

    dir=$(get_dir "$dir")
    
    if [[ ! -d "$dir" ]]; then
        echo "Error: Not a directory: $dir" >&2
        exit 1
    fi

    # Temporary file to store tag-file mappings
    local tmp_file
    tmp_file=$(mktemp)
    trap 'rm -f "$tmp_file"' EXIT

    shopt -s nullglob
    for f in "$dir"/*.yaml; do
        local filename
        filename=$(basename -- "$f")
        local name_no_ext="${filename%.yaml}"
        
        # Extract tags directly under the word/forms structure.
        # Based on the schema, tags are often at .[].forms[].tags
        # We'll use yq to get all tags at that level.
        yq e '.[].forms[].tags[]' "$f" 2>/dev/null | while read -r tag; do
            if [[ -n "$tag" ]]; then
                echo "$tag|$name_no_ext" >> "$tmp_file"
            fi
        done
    done

    if [[ ! -s "$tmp_file" ]]; then
        echo "No tags found."
        return
    fi

    # Process the temporary file to get unique tags and counts
    # Format: tag|file1,file2...
    sort -u "$tmp_file" | awk -F'|' -v show="$show_files" '
    {
        tags[$1]++
        if (show == "true") {
            if (files[$1] == "") files[$1] = $2
            else files[$1] = files[$1] "\n    - " $2
        }
    }
    END {
        # Sort tags alphabetically
        n = asorti(tags, sorted_tags)
        for (i = 1; i <= n; i++) {
            t = sorted_tags[i]
            if (show == "true") {
                printf "### %s (%d files):\n    - %s\n\n", t, tags[t], files[t]
            } else {
                printf "%-20s (%d files)\n", t, tags[t]
            }
        }
    }'

    rm -f "$tmp_file"
    trap - EXIT
}

# --- Main Entry Point ---

usage() {
    echo "Usage: $0 <command> [options] [directory]"
    echo ""
    echo "Commands:"
    echo "  find-null-hints             List files (no extension) with null hints"
    echo "  list-words                  List the 'word' value from all files"
    echo "  count-entries               Count total YAML files"
    echo "  list-tags [--show-files]    List unique tags and their frequency"
    exit 1
}

if [[ $# -lt 1 ]]; then
    usage
fi

check_yq

command_name="$1"
shift || true

case "$command_name" in
    find-null-hints)
        cmd_find_null_hints "${1:-}"
        ;;
    list-words)
        cmd_list_words "${1:-}"
        ;;
    count-entries)
        cmd_count_entries "${1:-}"
        ;;
    list-tags)
        cmd_list_tags "$@"
        ;;
    *)
        echo "Error: Unknown command '$command_name'" >&2
        usage
        ;;
esac
