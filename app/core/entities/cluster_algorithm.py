from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np


import matplotlib.cm as cm

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
class ClusterAlgorithm:

    def kmeans(self, n, X):
        kmeans = KMeans(n_clusters=n, random_state=0).fit(X)
        plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_)
        plt.xlabel("Feature space for the 1st feature")
        plt.ylabel("Feature space for the 2nd feature")
        plt.title("KMeans Clustering")
        plt.show()
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_
        return labels, centroids

    def kmeans_silhoutte(self, X):
        range_n_clusters = [6, 7, 8, 9, 10]

        for n_clusters in range_n_clusters:
            # Create a subplot with 1 row and 2 columns
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.set_size_inches(18, 7)

            # The 1st subplot is the silhouette plot
            # The silhouette coefficient can range from -1, 1 but in this example all
            # lie within [-0.1, 1]
            ax1.set_xlim([-0.1, 1])
            # The (n_clusters+1)*10 is for inserting blank space between silhouette
            # plots of individual clusters, to demarcate them clearly.
            ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

            # Initialize the clusterer with n_clusters value and a random generator
            # seed of 10 for reproducibility.
            clusterer = KMeans(n_clusters=n_clusters, random_state=10)
            cluster_labels = clusterer.fit_predict(X)

            # The silhouette_score gives the average value for all the samples.
            # This gives a perspective into the density and separation of the formed
            # clusters
            silhouette_avg = silhouette_score(X, cluster_labels)
            print(
                "For n_clusters =",
                n_clusters,
                "The average silhouette_score is :",
                silhouette_avg,
            )

            # Compute the silhouette scores for each sample
            sample_silhouette_values = silhouette_samples(X, cluster_labels)

            y_lower = 10
            for i in range(n_clusters):
                # Aggregate the silhouette scores for samples belonging to
                # cluster i, and sort them
                ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

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

                # Label the silhouette plots with their cluster numbers at the middle
                ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

                # Compute the new y_lower for next plot
                y_lower = y_upper + 10  # 10 for the 0 samples

            ax1.set_title("The silhouette plot for the various clusters.")
            ax1.set_xlabel("The silhouette coefficient values")
            ax1.set_ylabel("Cluster label")

            # The vertical line for average silhouette score of all the values
            ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

            ax1.set_yticks([])  # Clear the yaxis labels / ticks
            ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

            # 2nd Plot showing the actual clusters formed
            colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
            ax2.scatter(
                X[:, 0], X[:, 1], marker=".", s=30, lw=0, alpha=0.7, c=colors, edgecolor="k"
            )

            # Labeling the clusters
            centers = clusterer.cluster_centers_
            # Draw white circles at cluster centers
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

            ax2.set_title("The visualization of the clustered data.")
            ax2.set_xlabel("Feature space for the 1st feature")
            ax2.set_ylabel("Feature space for the 2nd feature")

            plt.suptitle(
                "Silhouette analysis for KMeans clustering on sample data with n_clusters = %d"
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

        print("Estimated number of clusters: %d" % n_clusters_)
        print("Estimated number of noise points: %d" % n_noise_)

        unique_labels = set(labels)
        core_samples_mask = np.zeros_like(labels, dtype=bool)
        core_samples_mask[self.cluster_model.core_sample_indices_] = True

        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
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

        plt.title(f"Estimated number of clusters: {n_clusters_} (Eps={ep}, MinPts={minPts})")
        plt.show()
        return labels

    def test_dbscan_parameters(self, vectors, eps_values, min_samples_values, use_pca=True, n_components=2):
        if use_pca:
            pca = PCA(n_components=n_components)
            reduced_vectors = pca.fit_transform(vectors)
        else:
            reduced_vectors = vectors

        fig, axes = plt.subplots(len(eps_values), len(min_samples_values), figsize=(15, 10))
        fig.suptitle('DBSCAN Clusters para diferentes (Eps, MinPts)', fontsize=16)

        for i, eps in enumerate(eps_values):
            for j, min_samples in enumerate(min_samples_values):
                self.cluster_model = DBSCAN(eps=eps, min_samples=min_samples, metric='l2')
                labels = self.cluster_model.fit_predict(vectors)

                if use_pca:
                    data_to_plot = reduced_vectors
                else:
                    data_to_plot = TSNE(n_components=2).fit_transform(vectors)

                ax = axes[i, j]
                unique_labels = set(labels)
                colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

                for k, col in zip(unique_labels, colors):
                    if k == -1:
                        col = [0, 0, 0, 1]

                    class_member_mask = (labels == k)
                    xy = data_to_plot[class_member_mask]
                    ax.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                            markeredgecolor='k', markersize=6)

                ax.set_title(f'Eps={eps}, MinPts={min_samples}')
          

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    