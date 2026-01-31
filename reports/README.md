# Reports Directory

This directory stores generated availability reports.

## Report Formats

Reports are generated in two formats:

### 1. Excel Report (`.xlsx`)
- Separate sheets for Windows and Linux agents
- RED highlighting for unavailable agents
- Domain and Agent Name columns
- Last Available Date and Status columns

### 2. Word Report (`.docx`)
- Tables organized by OS Type and Domain
- Availability percentage for each Domain/OS combination
- Detailed agent listings with availability status

## Availability Rules

An agent is considered **Available** if it meets ALL criteria:
1. Exists in the baseline database
2. Exists in the availability CSV file
3. Has a "Last Available Date" within the last 24 hours

## Important Notes

- **DO NOT** manually edit these files
- Reports are generated automatically by the application
- These files are excluded from git tracking (user data only)
- Reports persist across Docker container restarts
