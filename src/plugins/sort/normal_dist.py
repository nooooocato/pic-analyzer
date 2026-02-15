import numpy as np
from typing import List, Dict, Any
from src.plugins.sort.base import BaseSortPlugin

class NormalDistributionSortPlugin(BaseSortPlugin):

    """

    Sorts items by proximity to the mean (Peak First).

    """

    @property

    def name(self) -> str:

        return "Normal Distribution"



    @property

    def description(self) -> str:

        return "Show items closest to the mean value first."



    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:

        """

        Sorts items by absolute difference from the mean.

        

        Args:

            items (List[Dict[str, Any]]): List of image metadata dictionaries.

            metric_key (str): The key to sort by.

            

        Returns:

            List[Dict[str, Any]]: A new list sorted by proximity to the mean.

        """

        if not items:

            return []

        

        values = [float(item.get(metric_key, 0)) for item in items]

        mean = np.mean(values)

        

        # Sort by absolute difference from the mean

        return sorted(items, key=lambda x: abs(float(x.get(metric_key, 0)) - mean))      



    def get_stats(self, items: List[Dict[str, Any]], metric_key: str) -> Dict[str, Any]: 

        """

        Calculates mean and standard deviation for the provided items and metric.

        

        Args:

            items (List[Dict[str, Any]]): List of items to analyze.

            metric_key (str): The metric key to use for calculations.

            

        Returns:

            Dict[str, Any]: A dictionary containing 'mean' and 'sigma'.

        """

        if not items:

            return {"mean": 0, "sigma": 0}



        values = [float(item.get(metric_key, 0)) for item in items]

        return {

            "mean": float(np.mean(values)),

            "sigma": float(np.std(values))

        }


