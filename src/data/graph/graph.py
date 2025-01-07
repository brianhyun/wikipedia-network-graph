import json
import requests
import sys

from community_detection import detect_communities

BLACKLIST_KEYWORDS = [
    "Help:", "File:", "Template:", "Special:", "Talk:", "Portal:", 
    "Category:", "User:", "Wikipedia:"
]

def fetch_top_links(article, limit=30):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": article,
        "prop": "links",
        "pllimit": "max",
        "format": "json"
    }
    links = []
    
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Parse response
        pages = data.get("query", {}).get("pages", {})
        
        for _, page_data in pages.items():
            if "links" in page_data:
                for link in page_data["links"]:
                    title = link['title']
                    
                    # Exclude blacklisted links
                    if not any(keyword in title for keyword in BLACKLIST_KEYWORDS):
                        links.append(title)
                        
                        if len(links) >= limit:
                            return links
        
        # Handle continuation if more results exist
        if "continue" in data:
            params.update(data["continue"])
        else:
            break

    return links[:limit]  

def build_graph(start_article, depth):
    visited = set()
    graph = {
        "nodes": [],
        "links": []
    }

    def get_or_create_node(article):
        if article not in graph["nodes"]:
            graph["nodes"].append(article)

        return article

    def add_links(article, current_depth):
        if current_depth > depth or article in visited:
            return
        
        visited.add(article)
        
        links = fetch_top_links(article)
        
        for link in links:
            src = get_or_create_node(article)
            dest = get_or_create_node(link)

            graph["links"].append({
                "source": src,
                "target": dest
            })
            
            if current_depth < depth:
                add_links(link, current_depth + 1)

    add_links(start_article, 1)
    return graph

start_article = ""
depth = 2
graph = build_graph(start_article, depth)
graph["nodes"] = [{"id": node} for node in graph["nodes"]]

# Detect communities and update the graph
updated_graph = detect_communities(graph)

# Write the graph to standard output
json.dump(updated_graph, sys.stdout)
