from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """Generate dense embeddings using a local BGE model."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5"
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

    def embed_documents(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        return vectors.tolist()

    def embed_query(
        self,
        query: str
    ) -> list[float]:

        vector = self.model.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False,
        )[0]

        return vector.tolist()