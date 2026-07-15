"""
SVTRAF Validation Module

Implements statistical validation metrics:
  - NDCG (Normalized Discounted Cumulative Gain)
  - Spearman Rank Correlation
  - Mean Absolute Error
  - Wilcoxon Signed-Rank Test
  - Effect Sizes (Cohen's d, Cliff's Δ)
"""

from typing import Tuple, Dict
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import ndcg_score


class ValidationMetrics:
    """
    Statistical validation metrics for SVTRAF framework.
    """
    
    @staticmethod
    def ndcg_at_k(y_true: np.ndarray, y_pred: np.ndarray, k: int = 10) -> float:
        """
        Calculate NDCG@k (Normalized Discounted Cumulative Gain at k).
        
        Measures ranking quality of top k predictions against ground truth.
        
        Args:
            y_true: True labels (ground truth)
            y_pred: Predicted scores
            k: Number of top items to consider
        
        Returns:
            NDCG@k score [0, 1]
        """
        # Create relevance matrix (1 if in top k, 0 otherwise)
        y_true = np.array(y_true).reshape(1, -1)
        y_pred = np.array(y_pred).reshape(1, -1)
        
        return ndcg_score(y_true, y_pred, k=k)
    
    @staticmethod
    def spearman_correlation(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """
        Calculate Spearman Rank Correlation and p-value.
        
        Non-parametric correlation test.
        
        Args:
            x: First array
            y: Second array
        
        Returns:
            Tuple (correlation coefficient, p-value)
        """
        rho, p_value = stats.spearmanr(x, y)
        return rho, p_value
    
    @staticmethod
    def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Error.
        
        Args:
            y_true: True values
            y_pred: Predicted values
        
        Returns:
            MAE score
        """
        return np.mean(np.abs(y_true - y_pred))
    
    @staticmethod
    def wilcoxon_test(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """
        Wilcoxon Signed-Rank Test for paired samples.
        
        Tests if two paired samples have different distributions.
        
        Args:
            x: First sample
            y: Second sample (paired with x)
        
        Returns:
            Tuple (test statistic, p-value)
        """
        statistic, p_value = stats.wilcoxon(x, y)
        return statistic, p_value
    
    @staticmethod
    def cohens_d(x: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate Cohen's d effect size for independent samples.
        
        Args:
            x: First sample
            y: Second sample
        
        Returns:
            Cohen's d value
        """
        n1, n2 = len(x), len(y)
        var1, var2 = np.var(x, ddof=1), np.var(y, ddof=1)
        
        # Pooled standard deviation
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
        
        return (np.mean(x) - np.mean(y)) / pooled_std
    
    @staticmethod
    def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate Cliff's Delta effect size (non-parametric).
        
        More robust than Cohen's d for non-normal distributions.
        
        Args:
            x: First sample
            y: Second sample
        
        Returns:
            Cliff's Δ value [-1, 1]
        """
        n1, n2 = len(x), len(y)
        
        # Count dominance
        greater = sum(x[:, None] > y) 
        less = sum(x[:, None] < y)
        
        return (greater - less) / (n1 * n2)
    
    @staticmethod
    def evaluate_framework(y_true: np.ndarray, 
                          y_pred: np.ndarray,
                          framework_name: str = "") -> Dict[str, float]:
        """
        Comprehensive evaluation of framework performance.
        
        Args:
            y_true: True values (ground truth)
            y_pred: Predicted values (framework scores)
            framework_name: Name of framework being evaluated
        
        Returns:
            Dict with all validation metrics
        """
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Normalize scores to [0, 1] for fair comparison
        y_true_norm = (y_true - y_true.min()) / (y_true.max() - y_true.min())
        y_pred_norm = (y_pred - y_pred.min()) / (y_pred.max() - y_pred.min())
        
        rho, p_value = ValidationMetrics.spearmanr_correlation(y_true_norm, y_pred_norm)
        mae = ValidationMetrics.mean_absolute_error(y_true_norm, y_pred_norm)
        ndcg = ValidationMetrics.ndcg_at_k(y_true_norm, y_pred_norm, k=10)
        
        return {
            "framework": framework_name,
            "ndcg@10": ndcg,
            "spearman_rho": rho,
            "p_value": p_value,
            "mae": mae,
            "n_samples": len(y_true),
        }
    
    @staticmethod
    def compare_frameworks(frameworks_dict: Dict[str, Tuple[np.ndarray, np.ndarray]]) -> pd.DataFrame:
        """
        Compare multiple frameworks on same ground truth.
        
        Args:
            frameworks_dict: Dict {framework_name: (y_true, y_pred)}
        
        Returns:
            DataFrame with comparison metrics
        """
        results = []
        
        for name, (y_true, y_pred) in frameworks_dict.items():
            metrics = ValidationMetrics.evaluate_framework(y_true, y_pred, name)
            results.append(metrics)
        
        return pd.DataFrame(results)


if __name__ == "__main__":
    # Example validation
    np.random.seed(42)
    y_true = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y_svtraf = y_true + np.random.normal(0, 0.5, len(y_true))
    
    metrics = ValidationMetrics.evaluate_framework(y_true, y_svtraf, "SVTRAF")
    print("Validation Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
