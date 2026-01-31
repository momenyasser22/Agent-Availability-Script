# 📌 MASTER PROMPT — AGENT AVAILABILITY SCRIPT

## Role
You are a senior automation and data engineer.

## Objective
Generate a complete, production-ready script that calculates agent availability per **Domain** and **Operating System** using CSV inputs and a SQL database.

All requirements below are **mandatory**.  
Do **not** skip, simplify, or alter formats.

---

## 1️⃣ INPUT DATA — BASELINE (DATABASE CREATION)

The user provides **two baseline CSV files**:

- Windows baseline CSV  
- Linux baseline CSV  

Each baseline CSV contains **exactly two columns**:
Domain,Agent Name
Rules:
- No extra columns  
- Header names must match exactly  
- Data may span multiple domains  

---

## 2️⃣ DATABASE REQUIREMENTS

- Use **SQLite**
- Create **two tables**:
  - `windows_agents`
  - `linux_agents`

Each table must store:
- `domain`
- `agent_name`
- `operating_system`

---

## 3️⃣ SCRIPT MODES (CLI OPTIONS)

The script must support the following CLI options:

### Option 1: Create Windows Agent Database
- Input: Windows baseline CSV
- Action:
  - Clear existing Windows data
  - Insert all records from CSV

### Option 2: Create Linux Agent Database
- Input: Linux baseline CSV
- Action:
  - Clear existing Linux data
  - Insert all records from CSV

### Option 3: Check Availability
- Input:
  - Windows availability CSV
  - Linux availability CSV

Each availability CSV contains **exactly three columns**:
Agent Name,Domain,Available Date
---

## 4️⃣ AVAILABILITY RULES (CRITICAL)

An agent is **AVAILABLE** only if:

1. It exists in the baseline database  
2. It exists in the availability CSV  
3. `Available Date` is **within the last 24 hours** from execution time  

If **any rule fails**, the agent is **NOT AVAILABLE**.

---

## 5️⃣ AVAILABILITY CALCULATION

For **each Operating System and each Domain**:

- **Total Hosts** = count from baseline DB  
- **Available Hosts** = hosts meeting availability rules  
- **Unavailable Hosts** = baseline − available  

Availability percentage:(Available Hosts / Total Hosts) * 100
---

## 6️⃣ CONSOLE REPORT OUTPUT

For every **OS → Domain**, print:
Operating System: Windows
Domain: Domain1
Hosts Not Available:
	•	HOST01
	•	HOST02
Availability Percentage: 75%
Repeat for:
- All Windows domains
- All Linux domains

---

## 7️⃣ EXCEL REPORT (MANDATORY)

- Generate **one XLSX file**
- Two sheets:
  - Windows
  - Linux
- Columns:
  - Operating System
  - Domain
  - Agent Name
  - Availability Status
  - Last Available Date
- **Rows for NOT AVAILABLE hosts must be highlighted RED**

---

## 8️⃣ ERROR HANDLING (MANDATORY)

The script must fail fast with clear messages if:
- CSV headers are incorrect
- Required columns are missing
- CSV files are empty
- Dates are invalid or unparseable  

No silent failures.

---

## 9️⃣ CODE QUALITY REQUIREMENTS

- Modular functions for:
  - CSV parsing
  - Database creation
  - Availability evaluation
  - Reporting
- Clear inline comments
- CLI-runnable
- No hard-coded paths

---

## 🔟 REQUIRED TEST CASES (MUST BE INCLUDED)

Implement test cases for:

1. **100% availability**
2. **Missing agents**
3. **Availability older than 24 hours**
4. **Multiple domains and operating systems**
5. **Invalid CSV headers**
6. **Empty availability CSV**
7. **Database overwrite validation**

Each test must clearly state:
- Input
- Expected result

---

## 🔚 OUTPUT EXPECTATION

Generate:
- Full script
- Sample CSV files for testing
- Instructions on how to run each CLI mode

**Do not change formats.**  
**Do not simplify logic.**  
**Do not skip edge cases.**
