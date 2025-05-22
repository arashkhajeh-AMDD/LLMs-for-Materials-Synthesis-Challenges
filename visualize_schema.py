{
  "cell_type": "code",
  "metadata": {
    "language": "python"
  },
  "source": [
    "from py2neo import Graph",
    "import networkx as nx",
    "import matplotlib.pyplot as plt",
    "",
    "# Connect to Neo4j",
    "graph = Graph(\"bolt://localhost:7687\", auth=(\"neo4j\", \"your_password\"))",
    "",
    "# Query to fetch nodes and relationships",
    "query = \"\"\"",
    "MATCH (n)-[r]->(m)",
    "RETURN n.name AS source, type(r) AS relationship, m.name AS target",
    "\"\"\"",
    "",
    "results = graph.run(query).data()",
    "",
    "# Create a NetworkX graph",
    "G = nx.DiGraph()",
    "",
    "# Add nodes and edges to the graph",
    "for record in results:",
    "    G.add_node(record['source'])",
    "    G.add_node(record['target'])",
    "    G.add_edge(record['source'], record['target'], label=record['relationship'])",
    "",
    "# Draw the graph",
    "plt.figure(figsize=(12, 8))",
    "pos = nx.spring_layout(G)",
    "nx.draw(G, pos, with_labels=True, node_size=3000, node_color=\"lightblue\", font_size=10, font_weight=\"bold\")",
    "nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'))",
    "plt.title(\"Neo4j Schema Visualization\")",
    "plt.show()"
  ]
}
