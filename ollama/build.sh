#!/usr/bin/env bash
# Build the governance-ai Ollama model
#
# Usage:
#   ./build.sh                    # Build with default base (llama3.1:8b)
#   ./build.sh mistral            # Build with Mistral base
#   ./build.sh --list             # List available base model options
#   ./build.sh --test             # Build and run a quick test
#
# Prerequisites:
#   - Ollama must be installed and running
#   - The base model will be pulled automatically if not present

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL_NAME="${GOVERNANCE_AI_MODEL_NAME:-governance-ai}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
DIM='\033[2m'
NC='\033[0m'

info()  { echo -e "${BLUE}$*${NC}"; }
ok()    { echo -e "${GREEN}$*${NC}"; }
err()   { echo -e "${RED}$*${NC}" >&2; }
dim()   { echo -e "${DIM}$*${NC}"; }

# Check ollama is available
check_ollama() {
    if ! command -v ollama &>/dev/null; then
        err "Error: ollama is not installed."
        echo "Install from: https://ollama.com"
        exit 1
    fi

    if ! ollama list &>/dev/null 2>&1; then
        err "Error: ollama is not running."
        echo "Start with: ollama serve"
        exit 1
    fi
}

# List available Modelfile variants
list_variants() {
    echo ""
    info "Available base model variants:"
    echo ""
    echo "  Modelfile          → llama3.1:8b  (default, best balance of quality and speed)"
    echo "  Modelfile.mistral  → mistral:7b   (good alternative, strong reasoning)"
    echo ""
    echo "Usage: $0 [variant]"
    echo "  $0              # uses Modelfile (llama3.1:8b)"
    echo "  $0 mistral      # uses Modelfile.mistral"
    echo ""
    echo "Custom base model:"
    echo "  Edit the FROM line in the Modelfile, then run: $0"
    echo ""
}

# Build the model
build_model() {
    local modelfile="$1"

    if [ ! -f "$modelfile" ]; then
        err "Error: Modelfile not found: $modelfile"
        exit 1
    fi

    local base_model
    base_model=$(grep '^FROM ' "$modelfile" | head -1 | awk '{print $2}')

    echo ""
    info "=== Governance AI — Ollama Model Builder ==="
    echo ""
    echo "  Model name:  $MODEL_NAME"
    echo "  Base model:  $base_model"
    echo "  Modelfile:   $modelfile"
    echo ""

    # Pull base model if needed
    if ! ollama list | grep -q "$base_model"; then
        info "Pulling base model: $base_model ..."
        ollama pull "$base_model"
        echo ""
    else
        dim "Base model $base_model already available"
    fi

    # Create the model
    info "Creating model: $MODEL_NAME ..."
    ollama create "$MODEL_NAME" -f "$modelfile"
    echo ""

    ok "Model '$MODEL_NAME' created successfully!"
    echo ""
    echo "  Run interactively:  ollama run $MODEL_NAME"
    echo "  Use in geister:     --model $MODEL_NAME"
    echo "  API:                curl http://localhost:11434/api/chat -d '{\"model\": \"$MODEL_NAME\", \"messages\": [{\"role\": \"user\", \"content\": \"What is syntropy?\"}]}'"
    echo ""
}

# Quick test
test_model() {
    info "Testing model: $MODEL_NAME ..."
    echo ""

    local test_prompt="In one paragraph, explain why love is the best survival strategy in an entropic universe."

    dim "Prompt: $test_prompt"
    echo ""

    ollama run "$MODEL_NAME" "$test_prompt"

    echo ""
    ok "Test complete."
}

# Main
main() {
    case "${1:-}" in
        --list|-l)
            list_variants
            exit 0
            ;;
        --help|-h)
            echo "Usage: $0 [variant|--list|--test]"
            exit 0
            ;;
        --test|-t)
            check_ollama
            test_model
            exit 0
            ;;
        mistral)
            check_ollama
            build_model "$SCRIPT_DIR/Modelfile.mistral"
            ;;
        "")
            check_ollama
            build_model "$SCRIPT_DIR/Modelfile"
            ;;
        *)
            local custom="$SCRIPT_DIR/Modelfile.$1"
            if [ -f "$custom" ]; then
                check_ollama
                build_model "$custom"
            else
                err "Unknown variant: $1"
                list_variants
                exit 1
            fi
            ;;
    esac
}

main "$@"
