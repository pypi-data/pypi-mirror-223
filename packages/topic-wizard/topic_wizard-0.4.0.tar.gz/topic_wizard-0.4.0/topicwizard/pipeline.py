from typing import Iterable

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError
from sklearn.pipeline import Pipeline, _name_estimators
from sklearn.preprocessing import normalize

from topicwizard.prepare.topics import infer_topic_names


class TopicPipeline(Pipeline):
    """Scikit-learn compatible topic pipeline.
    It assigns topic names to the output, can return DataFrames
    and validates models and vectorizers.

    Parameters
    ----------
    steps: list of tuple of str and BaseEstimator
        Estimators in the pipeline. The first one has to
        be an sklearn compatible vectorizer, the last one
        has to be an sklearn compatible topic model.
    memory : str or object with the joblib.Memory interface, default None
        Used to cache the fitted transformers of the pipeline. The last step
        will never be cached, even if it is a transformer. By default, no
        caching is performed. If a string is given, it is the path to the
        caching directory. Enabling caching triggers a clone of the transformers
        before fitting. Therefore, the transformer instance given to the
        pipeline cannot be inspected directly. Use the attribute ``named_steps``
        or ``steps`` to inspect estimators within the pipeline. Caching the
        transformers is advantageous when fitting is time consuming.
    verbose : bool, default False
        If True, the time elapsed while fitting each step will be printed as it
        is completed.
    pandas_out: bool, default False
        If True, transform() will return a DataFrame.
    norm_row: bool, default True
        If True, every row in transform() will be sum-normalized so that
        they can be interpreted as probabilities.
    freeze: bool, default False
        If True, components of the pipeline will not be fitted when fit()
        is called. This is good for downstream uses of the topic model.

    Attributes
    ----------
    topic_names: list of str or None
        Inferred names of topics. Can be changed.
    vectorizer_: BaseEstimator
        Vectorizer model in the pipeline.
    topic_model_: BaseEstimator
        Topic model in the pipeline.
    """

    def __init__(
        self,
        steps: list[tuple[str, BaseEstimator]],
        *,
        memory=None,
        verbose=False,
        pandas_out=False,
        norm_row=True,
        freeze=False,
    ):
        super().__init__(steps, memory=memory, verbose=verbose)
        self.topic_names = None
        self.pandas_out = pandas_out
        self.norm_row = norm_row
        self.freeze = freeze
        if len(self) < 2:
            raise ValueError(
                "A Topic pipeline should at least have a vectorizer and a topic model."
            )
        _, self.vectorizer_ = self.steps[0]
        _, self.topic_model_ = self.steps[-1]
        if not hasattr(self.topic_model_, "transform"):
            raise TypeError("A topic model should have a transform method.")
        if not hasattr(self.vectorizer_, "transform"):
            raise TypeError("A vectorizer should have a transform method.")

    def _validate(self):
        if not hasattr(self.vectorizer_, "get_feature_names_out"):
            raise TypeError(
                "A fitted vectorizer should have a get_feature_names_out method."
            )
        if not hasattr(self.topic_model_, "components_"):
            raise TypeError("A fitted topic model should have a components_ attribute.")

    def fit(self, X: Iterable[str], y=None):
        """Fits the pipeline, infers topic names and validates that the
        individual estimators are indeed a vectorizer and a topic model.

        Parameters
        ----------
        X: iterable of str
            Texts to fit the model on.
        y: None
            Ignored, exists for compatibility.

        Returns
        -------
        self
            Fitted pipeline.
        """
        if not self.freeze:
            super().fit(X, y)
        self._validate()
        self.topic_names = infer_topic_names(self)
        return self

    def partial_fit(self, X, y=None, classes=None, **kwargs):
        """Fits the pipeline on a batch, infers topic names and validates that the
        individual estimators are indeed a vectorizer and a topic model.

        Parameters
        ----------
        X: iterable of str
            Texts to fit the model on.
        y: None
            Ignored, exists for compatibility.

        Returns
        -------
        self
            Fitted pipeline.
        """
        if not self.freeze:
            for name, step in self.steps:
                if not hasattr(step, "partial_fit"):
                    raise ValueError(
                        f"Step {name} is a {step} which does not have `.partial_fit` implemented."
                    )
            for name, step in self.steps:
                if hasattr(step, "predict"):
                    step.partial_fit(X, y, classes=classes, **kwargs)
                else:
                    step.partial_fit(X, y)
                if hasattr(step, "transform"):
                    X = step.transform(X)
        self._validate()
        self.topic_names = infer_topic_names(self)
        return self

    def transform(self, X: Iterable[str]):
        """Turns texts into a document-topic matrix.

        Parameters
        ----------
        X: iterable of str
            List of documents.

        Returns
        -------
        array or DataFrame of shape (n_documents, n_topics)
            Document-topic importance matrix.
        """
        if self.topic_names is None:
            raise NotFittedError("Topic pipeline has not been fitted yet.")
        X_new = super().transform(X)
        if self.norm_row:
            X_new = normalize(X_new, norm="l1", axis=1)
        if self.pandas_out:
            return pd.DataFrame(X_new, columns=self.topic_names)
        else:
            return X_new

    def get_feature_names_out(self):
        """Returns names of topics."""
        return self.topic_names

    def fit_transform(self, X: Iterable[str], y=None):
        """Fits the pipeline, infers topic names and validates that the
        individual estimators are indeed a vectorizer and a topic model.
        Then turns texts into a document-topic matrix.

        Parameters
        ----------
        X: iterable of str
            Texts to fit the model on.
        y: None
            Ignored, exists for compatibility.

        Returns
        -------
        array or DataFrame of shape (n_documents, n_topics)
            Document-topic importance matrix.
        """
        return self.fit(X, y).transform(X)

    def set_output(self, transform=None):
        """You can set the output of the pipeline to be a pandas dataframe.
        If you pass 'pandas' it will do this, otherwise it will disable pandas output.
        """
        if transform == "pandas":
            self.pandas_out = True
        else:
            self.pandas_out = False
        return self


def make_topic_pipeline(
    *steps, memory=None, verbose=False, pandas_out=False, norm_row=True, freeze=False
):
    """Shorthand for constructing a topic pipeline.

    Parameters
    ----------
    *steps: list of tuple of str and BaseEstimator
        Estimators in the pipeline. The first one has to
        be an sklearn compatible vectorizer, the last one
        has to be an sklearn compatible topic model.
    memory : str or object with the joblib.Memory interface, default None
        Used to cache the fitted transformers of the pipeline. The last step
        will never be cached, even if it is a transformer. By default, no
        caching is performed. If a string is given, it is the path to the
        caching directory. Enabling caching triggers a clone of the transformers
        before fitting. Therefore, the transformer instance given to the
        pipeline cannot be inspected directly. Use the attribute ``named_steps``
        or ``steps`` to inspect estimators within the pipeline. Caching the
        transformers is advantageous when fitting is time consuming.
    verbose : bool, default False
        If True, the time elapsed while fitting each step will be printed as it
        is completed.
    pandas_out: bool, default False
        If True, transform() will return a DataFrame.
    norm_row: bool, default True
        If True, every row in transform() will be sum-normalized so that
        they can be interpreted as probabilities.
    freeze: bool, default False
        If True, components of the pipeline will not be fitted when fit()
        is called. This is good for downstream uses of the topic model.


    """
    return TopicPipeline(
        _name_estimators(steps),
        memory=memory,
        verbose=verbose,
        pandas_out=pandas_out,
        norm_row=norm_row,
        freeze=freeze,
    )
