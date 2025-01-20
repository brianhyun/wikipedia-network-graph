---
title: Wikipedia Network Graph
toc: false
---

# Wikipedia Network Graph

This project presents visualizations of the network structure of Wikipedia articles given a starting article.

The data was gathered using the English Wikipedia API. Each network is generated with a depth of 2 links and the top 30 links from each article. You can hover over each node to see the article title.

The Louvain Modularity Algorithm was used to cluster the nodes into communities. The algorithm optimizes for modularity, which is a measure of the strength of division of a network into modules or communities. You can read more about it [here](https://en.wikipedia.org/wiki/Louvain_method). The color of each node determines the community it belongs to.

```js
import * as d3 from "npm:d3";

// Create the graph function
function createGraph(graph) {
  // Specify the dimensions of the chart.
  const height = 500;

  // Specify the color scale.
  const color = d3.scaleOrdinal(d3.schemeCategory10);

  // The force simulation mutates links and nodes, so create a copy
  // so that re-evaluating this cell produces the same result.
  const links = graph.links.map((d) => ({ ...d }));
  const nodes = graph.nodes.map((d) => ({ ...d }));

  // Create a simulation with several forces.
  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3.forceLink(links).id((d) => d.id)
    )
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2))
    .on("tick", ticked);

  // Create the SVG container.

  const svg = d3
    .create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto; border: 1px solid gray;");

  const g = svg.append("g");

  svg.call(
    d3.zoom().on("zoom", function (event) {
      g.attr("transform", event.transform);
    })
  );

  // Add a line for each link, and a circle for each node.
  const link = g
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .selectAll()
    .data(links)
    .join("line");
  //   .attr("stroke-width", (d) => Math.sqrt(d.value));

  const node = g
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll()
    .data(nodes)
    .join("circle")
    .attr("r", 5);

  node.append("title").text((d) => d.id);
  node.attr("fill", (d) => color(d.group));

  // Add a drag behavior.
  node.call(
    d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended)
  );

  // Set the position attributes of links and nodes each time the simulation ticks.
  function ticked() {
    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
  }

  // Reheat the simulation when drag starts, and fix the subject position.
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  // Update the subject (dragged node) position during drag.
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  // Restore the target alpha so the simulation cools after dragging ends.
  // Unfix the subject position now that it’s no longer being dragged.
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }

  // When this cell is re-run, stop the previous simulation.
  invalidation.then(() => simulation.stop());

  return svg.node();
}
```

## [Alan Turing](https://en.wikipedia.org/wiki/{{Alan_Turing}})

```js
const alan_turing_graph = FileAttachment(
  "./data/outputs/alan_turing_d2_l30.json"
).json();
```

```js
display(alan_turing_graph);
```

```js
display(createGraph(alan_turing_graph));
```

## [Machine Learning](https://en.wikipedia.org/wiki/{{Machine_learning}})

```js
const machine_learning_graph = FileAttachment(
  "./data/outputs/machine_learning_d2_l30.json"
).json();
```

```js
display(machine_learning_graph);
```

```js
display(createGraph(machine_learning_graph));
```

<!-- ```js
const machine_learning_graph_2 = FileAttachment(
  "./data/outputs/machine_learning_d3_l30.json"
).json();
```

```js
display(createGraph(machine_learning_graph_2));
``` -->

## [Black Hole](https://en.wikipedia.org/wiki/{{Black_hole}})

```js
const black_hole_graph = FileAttachment(
  "./data/outputs/black_hole_d2_l30.json"
).json();
```

```js
display(black_hole_graph);
```

```js
display(createGraph(black_hole_graph));
```

## [The Butterfly Effect](https://en.wikipedia.org/wiki/{{The_Butterfly_Effect}})

```js
const the_butterfly_effect_graph = FileAttachment(
  "./data/outputs/the_butterfly_effect_d2_l30.json"
).json();
```

```js
display(the_butterfly_effect_graph);
```

```js
display(createGraph(the_butterfly_effect_graph));
```

## [Leonardo da Vinci](https://en.wikipedia.org/wiki/{{Leonardo_da_Vinci}})

```js
const leonardo_da_vinci_graph = FileAttachment(
  "./data/outputs/leonardo_da_vinci_d2_l30.json"
).json();
```

```js
display(leonardo_da_vinci_graph);
```

```js
display(createGraph(leonardo_da_vinci_graph));
```

## Try it out yourself!

Enter the name of an article to see the network of the article and its top 30 links. The previous network graphs used the Louvain Modularity Algorithm from the python `community` package. The current implementation uses the npm `graphology` package.

If you get an unexpected graph, try capitalizing the article name appropriately. For example, "iphone" should be "iPhone".

<html>
  <body>
    <input type="text" id="article" placeholder="Enter an article" required/>
    <button id="submit">Submit</button>
  </body>
</html>

<style>
  input#article {
    padding: 8px; 
  }

  button#submit {
    padding: 8px;
  }
</style>

```js
import DOMPurify from "dompurify";

// For fetching data
const BLACKLIST_KEYWORDS = [
  "Help:",
  "File:",
  "Template:",
  "Special:",
  "Talk:",
  "Portal:",
  "Category:",
  "User:",
  "Wikipedia:",
];

async function fetchTopLinks(article, limit = 30) {
  const url = "https://en.wikipedia.org/w/api.php";
  const sanitizedArticle = DOMPurify.sanitize(article);

  const params = new URLSearchParams({
    action: "query",
    titles: sanitizedArticle,
    prop: "links",
    pllimit: "max",
    format: "json",
    origin: "*",
  });

  let links = [];

  while (true) {
    const response = await fetch(`${url}?${params}`);
    const data = await response.json();

    // Parse response
    const pages = data.query?.pages || {};

    for (const pageData of Object.values(pages)) {
      if (pageData.links) {
        for (const link of pageData.links) {
          const title = link.title;

          // Exclude blacklisted links
          if (!BLACKLIST_KEYWORDS.some((keyword) => title.includes(keyword))) {
            links.push(title);

            if (links.length >= limit) {
              return links;
            }
          }
        }
      }
    }

    // Handle continuation if more results exist
    if (data.continue) {
      Object.entries(data.continue).forEach(([key, value]) => {
        params.set(key, value);
      });
    } else {
      break;
    }
  }

  return links.slice(0, limit);
}

async function buildGraph(startArticle, depth = 2) {
  const visited = new Set();
  const graph = {
    nodes: [],
    links: [],
  };

  function getOrCreateNode(article) {
    if (!graph.nodes.includes(article)) {
      graph.nodes.push(article);
    }
    return article;
  }

  async function addLinks(article, currentDepth) {
    if (currentDepth > depth || visited.has(article)) {
      return;
    }

    visited.add(article);

    const links = await fetchTopLinks(article);

    for (const link of links) {
      const src = getOrCreateNode(article);
      const dest = getOrCreateNode(link);

      graph.links.push({
        source: src,
        target: dest,
      });

      if (currentDepth < depth) {
        await addLinks(link, currentDepth + 1);
      }
    }
  }

  await addLinks(startArticle, 1);
  return graph;
}
```

```js
// Helper functions for fetching data
import graphology from "graphology";
import louvain from "graphology-communities-louvain";

function dictToGraphology(graphDict) {
  const G = new graphology.Graph();

  // Add nodes
  graphDict.nodes.forEach((node) => {
    G.addNode(node.id);
  });

  // Add edges
  graphDict.links.forEach((link) => {
    G.addEdge(link.source, link.target);
  });

  return G;
}

function detectCommunities(graphDict) {
  const G = dictToGraphology(graphDict);

  // Apply Louvain modularity
  const partition = louvain(G);

  // Add community info back to nodes
  graphDict.nodes.forEach((node) => {
    node.group = partition[node.id];
  });

  return graphDict;
}
```

```js
document.getElementById("submit").addEventListener("click", async function () {
  const article = document.getElementById("article").value;

  // If the article doesn't exist, then return a notification.
  if (article === "") {
    alert("Please enter a valid article.");
    return;
  }

  // Disable input and button while loading
  document.getElementById("article").disabled = true;
  document.getElementById("submit").disabled = true;

  // Call a data loader
  const graph = await buildGraph(article);
  graph["nodes"] = graph["nodes"].map((node) => ({ id: node }));
  const updatedGraph = detectCommunities(graph);
  display(
    html`<h2>
      ${article
        .split(" ")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ")}
    </h2>`
  );
  display(createGraph(updatedGraph));

  // Re-enable input and button after loading
  document.getElementById("article").disabled = false;
  document.getElementById("submit").disabled = false;
});
```
