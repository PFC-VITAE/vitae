from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import NearestNeighbors
import matplotlib.cm as cm
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

class ClusterAlgorithm:

    def find_optimal_eps(self, vectors, k):
        nbrs = NearestNeighbors(n_neighbors=k+1).fit(vectors)
        dist, ind = nbrs.kneighbors(vectors)
        
        k_dist = np.sort(dist[:, -1])
        
        plt.figure(figsize=(10, 5))
        plt.plot(k_dist)
        plt.xlabel('Pontos ordenados pela distância')
        plt.ylabel(f'{k}-Distância')
        plt.title(f'{k}-Distância para Determinação do eps Ótimo')
        plt.grid(True)
        plt.show()
        
        diff = np.diff(k_dist)
        diff2 = np.diff(diff)
        elbow_index = np.argmax(diff2) + 1  
        
        optimal_eps = k_dist[elbow_index]
        print(f"Optimal eps determined by elbow method: {optimal_eps}")
        
        return optimal_eps


    def kmeans(self, n, X):
        kmeans = KMeans(n_clusters=n, random_state=0).fit(X)
        plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_)
        plt.xlabel("Espaço de características para a 1ª feauture")
        plt.ylabel("Espaço de características para a 2ª feauture") 
        plt.title(f"KMeans com K={n}")
        plt.show()
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_
        return labels, centroids

    def kmeans_silhoutte(self, X):
        range_n_clusters = [2, 3, 4, 5, 6, 7]

        for n_clusters in range_n_clusters:
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.set_size_inches(18, 7)

            ax1.set_xlim([-0.1, 1])
            ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

            clusterer = KMeans(n_clusters=n_clusters, random_state=10)
            cluster_labels = clusterer.fit_predict(X)

            silhouette_avg = silhouette_score(X, cluster_labels)
            print(
                "Para n_clusters =",
                n_clusters,
                "A métrica de silhueta média é:",
                silhouette_avg,
            )

            sample_silhouette_values = silhouette_samples(X, cluster_labels)

            y_lower = 10
            for i in range(n_clusters):
                # Aggregate the silhouette scores for samples belonging to
                # cluster i, and sort them
                ith_cluster_silhouette_values = sample_silhouette_values[
                    cluster_labels == i
                ]

                ith_cluster_silhouette_values.sort()

                size_cluster_i = ith_cluster_silhouette_values.shape[0]
                y_upper = y_lower + size_cluster_i

                color = cm.nipy_spectral(float(i) / n_clusters)
                ax1.fill_betweenx(
                    np.arange(y_lower, y_upper),
                    0,
                    ith_cluster_silhouette_values,
                    facecolor=color,
                    edgecolor=color,
                    alpha=0.7,
                )

                ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

                y_lower = y_upper + 10  
            ax1.set_title("Representação da silhueta para diversos clusters.")
            ax1.set_xlabel("Valores do coeficiente de silhueta")
            ax1.set_ylabel("Rótulo do cluster")

            ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

            ax1.set_yticks([])  
            ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

            colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
            ax2.scatter(
                X[:, 0],
                X[:, 1],
                marker=".",
                s=30,
                lw=0,
                alpha=0.7,
                c=colors,
                edgecolor="k",
            )

            centers = clusterer.cluster_centers_
            ax2.scatter(
                centers[:, 0],
                centers[:, 1],
                marker="o",
                c="white",
                alpha=1,
                s=200,
                edgecolor="k",
            )

            for i, c in enumerate(centers):
                ax2.scatter(c[0], c[1], marker="$%d$" % i, alpha=1, s=50, edgecolor="k")

            ax2.set_title("Visualização dos dados agrupados.")
            ax2.set_xlabel("Espaço de características para a 1ª feauture")
            ax2.set_ylabel("Espaço de características para a 2ª feauture")

            plt.suptitle(
                "Análise de Silhueta para clusterização com K-Means com k= %d"
                % n_clusters,
                fontsize=14,
                fontweight="bold",
            )

        plt.show()

    def dbscan(self, vectors, ep, minPts):
        self.cluster_model = DBSCAN(eps=ep, min_samples=minPts).fit(vectors)
        labels = self.cluster_model.labels_

        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        print(f"Ep = {ep}, MinPts = {minPts}")
        print("Estimated number of clusters: %d" % n_clusters_)
        print("Estimated number of noise points: %d" % n_noise_)

        unique_labels = set(labels)
        core_samples_mask = np.zeros_like(labels, dtype=bool)
        core_samples_mask[self.cluster_model.core_sample_indices_] = True

        colors = [
            plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))
        ]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]

            class_member_mask = labels == k

            xy = vectors[class_member_mask & core_samples_mask]
            plt.plot(
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                markeredgecolor="k",
                markersize=14,
            )

            xy = vectors[class_member_mask & ~core_samples_mask]
            plt.plot(
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                markeredgecolor="k",
                markersize=6,
            )

        plt.title(f"Número de clusters: {n_clusters_} Número de ruídos: {n_noise_} (Eps={ep}, MinPts={minPts})")
        plt.show()
        return labels
