import logging

import pipmaster as pm

logging.basicConfig(level=logging.DEBUG)

logging.debug('檢查 pipmaster 是否已安裝...')
if not pm.is_installed('pyvis'):
    logging.debug('pyvis 未安裝，嘗試安裝...')
    pm.install('pyvis')
    logging.debug('pyvis 安裝完成。')
else:
    logging.debug('pyvis 已安裝。')
if not pm.is_installed('networkx'):
    logging.debug('networkx 未安裝，嘗試安裝...')
    pm.install('networkx')
    logging.debug('networkx 安裝完成。')
else:
    logging.debug('networkx 已安裝。')

import random

import networkx as nx
from pyvis.network import Network

# Load the GraphML file
try:
    G = nx.read_graphml('./dickens/graph_chunk_entity_relation.graphml')
    logging.debug('GraphML 檔案讀取成功。')
except Exception as e:
    logging.error(f'GraphML 檔案讀取失敗：{e}')
    raise

# Create a Pyvis network
net = Network(height='100vh', notebook=True, cdn_resources='in_line')

# Convert NetworkX graph to Pyvis network
net.from_nx(G)


# Add colors and title to nodes
for node in net.nodes:
    node['color'] = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
    if 'description' in node:
        node['title'] = node['description']

# Add title to edges
for edge in net.edges:
    if 'description' in edge:
        edge['title'] = edge['description']

import codecs

# Save and display the network
try:
    net.show('knowledge_graph.html', notebook=False)
    html = net.html
    with codecs.open('knowledge_graph.html', 'w', 'utf-8') as f:
        f.write(html)
    logging.debug('知識圖譜已成功儲存為 knowledge_graph.html。')
except Exception as e:
    logging.error(f'知識圖譜儲存失敗：{e}')
    raise
