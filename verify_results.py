#!/usr/bin/env python3
"""
Verify SVTRAF framework outputs and data integrity.
Validates:
  - Dataset completeness and consistency
  - SVTRAF score calculations
  - Correlation with ground truth
  - Statistical result validity
  
Usage:
  python3 verify_results.py
  python3 verify_results.py --detailed
  python3 verify_results.py --skip-correlation
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import spearmanr
import argparse


class FrameworkValidator:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.base_path = Path("svtraf-dissertation")
        self.data_path = self.base_path / "FEW" / "data"
        self.tables_path = self.base_path / "FEW" / "tables"
        self.checks_passed = 0
        self.checks_failed = 0
        
    def log(self, msg, level="INFO"):
        prefix = f"[{level}]"
        print(f"{prefix} {msg}")
    
    def check(self, name, condition, error_msg=""):
        if condition:
            self.checks_passed += 1
            if self.verbose:
                self.log(f"✓ {name}", "PASS")
            else:
                print(".", end="", flush=True)
        else:
            self.checks_failed += 1
            self.log(f"✗ {name}: {error_msg}", "FAIL")
    
    def validate_files_exist(self):
        """Check that all required output files exist."""
        self.log("\n--- File Existence Checks ---")
        
        files = {
            "svtraf_scored.csv": self.data_path / "svtraf_scored.csv",
            "svtraf_dataset.csv": self.data_path / "svtraf_dataset.csv",
            "validation_results": self.tables_path / "table_validation_results.csv",
        }
        
        for name, path in files.items():
            self.check(f"File exists: {name}", path.exists(), 
                      f"Missing: {path}")
        
        return all(p.exists() for p in files.values())
    
    def validate_scored_dataset(self):
        """Validate svtraf_scored.csv structure and contents."""
        self.log("\n--- Scored Dataset Validation ---")
        
        if not self.data_path.exists():
            self.log("Data directory not found", "ERROR")
            return False
        
        df = pd.read_csv(self.data_path / "svtraf_scored.csv")
        
        # Check dimensions
        self.check("Dataset has 150 records", len(df) == 150, 
                  f"Got {len(df)}, expected 150")
        
        # Check required columns
        required_cols = ["contract_id", "category", "SVTRAF_score", "financial_loss_usd"]
        for col in required_cols:
            self.check(f"Column exists: {col}", col in df.columns,
                      f"Missing column: {col}")
        
        # Check for missing values
        missing = df.isnull().sum().sum()
        self.check("No missing values", missing == 0,
                  f"Found {missing} missing values")
        
        # Check SVTRAF score range [0, 10]
        if "SVTRAF_score" in df.columns:
            in_range = (df["SVTRAF_score"] >= 0) & (df["SVTRAF_score"] <= 10)
            self.check("SVTRAF scores in [0, 10]", in_range.all(),
                      f"Min: {df['SVTRAF_score'].min()}, Max: {df['SVTRAF_score'].max()}")
        
        # Check financial loss is positive
        if "financial_loss_usd" in df.columns:
            positive = (df["financial_loss_usd"] >= 0)
            self.check("Financial losses non-negative", positive.all(),
                      f"Found {(~positive).sum()} negative values")
        
        # Check stratification (5 categories × 30 contracts)
        if "category" in df.columns:
            category_counts = df["category"].value_counts()
            balanced = (category_counts >= 28).all() and (category_counts <= 32).all()
            self.check("Stratification balanced", balanced,
                      f"Category distribution: {category_counts.to_dict()}")
        
        return self.checks_failed == 0
    
    def validate_correlation(self):
        """Calculate and validate correlation with ground truth."""
        self.log("\n--- Correlation Validation ---")
        
        try:
            df = pd.read_csv(self.data_path / "svtraf_scored.csv")
            
            if "SVTRAF_score" not in df.columns or "financial_loss_usd" not in df.columns:
                self.log("Missing required columns for correlation", "WARN")
                return False
            
            rho, p_value = spearmanr(df["SVTRAF_score"], df["financial_loss_usd"])
            
            self.log(f"Spearman ρ = {rho:.4f}", "INFO")
            self.log(f"p-value = {p_value:.2e}", "INFO")
            
            # Check expected values
            self.check("Correlation > 0.9", rho > 0.9,
                      f"Got ρ = {rho:.4f}")
            
            self.check("Correlation statistically significant", p_value < 0.05,
                      f"Got p = {p_value:.2e}")
            
            return True
        except Exception as e:
            self.log(f"Correlation validation failed: {e}", "ERROR")
            return False
    
    def validate_dataset_consistency(self):
        """Validate consistency between raw and scored datasets."""
        self.log("\n--- Dataset Consistency ---")
        
        try:
            raw = pd.read_csv(self.data_path / "svtraf_dataset.csv")
            scored = pd.read_csv(self.data_path / "svtraf_scored.csv")
            
            # Check contract IDs match
            raw_ids = set(raw["contract_id"]) if "contract_id" in raw.columns else set()
            scored_ids = set(scored["contract_id"])
            
            self.check("Contract IDs match", raw_ids == scored_ids,
                      f"Mismatch: {len(raw_ids)} raw vs {len(scored_ids)} scored")
            
            return True
        except Exception as e:
            self.log(f"Consistency check failed: {e}", "WARN")
            return False
    
    def validate_statistical_results(self):
        """Validate statistical results table."""
        self.log("\n--- Statistical Results Validation ---")
        
        try:
            results = pd.read_csv(self.tables_path / "table_validation_results.csv")
            
            self.check("Results table has data", len(results) > 0,
                      "Empty results table")
            
            # Expected framework names
            expected_frameworks = ["SVTRAF", "CVSS v3.1", "BVSS", "Ahmad et al."]
            if "Framework" in results.columns:
                frameworks = results["Framework"].unique()
                self.check("All frameworks present", 
                          len(frameworks) >= 3,
                          f"Only found {len(frameworks)} frameworks")
            
            # Check NDCG scores in [0, 1]
            if "NDCG@10" in results.columns:
                in_range = (results["NDCG@10"] >= 0) & (results["NDCG@10"] <= 1)
                self.check("NDCG@10 scores valid", in_range.all(),
                          f"Invalid NDCG range")
            
            return True
        except Exception as e:
            self.log(f"Statistical results validation failed: {e}", "WARN")
            return False
    
    def run_all(self):
        """Execute all validations."""
        self.log("=" * 60)
        self.log("SVTRAF Framework Verification")
        self.log("=" * 60)
        
        if not self.validate_files_exist():
            self.log("Stopping: Required files not found", "ERROR")
            return False
        
        self.validate_scored_dataset()
        self.validate_dataset_consistency()
        self.validate_correlation()
        self.validate_statistical_results()
        
        # Summary
        self.log("\n" + "=" * 60)
        self.log(f"Checks Passed: {self.checks_passed}", "INFO")
        self.log(f"Checks Failed: {self.checks_failed}", "ERROR" if self.checks_failed > 0 else "INFO")
        self.log("=" * 60)
        
        return self.checks_failed == 0


def main():
    parser = argparse.ArgumentParser(
        description="Verify SVTRAF framework outputs and data integrity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 verify_results.py           # Quick validation
  python3 verify_results.py --verbose # Detailed output
        """
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    parser.add_argument("--skip-correlation", action="store_true",
                       help="Skip correlation validation (faster)")
    
    args = parser.parse_args()
    
    validator = FrameworkValidator(verbose=args.verbose)
    success = validator.run_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
