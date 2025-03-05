import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import data_loader

def load_route_data():
    """Load the airline, routes, and airports data."""
    return data_loader.load_data("data/airlines.csv", "data/routes.csv", "data/airports-extended.csv")

def create_graph(routes):
    """Create a directed graph of airports and flight routes."""
    G = nx.DiGraph()
    for index, row in routes.iterrows():
        G.add_node(row['airport.name_x'], pos=(row['long_x'], row['lat_x']))
        G.add_node(row['airport.name_y'], pos=(row['long_y'], row['lat_y']))
    for index, row in routes.iterrows():
        G.add_edge(row['airport.name_x'], row['airport.name_y'])
    return G

def plot_graph(G):
    """Plot the flight route network overlaid on a world map."""
    plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, color='lightgrey')
    
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color='skyblue', alpha=0.8, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='grey', alpha=0.6, arrows=True, ax=ax)
    
    plt.title('Flight Route Network with World Map Overlay (Cartopy)')
    plt.show()

def main():
    """Main function to load data, create the graph, and plot it."""
    routes = load_route_data()
    G = create_graph(routes)
    plot_graph(G)

if __name__ == "__main__":
    main()