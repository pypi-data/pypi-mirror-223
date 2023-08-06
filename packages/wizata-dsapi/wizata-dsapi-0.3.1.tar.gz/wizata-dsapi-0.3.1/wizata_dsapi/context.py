import uuid
import pandas

from .mlmodel import MLModel
from .plot import Plot


class Context:
    """
    Context defines all properties, dataframes, models and other data passed through pipeline steps.
    """

    def __init__(self,
                 pipeline_id: uuid.UUID = None,
                 execution_id: uuid.UUID = None):
        self.pipeline_id = pipeline_id
        self.execution_id = execution_id

        self.models = {}
        self.dataframes = {}
        self.properties = {}
        self.plots = {}

        self.__new_plot = None
        self.__new_model = None

    def append(self, key: str, obj, overwrite: bool = True):
        """
        append an object (pandas.Dataframe or any properties)
        :param key: dictionary identifier - name inside your pipeline.
        :param obj: ML Model, Dataframe or any properties (must be JSON serializable type).
        :param overwrite: by default - allow modifying an existing object. can be set to false.
        """
        if key is None or key == "":
            raise KeyError('please provide a non empty key.')

        if isinstance(obj, pandas.DataFrame):
            if not overwrite and key in self.dataframes:
                raise KeyError(f'cannot overwrite existing dataframe in context with key {key}')
            self.dataframes[key] = obj
        else:
            if not overwrite and key in self.properties:
                raise KeyError(f'cannot overwrite existing properties in context with key {key}')
            self.properties[key] = obj

    def get(self, key: str):
        """
        get key from either dataframes, models, plots or properties.
        return None if not found.
        """
        if key in self.dataframes:
            return self.dataframes[key]
        elif key in self.models:
            return self.models[key]
        elif key in self.plots:
            return self.plots[key]
        elif key in self.properties:
            return self.properties[key]
        else:
            return None

    def set_plot(self, figure, name="Unkwown"):
        """
        set plot to be added to the context.
        :param figure: Plotly figure.
        :param name: Name of the plot.
        :return: Plot object prepared.
        """
        plot = Plot()
        plot.name = name
        plot.figure = figure
        self.__new_plot = plot
        return plot

    def get_plot(self) -> Plot:
        """
        get plot set to be added to the context.
        """
        return self.__new_plot

    def set_model(self, trained_model, input_columns, output_columns=None, has_anomalies=False, scaler=None):
        """
        set model to be added to the context.
        :param trained_model: Trained Model to be stored as a pickled object.
        :param input_columns: List of str defining input columns to call the model (df.columns)
        :param output_columns: List of output columns - Optional as can be detected automatically during validation.
        :param has_anomalies: False by default, define if the model set anomalies
        :param scaler: Scaler to be stored if necessary.
        :return: ML Model object prepared.
        """
        ml_model = MLModel()
        ml_model.trained_model = trained_model
        ml_model.scaler = scaler
        ml_model.input_columns = input_columns
        ml_model.output_columns = output_columns
        ml_model.has_anomalies = has_anomalies
        self.__new_model = ml_model
        return ml_model

    def get_model(self) -> MLModel:
        """
        get model to be added to the context.
        """
        return self.__new_plot

    def reset(self):
        """
        reset context will clear any pending plot or model to be added.
        """
        self.__new_plot = None
        self.__new_model = None
