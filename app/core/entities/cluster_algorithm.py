from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

class ClusterAlgorithm:

    def dbscan(self, vectors, ep, minPts):
        self.cluster_model = DBSCAN(eps=ep, min_samples=minPts)
        labels = self.cluster_model.fit_predict(vectors)

        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        print("Estimated number of clusters: %d" % n_clusters_)
        print("Estimated number of noise points: %d" % n_noise_)


        unique_labels = set(labels)
        core_samples_mask = np.zeros_like(labels, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True

        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 0, 1]

            class_member_mask = labels == k

            xy = X[class_member_mask & core_samples_mask]
            plt.plot(
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                markeredgecolor="k",
                markersize=14,
            )

            xy = X[class_member_mask & ~core_samples_mask]
            plt.plot(
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=tuple(col),
                markeredgecolor="k",
                markersize=6,
            )

        plt.title(f"Estimated number of clusters: {n_clusters_}")
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

    