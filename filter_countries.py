import json

# List of major countries to keep
target_countries = [
    "United States", "United Kingdom", "Canada", "Australia", "France", "Germany", "Spain", "Italy", "Japan", "China", 
    "India", "Brazil", "Mexico", "Russia", "South Africa", "Argentina", "Netherlands", "Sweden", "Switzerland", "Belgium",
    "Austria", "Norway", "Denmark", "Finland", "Ireland", "Portugal", "Greece", "Turkey", "South Korea", "Singapore",
    "Malaysia", "Thailand", "Indonesia", "Vietnam", "Philippines", "New Zealand", "Egypt", "Saudi Arabia", "United Arab Emirates",
    "Israel", "Poland", "Czech Republic", "Hungary", "Romania", "Ukraine", "Pakistan", "Bangladesh", "Nigeria", "Kenya"
]

try:
    with open('listings/static/listings/js/countries.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    filtered_data = {}
    for country in target_countries:
        if country in data:
            # Keep all cities for these countries, or limit if too many?
            # Let's limit to top 100 cities alphabetically to save space if needed, 
            # but for now let's see how big it is.
            # Actually, some countries have thousands. Let's limit to 100.
            cities = data[country]
            if len(cities) > 100:
                # Try to pick major cities if possible? 
                # Without a population list, we can't. 
                # So we'll just take the first 100 (which are usually alphabetical).
                # This is a trade-off.
                filtered_data[country] = cities[:200] 
            else:
                filtered_data[country] = cities
    
    # Output as JS object
    js_content = "const countryData = " + json.dumps(filtered_data) + ";"
    
    with open('filtered_data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Generated filtered_data.js with {len(filtered_data)} countries.")

except Exception as e:
    print(f"Error: {e}")
