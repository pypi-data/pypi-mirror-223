import logging

import mlflow
from sklearn import svm
from sklearn import datasets

import bentoml
from mlflow import MlflowClient

logging.basicConfig(level=logging.WARN)

if __name__ == "__main__":

    # Load training data
    iris = datasets.load_iris()
    X, y = iris.data, iris.target

    # Model Training
    clf = svm.SVC()
    clf.fit(X, y)

    # mlflow set
    # mlflow.set_registry_uri("https://kcai-mlflow-stage.is.kakaocorp.com/")
    # mlflow.sklearn.save_model(clf, "iris")



    # Save model to BentoML local model store
    saved_model = bentoml.sklearn.save_model(
        "iris_clf:0.0.3", clf, signatures={"predict": {"batchable": True, "batch_dim": 0}}
    )
    print(f"Model saved: {saved_model}")
