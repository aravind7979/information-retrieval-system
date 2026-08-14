def parse_boolean_query(query: str):
    """
    Identifies Boolean operators (AND, OR, NOT) in the query
    and splits the query into parts.
    """
    operator = "OR" # Default behavior is OR (match any)
    parts = []
    
    if " AND " in query:
        operator = "AND"
        parts = query.split(" AND ")
    elif " OR " in query:
        operator = "OR"
        parts = query.split(" OR ")
    elif " NOT " in query:
        operator = "NOT"
        parts = query.split(" NOT ")
    else:
        parts = [query]
        
    return operator, parts
