import matplotlib.pyplot as plt

def visualize_similarity_results(query_text, similar_text_ids, distances):
    """
    Visualize the similarity search results.

    Parameters:
    - query_text: The query text used for the similarity search.
    - similar_text_ids: List of text IDs (CPFs) similar to the query.
    - distances: Corresponding distances for the similar text IDs.
    """
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjusted figure size

    y_pos = range(len(similar_text_ids))
    ax.barh(y_pos, distances, align='center', color='#556B2F')  # Set the color to moss green
    ax.set_yticks(y_pos)
    ax.set_yticklabels(similar_text_ids)
    ax.invert_yaxis()  # Reverse the order of IDs to have the most similar at the top
    ax.set_xlabel('Distância')
    ax.set_title(f'Similaridade semântica com "Desenvolver conhecimentos sobre as propriedades das biocerâmicas..."')

    plt.show()


from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt

def find_optimal_eps(vectors, k):
    """
    Calcula o k-NN de um conjunto de vetores e plota a distância k-NN para encontrar o eps ótimo para DBSCAN.

    Parâmetros:
    vectors (np.ndarray): Conjunto de vetores (dados de entrada).
    k (int): O valor de k para k-NN, que geralmente é definido como MinPts para DBSCAN.

    Retorna:
    None: Plota a distância k-NN.
    """
    # Compute k-nearest neighbors
    nbrs = NearestNeighbors(n_neighbors=k+1).fit(vectors)

    # get distances
    dist, ind = nbrs.kneighbors(vectors)

    # sort the distances of the k-th nearest neighbors
    k_dist = np.sort(dist[:, -1])

    # plot the k-distance graph
    plt.figure(figsize=(10, 5))
    plt.plot(k_dist)
    plt.xlabel('Pontos ordenados pela distância')
    plt.ylabel(f'{k}-Distância')
    plt.title(f'{k}-Distância para Determinação do eps Ótimo')
    plt.grid(True)
    plt.show()