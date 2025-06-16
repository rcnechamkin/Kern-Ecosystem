#!/bin/bash

echo "=== Kern Ecosystem Daemons ==="
echo ""

TIMER_LIST=("lastfm_fetcher" "blackbox")

for name in "${TIMER_LIST[@]}"; do
    echo -n "["
    if systemctl --user is-active --quiet "$name.timer"; then
        echo -n "Active"
    else
        echo -n "Inactive"
    fi
    echo "] $name.timer"

    last_run=$(journalctl --user -u "$name.service" --no-pager --reverse --output=short-unix | grep -m 1 "Starting" | cut -d' ' -f1)
    if [ -n "$last_run" ]; then
        echo "  ↪ Last run: $(date -d @$last_run)"
    fi

    next_run=$(systemctl --user list-timers | grep "$name.timer" | awk '{print $1, $2}')
    if [ -n "$next_run" ]; then
        echo "  ↪ Next run: $next_run"
    fi

    echo "  ↪ Status: $(systemctl --user show -p ActiveState --value "$name.timer")"
    echo ""

    echo "$name.service recent output:"
    journalctl --user -n 5 -u "$name.service" --no-pager | sed 's/^/  ▸ /'
    echo ""
done

echo "All Kern monitors complete."
