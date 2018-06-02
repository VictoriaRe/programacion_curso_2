#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 23:22:19 2018

@author: victoriaregina
"""
import networkx as nx
import gensim
import matplotlib.pyplot as plt 
def downloading_model():
    m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
    if m.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
        model = gensim.models.KeyedVectors.load(m)
    model.init_sims(replace=True)
    return model

def creating_graph(model):
    sem_field=['детишки_NOUN', 'младенец_NOUN', 'ребенок_NOUN', 'малыш_NOUN', 'девочка_NOUN','мальчик_NOUN', 
           'подросток_NOUN', 'детей_NOUN', 'дитё_NOUN','ребятишки_NOUN']
    G = nx.Graph()
    G.add_nodes_from(sem_field)
    for word in sem_field:
        for w in sem_field:
            if word!=w:
                cos=model.similarity(word, w)
                if cos>0.5:
                    G.add_edge(word, w)              
    nx.write_gexf(G, 'graph_file.gexf')
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='blue', node_size=50) # рисуем узлы красным цветом, задаём размер узла
    nx.draw_networkx_edges(G, pos, edge_color='grey') # рисуем рёбра жёлтым
    nx.draw_networkx_labels(G, pos, font_size=7, font_family='Arial')
    plt.axis('off')
    plt.savefig('граф РЕБЕНОК', dpi=200, format='png')
    return G

def add_info(G):
    print('самые центральные слова графа:')
    deg = nx.degree_centrality(G)
    for nodeid in sorted(deg, key=deg.get, reverse=True):
        print(nodeid, G.degree(nodeid))
    print('коэффициент кластеризации:', nx.average_clustering(G))
    for l in list(nx.connected_component_subgraphs(G)):
        print('радиус компоненты связности:', nx.radius(l))

model=downloading_model()
graph=creating_graph(model)
add_info(graph)