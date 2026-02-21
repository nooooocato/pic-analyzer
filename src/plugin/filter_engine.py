from typing import List, Dict, Any

class FilterEngine:
    """Evaluates sequential filter rules with boolean logic (AND/OR)."""

    def apply(self, items: List[Dict[str, Any]], rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes a list of rules: [Filter, Connector, Filter, Connector, ...]
        
        Evaluation is sequential: ((F1 Op F2) Op F3)
        """
        if not items:
            return []
        if not rules:
            return items

        current_results = list(items)
        last_op = "AND"
        
        first_plugin_seen = False
        
        for rule in rules:
            rule_type = rule.get("type")
            
            if rule_type == "connector":
                last_op = rule.get("op", "AND")
                
            elif rule_type == "plugin":
                plugin = rule.get("plugin")
                params = rule.get("params", {})
                
                if not plugin:
                    continue
                
                if not first_plugin_seen:
                    # First plugin always acts as 'AND' on the full set
                    current_results = plugin.filter(items, params)
                    first_plugin_seen = True
                    continue
                
                if last_op == "AND":
                    # AND: Only search within current results
                    current_results = plugin.filter(current_results, params)
                else: # OR
                    # OR: Search within full set and combine
                    new_matches = plugin.filter(items, params)
                    seen_paths = {it['path'] for it in current_results}
                    for it in new_matches:
                        if it['path'] not in seen_paths:
                            current_results.append(it)
                
        return current_results
