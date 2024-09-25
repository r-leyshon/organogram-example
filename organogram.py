import pandas as pd
import os
import networkx as nx
from pyvis.network import Network
import random

# Define the path to the pickle file
pickle_path = os.path.join('data', 'example_employee_data.pkl')

# Check if the file exists
if os.path.exists(pickle_path):
    # Read the pickle file and create a DataFrame
    df = pd.read_pickle(pickle_path)


# Create a directed graph
G = nx.DiGraph()

# Add nodes to the graph
# for _, row in df.iterrows():
#     G.add_node(row['ID'], name=row['name'], team=row['team'], division=row['division'])

for _, row in df.iterrows():
    G.add_node(row['ID'], name=row['name'], team=row['team'], division=row['division'])

# Add edges to the graph (employee to manager)
for _, row in df.iterrows():
    if row['managerID']:  # Check if the employee has a manager
        G.add_edge(row['ID'], row['managerID'])


#--pyvis interactive---

# Create a color map for teams
unique_teams = df['team'].unique()
color_map = {team: f"#{random.randint(0, 0xFFFFFF):06x}" for team in unique_teams}

# Interactive visualization with Pyvis
net = Network(height="750px", width="100%", directed=True, bgcolor="#222222", font_color="white")

# Add nodes to the Pyvis network with color based on team
for node, data in G.nodes(data=True):
    net.add_node(node, 
                 label=data['name'], 
                 title=f"Team: {data['team']}\nDivision: {data['division']}", 
                 color=color_map[data['team']],  # Set node color based on team
                 group=data['team'])

# Add edges to the Pyvis network
for edge in G.edges():
    net.add_edge(edge[0], edge[1])

# Set options for the network visualization
net.set_options("""
var options = {
  "nodes": {
    "font": {
      "size": 12
    }
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "physics": {
    "hierarchicalRepulsion": {
      "centralGravity": 0
    },
    "minVelocity": 0.75,
    "solver": "hierarchicalRepulsion"
  }
}
""")



# Save the interactive visualization
net.show("index.html", notebook=False)
