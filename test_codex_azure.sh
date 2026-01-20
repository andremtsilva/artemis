#!/bin/bash
# Test script to verify Rust codex binary works with Azure OpenAI

echo "=========================================="
echo "Testing Codex Binary with Azure OpenAI"
echo "=========================================="
echo ""

# Check if environment variables are set
echo "✓ Checking environment variables..."
if [ -z "$AZURE_OPENAI_API_KEY" ]; then
    echo "  ✗ AZURE_OPENAI_API_KEY not set"
    echo "  Run: source .env or export AZURE_OPENAI_API_KEY=your-key"
    exit 1
fi
echo "  ✓ AZURE_OPENAI_API_KEY is set"

if [ -z "$AZURE_OPENAI_ENDPOINT" ]; then
    echo "  ✗ AZURE_OPENAI_ENDPOINT not set"
    exit 1
fi
echo "  ✓ AZURE_OPENAI_ENDPOINT: $AZURE_OPENAI_ENDPOINT"

SUBAGENT_MODEL="${SUBAGENT_MODEL:-gpt-5.1-codex-mini}"
echo "  ✓ SUBAGENT_MODEL: $SUBAGENT_MODEL"

# Check if config.toml exists
echo ""
echo "✓ Checking codex configuration..."
if [ ! -f ~/.codex/config.toml ]; then
    echo "  ✗ ~/.codex/config.toml not found!"
    exit 1
fi
echo "  ✓ ~/.codex/config.toml exists"

# Check if codex binary exists
echo ""
echo "✓ Checking codex binary..."
CODEX_BINARY="./codex-rs/target/release/codex"
if [ ! -f "$CODEX_BINARY" ]; then
    echo "  ✗ Codex binary not found at $CODEX_BINARY"
    echo "  Build it with: cargo build --release --manifest-path codex-rs/Cargo.toml"
    exit 1
fi
echo "  ✓ Codex binary found"

# Test the codex binary
echo ""
echo "✓ Testing codex binary with Azure OpenAI..."
echo "  Running: codex --model-provider azure --model $SUBAGENT_MODEL 'Say hello'"
echo ""

$CODEX_BINARY --model-provider azure --model "$SUBAGENT_MODEL" "Say 'Azure OpenAI is working with codex binary!' if you can read this"

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! Codex binary works with Azure!"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "❌ FAILED - Check the error above"
    echo "=========================================="
    echo ""
    echo "Common issues:"
    echo "1. Wrong deployment name in SUBAGENT_MODEL"
    echo "2. Wrong base_url in ~/.codex/config.toml (should end with /openai)"
    echo "3. Invalid API key"
    exit 1
fi
