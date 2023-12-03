import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from app.schemas import Purchase


def create_recommendation_matrix(purchases: list[Purchase]):
    data = {
        "user_id": [],
        "product_id": [],
    }

    for purchase in purchases:
        data["user_id"].append(purchase.user_id)
        data["product_id"].append(purchase.product_id)

    purchase_history = pd.DataFrame(data)

    purchase_counts = (
        purchase_history.groupby(["user_id", "product_id"]).size().unstack(fill_value=0)
    )

    sparse_purchase_counts = sparse.csr_matrix(purchase_counts)

    cosine_similarities_products = cosine_similarity(sparse_purchase_counts.T)

    return (
        purchase_counts,
        sparse_purchase_counts,
        cosine_similarities_products,
    )


def recommend_items(purchases, user_id, n=5):
    (
        purchase_counts,
        sparse_purchase_counts,
        cosine_similarities_products,
    ) = create_recommendation_matrix(purchases=purchases)

    user_history = sparse_purchase_counts[user_id].toarray().flatten()

    aggregated_similarities = np.zeros(cosine_similarities_products.shape[1])

    for idx, purchased in enumerate(user_history):
        if purchased > 0:
            product_similarities = cosine_similarities_products[idx]

            aggregated_similarities += purchased * product_similarities

    aggregated_similarities[user_history.nonzero()[0]] = 0

    recommended_indices = np.argsort(aggregated_similarities)[::-1][:n]
    recommended_items = list(purchase_counts.columns[recommended_indices])

    purchased_items = list(purchase_counts.columns[purchase_counts.loc[user_id] > 0])
    recommended_items = [
        item for item in recommended_items if item not in purchased_items
    ]

    return recommended_items
