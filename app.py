import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from astar_module import run_astar, time_weighted_graph, add_traffic

# Layout coordinates
coordinates = {
    0: (0, 0),
    1: (8, 6),
    2: (22, 7),
    3: (15, 12),
    4: (15.7, 8.5),
    5: (6, 8),
    6: (5, 7)
}

# Initialize G once and store in session_state
if "G" not in st.session_state:
    G = time_weighted_graph()
    add_traffic(G)
    st.session_state.G = G
else:
    G = st.session_state.G

st.set_page_config(page_title="MC_FPA-AI A*", layout="wide")
st.title("🚀 MC_FPA-AI - Fastest Path Visualizer")
st.caption("Visualize A*, BFS, Genetic, and Simulated Annealing pathfinding algorithms on a sample graph.")

# Sidebar input
with st.sidebar:
    st.header("User Input")
    start_node = st.selectbox("Start Node", list(coordinates.keys()))
    goal_node = st.selectbox("Goal Node", list(coordinates.keys()))
    find_path = st.button("Find Path")
    if st.button("Reset Graph"):
        st.session_state.clear()
        st.experimental_rerun()

# Base graph
fig, ax = plt.subplots()
pos = coordinates
edge_labels = nx.get_edge_attributes(G, 'weight')

nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=800, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', ax=ax)
nx.draw_networkx_edges(G, pos, edge_color='black', width=2, ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels={e: f"{w:.1f}" for e, w in edge_labels.items()}, font_size=10, ax=ax)

# Path finding
if find_path:
    total_cost, path = run_astar(G, start_node, goal_node)
    if path:
        st.success(f"Path: {' → '.join(map(str, path))}")
        st.info(f"Total Time: {total_cost:.2f} seconds")

        # Highlight path
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', width=4, ax=ax)
    else:
        st.warning("No path found!")

# Show plot
st.pyplot(fig)
