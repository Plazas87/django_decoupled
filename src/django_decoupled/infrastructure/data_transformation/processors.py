"""Data processor module."""
from typing import List

from django_decoupled.application.exceptions import TrainDatasetDataError

from ...application.dtos import TrainDataSet, WorkspaceDTO
from ...application.interfaces import IDataProcessor


class DataProcessorService(IDataProcessor[WorkspaceDTO, TrainDataSet]):
    """DataProcessorService class."""

    def generate_dataset(self, workspaces: List[WorkspaceDTO]) -> TrainDataSet:
        """Generate the dataset."""
        texts: List[str] = []
        classes: List[str] = []

        for workspace in workspaces:
            for category in workspace.categories:
                for document in category.documents:
                    texts.append(document.text)
                    classes.append(category.name)

        if len(texts) != len(classes):
            raise TrainDatasetDataError

        return TrainDataSet(texts=texts, classes=classes)
