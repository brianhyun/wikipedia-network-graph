---
title: Wikiepedia Network Graph
toc: false
---

# Wikipedia Network Graph

This project presents visualizations of the network structure of Wikipedia articles given a starting article. Each network is generated from a depth of 2 links and the top 30 links, represented by nodes, from each article. You can hover over each node to see the article title.

```js
import * as d3 from "npm:d3";

// Create the graph function
function createGraph(graph) {
  // Specify the dimensions of the chart.
  const width = 900;
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
  //   .attr("fill", (d) => color(d.group));

  node.append("title").text((d) => d.id);

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
display(createGraph(alan_turing_graph));
```

## [Machine learning](https://en.wikipedia.org/wiki/{{Machine_learning}})

```js
const machine_learning_graph = FileAttachment(
  "./data/outputs/machine_learning_d2_l30.json"
).json();
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

## [Black Holes](https://en.wikipedia.org/wiki/{{Black_Holes}})

```js
const black_holes_graph = FileAttachment(
  "./data/outputs/black_holes_d2_l30.json"
).json();
```

```js
display(createGraph(black_holes_graph));
```

## [Butterfly Effect](https://en.wikipedia.org/wiki/{{Butterfly_Effect}})

```js
const butterfly_effect_graph = FileAttachment(
  "./data/outputs/butterfly_effect_d2_l30.json"
).json();
```

```js
display(createGraph(butterfly_effect_graph));
```

## [Leonardo da Vinci](https://en.wikipedia.org/wiki/{{Leonardo_da_Vinci}})

```js
const leonardo_da_vinci_graph = FileAttachment(
  "./data/outputs/leonardo_da_vinci_d2_l30.json"
).json();
```

```js
display(createGraph(leonardo_da_vinci_graph));
```
