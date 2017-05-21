import re

def kill_parentheses(str_1):
    
    try:
        ingredient = str_1.replace(re.search("\(.*\)|（.*）|\[.*\]", str_1).group(), '').strip()
    except:
        ingredient = str_1
    
    return(ingredient)