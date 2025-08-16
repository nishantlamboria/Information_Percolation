
# Please ensure all the libraries are installed.

import numpy as np
import random as rd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.io as pio
import os

N = 50
T = 21
beta = 0.75
theta = 1 - np.tanh(2*beta)

update_history = []
for v in range(N):
    update_seqn = []
    S = 0
    update_times = []
    while S < T:
        update_times.append(S)
        exp_t = np.random.exponential(scale=1)
        S += exp_t
            
    for time in reversed(update_times):
        if time == 0:
            update_seqn.append((0,0))
            break
        U = np.random.uniform(0,1)
        if U < theta:
            update_seqn.append((0,time))
            break
        else:
            neighbour = rd.choice([1,-1])
            update_seqn.append((neighbour, time))

    update_history.append(update_seqn)

complete_histories = []
cluster_ids = [-1 for iii in range(N)]

for v in range(N):
    path_history = [(v,T)]
    merged = False
    merger = None
    posn = v
    for event in update_history[v]:
        incoming = []
        s = path_history[-1][1]
        t = event[1]
        for path in complete_histories:
            for state in path:
                if state[0] == posn and s >= state[1] > t:
                    incoming.append((path, state))
                    break

        if incoming != []:
            hitting_times = [x[1][1] for x in incoming]
            argmin = hitting_times.index(min(hitting_times))
            path0, state0 = incoming[argmin]
            path_history.extend(path0[(path0.index(state0)+1):])
            merged = True
            merger = complete_histories.index(path0)
            break

        posn = (posn+event[0])%N
        if event[0] == 0:
            path_history.append((posn,t))
            break
        else:
            path_history.append((posn,t))
            for path in complete_histories:
                for j in range(len(path)-1):
                    if path[j][1] >= event[1] > path[j+1][1]:
                        if path[j][0] == posn:
                            path_history.extend(path[(j+1):])
                            merged = True
                            merger = complete_histories.index(path)
                        break
                if merged == True:
                    break
        if merged == True:
            break
    
    complete_histories.append(path_history)
    if merged == True:
        cluster_ids[v] = cluster_ids[merger]
    else:
        cluster_ids[v] = max(cluster_ids) + 1

clusters = []
for jjj in range(max(cluster_ids)+1):
    cluster = []
    for v in range(N):
        if cluster_ids[v] == jjj:
            cluster.append(v)
    clusters.append(cluster)


def color(c):
    for v in c:
        if complete_histories[v][-1][1] == 0:
            return 'red'
    if len(c) == 1:
        return 'blue'
    else:
        return 'green'
    
colors = []
for id in range(max(cluster_ids)+1):
    colors.append(color(clusters[id]))


def plot_interactive_walks(walks, num_vertices, walk_to_cluster=None, cluster_to_color=None):
    pio.renderers.default = 'browser'
    fig = go.Figure()
    theta_scale = 2 * np.pi / num_vertices

    cluster_keys = set(walk_to_cluster) if walk_to_cluster else range(len(walks))

    # Add cylinder surface for aesthetics
    theta_cyl = np.linspace(0, 2*np.pi, 1000)
    z_vals = [time for walk in walks for (_, time) in walk]
    zmin, zmax = min(z_vals), max(z_vals)
    z_cyl = np.linspace(zmin, zmax, 100)
    theta_grid, z_grid = np.meshgrid(theta_cyl, z_cyl)
    x_cyl = np.cos(theta_grid)
    y_cyl = np.sin(theta_grid)

    fig.add_trace(go.Surface(
        x=x_cyl, y=y_cyl, z=z_grid,
        showscale=False,
        opacity=0.16,
        colorscale='geyser_r',
        hoverinfo='skip'
    ))

    # Plot walks
    for i, walk in enumerate(walks):
        cluster_key = walk_to_cluster[i] if walk_to_cluster else i
        color = cluster_to_color[cluster_key] if cluster_to_color else f'rgb({i*5%255},{i*13%255},{i*17%255})'

        for (site1, time1), (site2, time2) in zip(walk[:-1], walk[1:]):
            theta1, theta2 = site1 * theta_scale, site2 * theta_scale
            x1, y1 = np.cos(theta1), np.sin(theta1)
            x2, y2 = np.cos(theta2), np.sin(theta2)

            # Vertical segment
            fig.add_trace(go.Scatter3d(
                x=[x1, x1], y=[y1, y1], z=[time1, time2],
                mode='lines',
                line=dict(color=color, width=4),
                hoverinfo='skip',
                showlegend=False
            ))

            # Horizontal step
            fig.add_trace(go.Scatter3d(
                x=[x1, x2], y=[y1, y2], z=[time2, time2],
                mode='lines',
                line=dict(color=color, width=4),
                hoverinfo='skip',
                showlegend=False
            ))


        # --- Add starting point: always a small sphere ---
        start_site, start_time = walk[0]
        theta_start = start_site * theta_scale
        x0, y0 = np.cos(theta_start), np.sin(theta_start)
        fig.add_trace(go.Scatter3d(
            x=[x0], y=[y0], z=[start_time],
            mode='markers',
            marker=dict(size=3, color=color, symbol='circle'),
            showlegend=False
        ))

        # --- Add endpoint marker if cluster color is green or blue ---
        if color in ['green', 'blue']:
            end_site, end_time = walk[-1]
            theta_end = end_site * theta_scale
            x1, y1 = np.cos(theta_end), np.sin(theta_end)
            fig.add_trace(go.Scatter3d(
                x=[x1], y=[y1], z=[end_time],
                mode='markers',
                marker=dict(size=2, color=color, symbol='x'),
                showlegend=False
            ))

        if color in ['red']:
            end_site, end_time = walk[-1]
            theta_end = end_site * theta_scale
            x1, y1 = np.cos(theta_end), np.sin(theta_end)
            fig.add_trace(go.Scatter3d(
                x=[x1], y=[y1], z=[end_time],
                mode='markers',
                marker=dict(size=2.5, color=color, symbol='circle'),
                showlegend=False
            ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False,
                title=dict(text='Time', font=dict(size=16)),
                tickfont=dict(size=12)
            ),
            camera=dict(eye=dict(x=2.175, y=2.175, z=1.25)),
            aspectmode='manual',
            aspectratio=dict(x=2, y=2, z=1.25)
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=0, r=0, b=0, t=0),
    )

    # # Create output directory for frames
    # output_dir = "rotation_frames"
    # os.makedirs(output_dir, exist_ok=True)

    # # Total frames and rotation angle per step
    # num_frames = 36  # You can use 36 for 10° increments (360/36 = 10°)
    # radius = 2.8  # Distance of the camera from the center
    # z_eye = 1.2   # Vertical eye level of the camera

    # for i in range(num_frames):
    #     angle = 2 * np.pi * i / num_frames
    #     camera = dict(
    #         eye=dict(
    #             x=radius * np.cos(angle),
    #             y=radius * np.sin(angle),
    #             z=z_eye
    #         )
    #     )

    #     fig.update_layout(scene_camera=camera)

    #     frame_path = os.path.join(output_dir, f"frame_{i:03d}.png")
    #     fig.write_image(frame_path, width=1200, height=900, scale=2)

    # print("✅ All rotation frames saved!")

    fig.show()


plot_interactive_walks(
    complete_histories,
    num_vertices=N,
    walk_to_cluster=cluster_ids,
    cluster_to_color=colors
)