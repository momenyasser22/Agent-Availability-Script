# Data Directory

This directory stores the persistent SQLite database (`agent_baseline.db`) that contains baseline agent data.

## What is stored here?

- **agent_baseline.db** - SQLite database with:
  - `windows_agents` table
  - `linux_agents` table

## How is this populated?

1. Run the application: `python agent_availability.py`
2. Select option **[1]** to load Windows baseline
3. Select option **[2]** to load Linux baseline

## Persistence

- Database persists across script runs
- Database persists across Docker container restarts
- Loading new baseline **replaces** all existing data

## Important Notes

- **DO NOT manually edit this database** - Use the application menu
- **DO NOT delete** this file unless you want to reset all baseline data
- This file is excluded from git tracking (user data only)
