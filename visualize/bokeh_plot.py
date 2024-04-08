from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Arrow, VeeHead, LabelSet, ColumnDataSource

def create_base_flowchart():
    p = figure(width=400, height=400)
    
    # Define the base structure of the flowchart
    # For simplicity, let's say our flowchart has three nodes
    nodes = {'x_values': [1, 2, 3], 
             'y_values': [3, 2, 3]}
    
    source = ColumnDataSource(nodes)

    # Adding nodes as circles (you can style these as needed)
    p.circle(x='x_values', y='y_values', size=20, source=source)

    # Adding arrows (you can adjust positions as needed)
    p.add_layout(Arrow(end=VeeHead(size=10), x_start=1, y_start=3, x_end=2, y_end=2))
    p.add_layout(Arrow(end=VeeHead(size=10), x_start=2, y_start=2, x_end=3, y_end=3))

    return p, source
def update_flowchart_with_metadata(plot, source, metadata):
    # Update the source data based on the metadata
    # This example assumes metadata contains new labels for the nodes
    source.data['labels'] = metadata['labels']

    # Add or update labels on the plot
    if 'labels' in source.data:
        labels = LabelSet(x='x_values', y='y_values', text='labels', source=source)
        plot.add_layout(labels)

