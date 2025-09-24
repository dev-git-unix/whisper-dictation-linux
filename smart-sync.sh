#!/bin/bash

# === CONFIG ===
REPO_DIR="$(pwd)"
BRANCH="main"
TIMER=10
COUNTER_FILE="$REPO_DIR/.autosync_count"

cd "$REPO_DIR" || exit 1

# Initialize counter file if not present
if [ ! -f "$COUNTER_FILE" ]; then
    echo 1 > "$COUNTER_FILE"
fi

echo "🔄 [Smart Sync] Starting in $REPO_DIR on branch $BRANCH"

# Step 1: Always pull latest changes first
echo "📥 Pulling latest changes from origin/$BRANCH..."
git pull --rebase origin "$BRANCH"

# Step 2: Start watching for changes
echo "👀 Watching for file changes..."
fswatch -o . | while read; do
    echo "⌛ Change detected. Debouncing for $TIMER sec..."
    sleep "$TIMER"

    # Check for unstaged or uncommitted changes
    if [[ -n $(git status --porcelain) ]]; then
        # Update commit counter
        COUNT=$(cat "$COUNTER_FILE")
        NEXT_COUNT=$((COUNT + 1))
        echo "$NEXT_COUNT" > "$COUNTER_FILE"

        # Build commit message
        COMMIT_MSG="#$COUNT | Auto-sync: $(hostname) on $(date '+%Y-%m-%d %H:%M:%S')"

        echo "📦 Staging changes..."
        git add .

        echo "📝 Committing: $COMMIT_MSG"
        git commit -m "$COMMIT_MSG"

        echo "📥 Pulling remote (just in case)..."
        git pull --rebase origin "$BRANCH"

        echo "📤 Pushing to GitHub..."
        git push origin "$BRANCH"
    else
        echo "✅ No changes to commit. Waiting for next file event..."
    fi
done
