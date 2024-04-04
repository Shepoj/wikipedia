import requests
from bs4 import BeautifulSoup
import matplotlib
import networkx as nx
import random
import matplotlib.pyplot as plt
import urllib.parse


starturl = "/wiki/Wikip%C3%A9dia"


def get_links(myurl):
    deja_vu = []
    response = requests.get(myurl)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        all_links = soup.find_all('a')

        for link in all_links:
            if 'href' in link.attrs:
                url = link['href']
                if url.startswith('/wiki/') and "501c" not in url and not url.startswith('/wiki/Fichier:') and not url.startswith(
                        '/wiki/Aide:') and not url.startswith('/wiki/Portail:') and not url.startswith(
                    '/wiki/Mod%C3%A8le:') and not url.startswith('/wiki/Projet:') and not url.startswith(
                    '/wiki/Utilisateur:') and not url.startswith('/wiki/Discussion:') and not url.startswith(
                    '/wiki/Cat%C3%A9gorie:') and not url.startswith('/wiki/Sp%C3%A9cial:') and not url.startswith(
                    '/wiki/Wikip%C3%A9dia:'):
                    deja_vu.append(url)
    else:
        print("La requête a échoué. Statut de la réponse :", response.status_code)
    return deja_vu


def get_random_link(page):
    links = get_links("https://fr.wikipedia.org" + page)
    random_link = random.choice(links)
    titled = titling(random_link)
    titledpage = titling(page)
    if random_link in graph.nodes:
        return get_random_link(page)
    graph.add_node(titled)
    if titled != titledpage:
        graph.add_edge(titledpage, titled)
    random_links = get_links("https://fr.wikipedia.org" + random_link)
    for i in random_links:
        i = titling(i)
        if i in graph.nodes and not graph.has_edge(titled, i) and i != titled:
            graph.add_edge(titled, i)
    return random_link


def titling(url):
    mots = urllib.parse.unquote(url.split("/")[2].split("#")[0]).split("_")
    return " ".join(mots)


def shift_color(color):
    # Function to shift the color
    return (color + random.random()*0.1-0.05) % 1.0  # Adjust the shifting factor as needed


def average_color(neighbors_colors):
    # Function to calculate the average color of neighbors
    return sum(neighbors_colors) / len(neighbors_colors)


graph = nx.Graph()

links = get_links("https://fr.wikipedia.org" + starturl)

graph.add_node(titling(starturl))
testurl = starturl

for i in range(800):
    testurl = get_random_link(testurl)

# Node colors dictionary to store node colors
node_colors = {}

# Iterate over each node to assign colors
for node in graph.nodes:
    neighbor_colors = [node_colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in node_colors]
    if neighbor_colors:
        avg_color = average_color(neighbor_colors)
        shifted_color = shift_color(avg_color)
        node_colors[node] = shifted_color
    else:
        node_colors[node] = random.random()  # Assign a random color to isolated nodes

# Draw the graph with assigned colors
nx.draw(graph, with_labels=True, node_size=30, width=0.1, font_size=8, node_color=list(node_colors.values()))
plt.show()
