import networkx as nx
import plotly.graph_objects as go
import matplotlib.cm as cm

def plot_3d_multilayer_graph_with_synced_colors(array3d, filename="multiplex_graph_synced.html"):
    """
    Visualize a multiplex graph from a 3D array.
    Each layer is placed at a different z-depth.
    Intra-layer edges are color-coded, inter-layer edges connect same nodes vertically,
    transparent planes highlight each layer,
    and matrix tables use the same colors as their layer edges.
    """
    n = len(array3d[0])        # number of nodes
    num_layers = len(array3d)  # number of layers

    # Generate color map for layers
    color_map = cm.get_cmap('tab10', num_layers)

    # Base 2D positions for nodes
    base_pos = nx.spring_layout(nx.complete_graph(n), dim=2, seed=42)

    traces = []

    # Add nodes, intra-layer edges, and transparent planes
    for layer_index in range(num_layers):
        z_offset = layer_index * 2.0
        x_nodes = [base_pos[k][0] for k in range(n)]
        y_nodes = [base_pos[k][1] for k in range(n)]
        z_nodes = [z_offset for _ in range(n)]

        # Nodes
        node_trace = go.Scatter3d(
            x=x_nodes, y=y_nodes, z=z_nodes,
            mode='markers+text',
            marker=dict(size=10, color='lightblue'),
            text=[f"{k} (L{layer_index+1})" for k in range(n)],
            textposition="top center",
            name=f"Layer {layer_index+1} Nodes"
        )
        traces.append(node_trace)

        # Intra-layer edges
        matrix = array3d[layer_index]
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != 0:
                    x0, y0 = base_pos[i]
                    x1, y1 = base_pos[j]
                    z0, z1 = z_offset, z_offset
                    edge_trace = go.Scatter3d(
                        x=[x0, x1], y=[y0, y1], z=[z0, z1],
                        mode='lines',
                        line=dict(color=color_map(layer_index), width=4),
                        name=f"Layer {layer_index+1} Edge"
                    )
                    traces.append(edge_trace)

        # Transparent plane
        plane_trace = go.Mesh3d(
            x=[min(x_nodes), max(x_nodes), max(x_nodes), min(x_nodes)],
            y=[min(y_nodes), min(y_nodes), max(y_nodes), max(y_nodes)],
            z=[z_offset, z_offset, z_offset, z_offset],
            opacity=0.15,
            color='lightgray',
            name=f"Layer {layer_index+1} Plane",
            showscale=False
        )
        traces.append(plane_trace)

    # Inter-layer edges
    for node in range(n):
        for layer_index in range(num_layers - 1):
            x, y = base_pos[node]
            z0 = layer_index * 2.0
            z1 = (layer_index + 1) * 2.0
            inter_edge = go.Scatter3d(
                x=[x, x], y=[y, y], z=[z0, z1],
                mode='lines',
                line=dict(color='gray', width=2, dash='dot'),
                name=f"Inter-layer Node {node}"
            )
            traces.append(inter_edge)

    fig = go.Figure(data=traces)
    fig.update_layout(
        title="Multiplex Graph with Transparent Layer Planes",
        showlegend=False,
        scene=dict(
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(showbackground=False)
        )
    )

    # Export visualization
    html_graph = fig.to_html(full_html=True, include_plotlyjs='cdn')

    # Build matrix tables with synchronized colors
    html_table = "<h2>Matrix Values (Layer Colors)</h2>"
    for layer_index, matrix in enumerate(array3d):
        # Convert matplotlib color to CSS rgb string
        rgba = color_map(layer_index)
        layer_color = f"rgb({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)})"

        html_table += f"<h3 style='color:{layer_color};'>Layer {layer_index+1}</h3>"
        html_table += "<table border='1' style='border-collapse:collapse;'>"
        for row in matrix:
            html_table += "<tr>"
            for val in row:
                if val == 0:
                    cell_color = "white"
                else:
                    cell_color = layer_color
                html_table += f"<td style='background-color:{cell_color}; padding:5px; text-align:center;'>{val}</td>"
            html_table += "</tr>"
        html_table += "</table><br>"

    # Combine graph + matrix table
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Multiplex Graph with Matrix</title>
      <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
      <h1>Multiplex Graph Visualization</h1>
      {html_graph}
      {html_table}
    </body>
    </html>
    """

    with open(filename, "w") as f:
        f.write(html_content)

    print(f"Visualization with synchronized matrix colors exported as {filename}")


# Example: 3 layers of 3x3 matrices
A = [
    [
        [0, 1, 0],
        [0, 0, 2],
        [3, 0, 0]
    ],
    [
        [0, 4, 0],
        [5, 0, 0],
        [0, 0, 6]
    ],
    [
        [0, 0, 7],
        [0, 0, 8],
        [9, 0, 0]
    ]
]

plot_3d_multilayer_graph_with_synced_colors(A, filename="multiplex_graph_synced.html")