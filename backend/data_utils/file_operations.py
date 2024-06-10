import json
import os
from typing import Any


class FileOperations:
    def __init__(self):
        self.output_data_path = 'output_data'
        self.filename = 'results.json'
        self.file_path = os.path.join(self.output_data_path, self.filename)
        self.plots_path = os.path.join(self.output_data_path, 'plots')

    def create_dirs(self) -> None:
        os.makedirs(self.output_data_path, exist_ok=True)
        os.makedirs(self.plots_path, exist_ok=True)

    def save_results_to_file(self, results) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)

    def get_saved_results_from_file(self) -> Any:
        with open(os.path.join(self.file_path), 'r') as file:
            data = json.loads(file.read())
            return data

    def get_filename_for_plot_for_given_operation(self, operation) -> str:
        return os.path.join(self.plots_path, f'{operation}_PLOT.png')
