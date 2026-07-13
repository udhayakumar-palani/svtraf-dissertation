"""
SVTRAF Scoring Module

Implements the SVTRAF scoring formula:
  SVTRAF = 10 × [0.40·ISC + 0.20·ESC + 0.25·AMP + 0.15·INT]

Where:
  - ISC = Intrinsic Smart Contract Component (financial damage + exploitability)
  - ESC = External Systems Component (exploitation likelihood)
  - AMP = Automation & Persistence (immutability + autonomous execution)
  - INT = Integrity/Trade Confidentiality (scope)
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


class SVTRAFScorer:
    """
    SVTRAF Framework Scorer.
    
    Attributes:
        weights: Component weights in SVTRAF formula
        components: List of component names
    """
    
    # SVTRAF component weights (grounded in literature)
    WEIGHTS = {
        "ISC": 0.40,   # Intrinsic Smart Contract Component
        "ESC": 0.20,   # External Systems Component
        "AMP": 0.25,   # Automation & Persistence
        "INT": 0.15,   # Integrity/Trade Confidentiality
    }
    
    SCALE_FACTOR = 10  # Final score range [0, 10]
    
    def __init__(self):
        """Initialize SVTRAF scorer with component weights."""
        self.weights = self.WEIGHTS.copy()
        self.components = list(self.weights.keys())
    
    def calculate_isc(self, financial_harm: float, exploitability: float) -> float:
        """
        Calculate ISC (Intrinsic Smart Contract Component).
        
        ISC = 0.6 × financial_harm + 0.4 × exploitability
        
        Args:
            financial_harm: Financial damage potential [0, 10]
            exploitability: Ease of exploitation [0, 10]
        
        Returns:
            ISC score [0, 10]
        """
        return 0.6 * financial_harm + 0.4 * exploitability
    
    def calculate_esc(self, exploitability: float) -> float:
        """
        Calculate ESC (External Systems Component).
        
        ESC = exploitability
        
        Args:
            exploitability: Exploitation likelihood [0, 10]
        
        Returns:
            ESC score [0, 10]
        """
        return exploitability
    
    def calculate_amp(self, immutability: float, automation: float) -> float:
        """
        Calculate AMP (Automation & Persistence).
        
        AMP = 0.5 × immutability + 0.5 × automation
        
        Args:
            immutability: Contract immutability [0, 10]
            automation: Autonomous execution [0, 10]
        
        Returns:
            AMP score [0, 10]
        """
        return 0.5 * immutability + 0.5 * automation
    
    def calculate_int(self, scope: float) -> float:
        """
        Calculate INT (Integrity/Trade Confidentiality).
        
        INT = scope
        
        Args:
            scope: Impact scope [0, 10]
        
        Returns:
            INT score [0, 10]
        """
        return scope
    
    def score(self, isc: float, esc: float, amp: float, int_score: float) -> float:
        """
        Calculate composite SVTRAF score.
        
        SVTRAF = 10 × [0.40·ISC + 0.20·ESC + 0.25·AMP + 0.15·INT]
        
        Args:
            isc: ISC component [0, 10]
            esc: ESC component [0, 10]
            amp: AMP component [0, 10]
            int_score: INT component [0, 10]
        
        Returns:
            SVTRAF score [0, 10]
        """
        weighted_sum = (
            self.weights["ISC"] * isc +
            self.weights["ESC"] * esc +
            self.weights["AMP"] * amp +
            self.weights["INT"] * int_score
        )
        return self.SCALE_FACTOR * weighted_sum
    
    def score_contract(self, 
                      financial_harm: float,
                      exploitability: float,
                      immutability: float,
                      automation: float,
                      scope: float) -> Dict[str, float]:
        """
        Calculate full SVTRAF score for a contract.
        
        Args:
            financial_harm: Financial damage capability [0, 10]
            exploitability: Exploitation likelihood [0, 10]
            immutability: Contract immutability [0, 10]
            automation: Autonomous execution [0, 10]
            scope: Impact scope [0, 10]
        
        Returns:
            Dict with component scores and final SVTRAF score
        """
        isc = self.calculate_isc(financial_harm, exploitability)
        esc = self.calculate_esc(exploitability)
        amp = self.calculate_amp(immutability, automation)
        int_score = self.calculate_int(scope)
        
        svtraf = self.score(isc, esc, amp, int_score)
        
        return {
            "ISC": isc,
            "ESC": esc,
            "AMP": amp,
            "INT": int_score,
            "SVTRAF_score": svtraf,
        }
    
    def score_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Score multiple contracts in a DataFrame.
        
        Expected columns: financial_harm, exploitability, immutability, automation, scope
        
        Args:
            df: DataFrame with component scores
        
        Returns:
            DataFrame with added component and SVTRAF scores
        """
        result = df.copy()
        
        result["ISC"] = self.calculate_isc(
            result["financial_harm"], result["exploitability"]
        )
        result["ESC"] = self.calculate_esc(result["exploitability"])
        result["AMP"] = self.calculate_amp(
            result["immutability"], result["automation"]
        )
        result["INT"] = self.calculate_int(result["scope"])
        
        result["SVTRAF_score"] = self.score(
            result["ISC"], result["ESC"], result["AMP"], result["INT"]
        )
        
        return result
    
    def ablation_study(self, isc: float, esc: float, amp: float, int_score: float) -> Dict[str, float]:
        """
        Perform ablation study: calculate score with each component removed.
        
        Args:
            isc, esc, amp, int_score: Component scores
        
        Returns:
            Dict with full score and ablation results
        """
        full_score = self.score(isc, esc, amp, int_score)
        
        return {
            "full": full_score,
            "without_ISC": self.SCALE_FACTOR * (
                self.weights["ESC"] * esc +
                self.weights["AMP"] * amp +
                self.weights["INT"] * int_score
            ),
            "without_ESC": self.SCALE_FACTOR * (
                self.weights["ISC"] * isc +
                self.weights["AMP"] * amp +
                self.weights["INT"] * int_score
            ),
            "without_AMP": self.SCALE_FACTOR * (
                self.weights["ISC"] * isc +
                self.weights["ESC"] * esc +
                self.weights["INT"] * int_score
            ),
            "without_INT": self.SCALE_FACTOR * (
                self.weights["ISC"] * isc +
                self.weights["ESC"] * esc +
                self.weights["AMP"] * amp
            ),
        }


if __name__ == "__main__":
    # Example usage
    scorer = SVTRAFScorer()
    
    result = scorer.score_contract(
        financial_harm=8.5,
        exploitability=7.2,
        immutability=10.0,
        automation=9.0,
        scope=7.5
    )
    
    print("Example SVTRAF Scoring:")
    for component, value in result.items():
        print(f"  {component}: {value:.2f}")
