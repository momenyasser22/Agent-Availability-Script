#!/usr/bin/env python3
"""
Test Cases for Agent Availability Script

This module contains test cases for the agent availability script.
Each test case includes:
- Input description
- Expected result
"""

import csv
import unittest
import tempfile
import os
from pathlib import Path
from datetime import datetime, timedelta
import shutil

import agent_availability as aa


class TestAgentAvailability(unittest.TestCase):
    """Test cases for agent availability functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = Path(self.temp_dir) / "test_agents.db"

        # Override the DB_FILE constant for testing
        aa.DB_FILE = str(self.test_db_path)

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        if Path(self.test_db_path).exists():
            Path(self.test_db_path).unlink()
        shutil.rmtree(self.temp_dir)

    # ========== TEST CASE 1: 100% Availability ==========

    def test_100_percent_availability(self):
        """
        TEST CASE 1: 100% availability

        INPUT:
        - Baseline: 3 Windows agents, 2 Linux agents
        - Availability: All agents with current timestamp

        EXPECTED RESULT:
        - All agents marked as Available
        - Availability percentage: 100%
        """
        # Create baseline files
        windows_baseline = Path(self.temp_dir) / "windows_baseline.csv"
        linux_baseline = Path(self.temp_dir) / "linux_baseline.csv"

        with open(windows_baseline, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.BASELINE_COLUMNS)
            writer.writerow(["Domain1", "WIN-HOST01"])
            writer.writerow(["Domain1", "WIN-HOST02"])
            writer.writerow(["Domain2", "WIN-HOST03"])

        with open(linux_baseline, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.BASELINE_COLUMNS)
            writer.writerow(["Domain1", "LIN-HOST01"])
            writer.writerow(["Domain1", "LIN-HOST02"])

        # Load baselines
        aa.create_database()
        aa.load_baseline_windows(windows_baseline)
        aa.load_baseline_linux(linux_baseline)

        # Create availability files with current timestamps
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        windows_avail = Path(self.temp_dir) / "windows_avail.csv"
        linux_avail = Path(self.temp_dir) / "linux_avail.csv"

        with open(windows_avail, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.AVAILABILITY_COLUMNS)
            writer.writerow(["WIN-HOST01", "Domain1", now])
            writer.writerow(["WIN-HOST02", "Domain1", now])
            writer.writerow(["WIN-HOST03", "Domain2", now])

        with open(linux_avail, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.AVAILABILITY_COLUMNS)
            writer.writerow(["LIN-HOST01", "Domain1", now])
            writer.writerow(["LIN-HOST02", "Domain1", now])

        # Check availability
        windows_baseline_data = aa.get_baseline_agents(aa.WINDOWS_TABLE)
        linux_baseline_data = aa.get_baseline_agents(aa.LINUX_TABLE)
        windows_avail_data = aa.get_availability_records(windows_avail)
        linux_avail_data = aa.get_availability_records(linux_avail)

        windows_results = aa.calculate_availability(windows_baseline_data, windows_avail_data)
        linux_results = aa.calculate_availability(linux_baseline_data, linux_avail_data)

        # Assertions
        self.assertEqual(len(windows_results["Domain1"]["available"]), 2)
        self.assertEqual(len(windows_results["Domain1"]["not_available"]), 0)
        self.assertEqual(len(windows_results["Domain2"]["available"]), 1)
        self.assertEqual(len(windows_results["Domain2"]["not_available"]), 0)

        self.assertEqual(len(linux_results["Domain1"]["available"]), 2)
        self.assertEqual(len(linux_results["Domain1"]["not_available"]), 0)

    # ========== TEST CASE 2: Missing Agents ==========

    def test_missing_agents(self):
        """
        TEST CASE 2: Missing agents

        INPUT:
        - Baseline: 3 Windows agents
        - Availability: Only 2 agents present (1 missing)

        EXPECTED RESULT:
        - Missing agent marked as Not Available
        - Availability percentage: 66.7% (2/3)
        """
        windows_baseline = Path(self.temp_dir) / "windows_baseline.csv"

        with open(windows_baseline, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.BASELINE_COLUMNS)
            writer.writerow(["Domain1", "WIN-HOST01"])
            writer.writerow(["Domain1", "WIN-HOST02"])
            writer.writerow(["Domain1", "WIN-HOST03"])

        aa.create_database()
        aa.load_baseline_windows(windows_baseline)

        # WIN-HOST02 is missing from availability
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        windows_avail = Path(self.temp_dir) / "windows_avail.csv"

        with open(windows_avail, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.AVAILABILITY_COLUMNS)
            writer.writerow(["WIN-HOST01", "Domain1", now])
            writer.writerow(["WIN-HOST03", "Domain1", now])

        windows_baseline_data = aa.get_baseline_agents(aa.WINDOWS_TABLE)
        windows_avail_data = aa.get_availability_records(windows_avail)
        windows_results = aa.calculate_availability(windows_baseline_data, windows_avail_data)

        # Assertions
        self.assertEqual(len(windows_results["Domain1"]["available"]), 2)
        self.assertEqual(len(windows_results["Domain1"]["not_available"]), 1)
        self.assertIn("WIN-HOST02", windows_results["Domain1"]["not_available"])

    # ========== TEST CASE 3: Availability Older Than 24 Hours ==========

    def test_availability_older_than_24_hours(self):
        """
        TEST CASE 3: Availability older than 24 hours

        INPUT:
        - Baseline: 3 Windows agents
        - Availability: 1 agent with timestamp 25 hours ago

        EXPECTED RESULT:
        - Agent with old timestamp marked as Not Available
        - Availability percentage: 33.3% (1/3)
        """
        windows_baseline = Path(self.temp_dir) / "windows_baseline.csv"

        with open(windows_baseline, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.BASELINE_COLUMNS)
            writer.writerow(["Domain1", "WIN-HOST01"])
            writer.writerow(["Domain1", "WIN-HOST02"])
            writer.writerow(["Domain1", "WIN-HOST03"])

        aa.create_database()
        aa.load_baseline_windows(windows_baseline)

        # WIN-HOST02 has timestamp 25 hours ago
        now = datetime.now()
        old_time = (now - timedelta(hours=25)).strftime("%Y-%m-%d %H:%M:%S")
        recent_time = now.strftime("%Y-%m-%d %H:%M:%S")

        windows_avail = Path(self.temp_dir) / "windows_avail.csv"

        with open(windows_avail, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.AVAILABILITY_COLUMNS)
            writer.writerow(["WIN-HOST01", "Domain1", recent_time])
            writer.writerow(["WIN-HOST02", "Domain1", old_time])
            writer.writerow(["WIN-HOST03", "Domain1", recent_time])

        windows_baseline_data = aa.get_baseline_agents(aa.WINDOWS_TABLE)
        windows_avail_data = aa.get_availability_records(windows_avail)
        windows_results = aa.calculate_availability(windows_baseline_data, windows_avail_data)

        # Assertions
        self.assertEqual(len(windows_results["Domain1"]["available"]), 2)
        self.assertEqual(len(windows_results["Domain1"]["not_available"]), 1)
        self.assertIn("WIN-HOST02", windows_results["Domain1"]["not_available"])

    # ========== TEST CASE 4: Multiple Domains and Operating Systems ==========

    def test_multiple_domains_and_operating_systems(self):
        """
        TEST CASE 4: Multiple domains and operating systems

        INPUT:
        - Windows: 3 domains with 2 agents each
        - Linux: 2 domains with 3 agents each
        - Mixed availability across all

        EXPECTED RESULT:
        - Correct calculations for each OS/Domain combination
        - 6 Windows results (3 domains)
        - 6 Linux results (2 domains)
        """
        windows_baseline = Path(self.temp_dir) / "windows_baseline.csv"
        linux_baseline = Path(self.temp_dir) / "linux_baseline.csv"

        with open(windows_baseline, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.BASELINE_COLUMNS)
            writer.writerow(["Domain1", "WIN-HOST01"])
            writer.writerow(["Domain1", "WIN-HOST02"])
            writer.writerow(["Domain2", "WIN-HOST03"])
            writer.writerow(["Domain2", "WIN-HOST04"])
            writer.writerow(["Domain3", "WIN-HOST05"])
            writer.writerow(["Domain3", "WIN-HOST06"])

        with open(linux_baseline, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.BASELINE_COLUMNS)
            writer.writerow(["DomainA", "LIN-HOST01"])
            writer.writerow(["DomainA", "LIN-HOST02"])
            writer.writerow(["DomainA", "LIN-HOST03"])
            writer.writerow(["DomainB", "LIN-HOST04"])
            writer.writerow(["DomainB", "LIN-HOST05"])
            writer.writerow(["DomainB", "LIN-HOST06"])

        aa.create_database()
        aa.load_baseline_windows(windows_baseline)
        aa.load_baseline_linux(linux_baseline)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        windows_avail = Path(self.temp_dir) / "windows_avail.csv"
        linux_avail = Path(self.temp_dir) / "linux_avail.csv"

        with open(windows_avail, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.AVAILABILITY_COLUMNS)
            # Domain1: all available
            writer.writerow(["WIN-HOST01", "Domain1", now])
            writer.writerow(["WIN-HOST02", "Domain1", now])
            # Domain2: 1 available
            writer.writerow(["WIN-HOST03", "Domain2", now])
            # Domain3: none available
            pass

        with open(linux_avail, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.AVAILABILITY_COLUMNS)
            # DomainA: 2 available
            writer.writerow(["LIN-HOST01", "DomainA", now])
            writer.writerow(["LIN-HOST02", "DomainA", now])
            # DomainB: all available
            writer.writerow(["LIN-HOST04", "DomainB", now])
            writer.writerow(["LIN-HOST05", "DomainB", now])
            writer.writerow(["LIN-HOST06", "DomainB", now])

        windows_baseline_data = aa.get_baseline_agents(aa.WINDOWS_TABLE)
        linux_baseline_data = aa.get_baseline_agents(aa.LINUX_TABLE)
        windows_avail_data = aa.get_availability_records(windows_avail)
        linux_avail_data = aa.get_availability_records(linux_avail)

        windows_results = aa.calculate_availability(windows_baseline_data, windows_avail_data)
        linux_results = aa.calculate_availability(linux_baseline_data, linux_avail_data)

        # Assertions for Windows
        self.assertEqual(len(windows_results["Domain1"]["available"]), 2)
        self.assertEqual(len(windows_results["Domain1"]["not_available"]), 0)
        self.assertEqual(len(windows_results["Domain2"]["available"]), 1)
        self.assertEqual(len(windows_results["Domain2"]["not_available"]), 1)
        self.assertEqual(len(windows_results["Domain3"]["available"]), 0)
        self.assertEqual(len(windows_results["Domain3"]["not_available"]), 2)

        # Assertions for Linux
        self.assertEqual(len(linux_results["DomainA"]["available"]), 2)
        self.assertEqual(len(linux_results["DomainA"]["not_available"]), 1)
        self.assertEqual(len(linux_results["DomainB"]["available"]), 3)
        self.assertEqual(len(linux_results["DomainB"]["not_available"]), 0)

    # ========== TEST CASE 5: Invalid CSV Headers ==========

    def test_invalid_csv_headers(self):
        """
        TEST CASE 5: Invalid CSV headers

        INPUT:
        - Baseline CSV with incorrect headers

        EXPECTED RESULT:
        - CSVValidationError raised
        - Clear error message about invalid headers
        """
        invalid_csv = Path(self.temp_dir) / "invalid.csv"

        with open(invalid_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Wrong", "Headers"])
            writer.writerow(["Domain1", "HOST01"])

        with self.assertRaises(aa.CSVValidationError) as context:
            aa.validate_baseline_csv(invalid_csv)

        self.assertIn("Invalid headers", str(context.exception))

    # ========== TEST CASE 6: Empty Availability CSV ==========

    def test_empty_availability_csv(self):
        """
        TEST CASE 6: Empty availability CSV

        INPUT:
        - Baseline: 3 Windows agents
        - Availability: Empty CSV file

        EXPECTED RESULT:
        - All agents marked as Not Available
        - Availability percentage: 0%
        """
        windows_baseline = Path(self.temp_dir) / "windows_baseline.csv"

        with open(windows_baseline, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.BASELINE_COLUMNS)
            writer.writerow(["Domain1", "WIN-HOST01"])
            writer.writerow(["Domain1", "WIN-HOST02"])
            writer.writerow(["Domain1", "WIN-HOST03"])

        aa.create_database()
        aa.load_baseline_windows(windows_baseline)

        # Create empty availability CSV (headers only)
        windows_avail = Path(self.temp_dir) / "windows_avail.csv"
        with open(windows_avail, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.AVAILABILITY_COLUMNS)

        windows_baseline_data = aa.get_baseline_agents(aa.WINDOWS_TABLE)
        windows_avail_data = aa.get_availability_records(windows_avail)
        windows_results = aa.calculate_availability(windows_baseline_data, windows_avail_data)

        # All agents should be not available
        self.assertEqual(len(windows_results["Domain1"]["available"]), 0)
        self.assertEqual(len(windows_results["Domain1"]["not_available"]), 3)

    # ========== TEST CASE 7: Database Overwrite Validation ==========

    def test_database_overwrite_validation(self):
        """
        TEST CASE 7: Database overwrite validation

        INPUT:
        - Initial load: 2 Windows agents
        - Overwrite load: 3 different Windows agents

        EXPECTED RESULT:
        - Original data cleared
        - Only new data present
        """
        windows_baseline1 = Path(self.temp_dir) / "windows_baseline1.csv"
        windows_baseline2 = Path(self.temp_dir) / "windows_baseline2.csv"

        # First load
        with open(windows_baseline1, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.BASELINE_COLUMNS)
            writer.writerow(["Domain1", "WIN-HOST01"])
            writer.writerow(["Domain1", "WIN-HOST02"])

        aa.create_database()
        aa.load_baseline_windows(windows_baseline1)

        windows_baseline_data = aa.get_baseline_agents(aa.WINDOWS_TABLE)
        self.assertEqual(len(windows_baseline_data["Domain1"]), 2)

        # Second load (overwrite)
        with open(windows_baseline2, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(aa.BASELINE_COLUMNS)
            writer.writerow(["Domain2", "WIN-HOST03"])
            writer.writerow(["Domain2", "WIN-HOST04"])
            writer.writerow(["Domain2", "WIN-HOST05"])

        aa.load_baseline_windows(windows_baseline2)

        windows_baseline_data = aa.get_baseline_agents(aa.WINDOWS_TABLE)
        # Domain1 should be gone
        self.assertNotIn("Domain1", windows_baseline_data)
        # Domain2 should have 3 agents
        self.assertEqual(len(windows_baseline_data["Domain2"]), 3)

    # ========== Additional Helper Tests ==========

    def test_date_parsing_valid(self):
        """Test valid date parsing."""
        date_str = "2024-01-15 14:30:00"
        result = aa.parse_available_date(date_str)
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 15)

    def test_date_parsing_invalid(self):
        """Test invalid date parsing raises error."""
        with self.assertRaises(aa.CSVValidationError):
            aa.parse_available_date("invalid-date")

    def test_within_last_24_hours_true(self):
        """Test that recent time is within 24 hours."""
        now = datetime.now()
        self.assertTrue(aa.is_within_last_24_hours(now))

    def test_within_last_24_hours_false(self):
        """Test that old time is not within 24 hours."""
        old = datetime.now() - timedelta(hours=25)
        self.assertFalse(aa.is_within_last_24_hours(old))


def run_tests():
    """Run all test cases with detailed output."""
    print("=" * 60)
    print("AGENT AVAILABILITY SCRIPT - TEST SUITE")
    print("=" * 60)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAgentAvailability)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 60)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
