import numpy as np
import plotly.graph_objects as go

# Define the function
def f(x, y):
    return np.sin(x) * np.cos(y) + y*x/8/3.4

# Create a meshgrid for x and y
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = f(x, y)

# Create the surface plot
fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Viridis')])

# Annotate coordinates on the surface (sample points)
for i in range(0, x.shape[0], 10):  # Skip some points for clarity
    for j in range(0, y.shape[1], 10):
        fig.add_trace(go.Scatter3d(
            x=[x[i, j]], y=[y[i, j]], z=[z[i, j]],
            mode='text',
            text=[f'({x[i, j]:.2f}, {y[i, j]:.2f}, {z[i, j]:.2f})'],
            textposition='top center',
            marker=dict(size=5, color='red')
        ))

# Labels and title
fig.update_layout(
    title='3D Surface Plot of f(x, y) = sin(x) * cos(y)',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
)

# Show the interactive plot
fig.show()
