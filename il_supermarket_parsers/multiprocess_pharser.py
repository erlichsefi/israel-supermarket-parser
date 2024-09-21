from .raw_parsing_pipeline import RawParseingPipeline
from .utils.multi_prcoessing import MultiProcessor, ProcessJob
from .utils.logger import Logger
from .parser_factroy import ParserFactory
from .utils import FileTypesFilters
import itertools


class RawProcessing(ProcessJob):
    """converting file to database"""

    def job(self, **kwargs):
        """read the dump folder and filter according to the requested filters
        start processing file according to thier "update_date"
        """
        # take args
        drop_folder = kwargs.pop("data_folder")
        file_type = kwargs.pop("file_type")
        parser_name = kwargs.pop("type")
        parser_enum = ParserFactory.get(parser_name)

        return RawParseingPipeline(drop_folder, parser_enum, file_type).process()


class ParallelParser(MultiProcessor):
    """run insert task on parallel"""

    def __init__(self, data_folder, multiprocessing=6):
        super().__init__(multiprocessing=multiprocessing)
        self.data_folder = data_folder

    def task_to_execute(self):
        """the task to execute"""
        return RawProcessing

    def get_arguments_list(self):
        """create list of arguments"""

        all_parsers = ParserFactory.all_parsers_name()
        all_file_types = FileTypesFilters.all_full_files()
        params_order = ["type", "file_type", "data_folder"]
        combinations = list(
            itertools.product(
                all_parsers, all_file_types, all_file_types, self.data_folder
            )
        )
        task_can_executed_indepentlly = [
            dict(zip(params_order, combo)) for combo in combinations
        ]
        return task_can_executed_indepentlly
