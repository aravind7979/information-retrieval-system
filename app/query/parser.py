def parse_boolean_query(query: str):
    """
    Identifies Boolean operators (AND, OR, NOT) in the query
    and splits the query into parts.
    Also detects exact phrase matching if wrapped in quotes.
    """
    operator = "OR" # Default behavior is OR (match any)
    is_phrase = False
    
    # Phase 5: Check for phrase search (exact match)
    if query.startswith('"') and query.endswith('"') and len(query) >= 2:
        is_phrase = True
        query = query[1:-1] # Strip the quotes for boolean processing
        
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
        
    return operator, parts, is_phrase, query
