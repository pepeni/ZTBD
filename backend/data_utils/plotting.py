import matplotlib.pyplot as plt
import numpy as np

from backend.data_utils.file_operations import FileOperations


class Plotting:
    def __init__(self):
        file_operations = FileOperations()
        self.data = file_operations.get_saved_results_from_file()
        self.file_operations = FileOperations()

    def create_charts_from_json(self):
        for operation in self.data.keys():
            self.create_bar_chart(operation, self.data[operation])

    def create_bar_chart(self, operation, data):
        databases = list(data.keys())

        rows = sorted(set(int(row) for db in databases for row in data[db].keys()))

        fig, ax = plt.subplots()

        bar_width = 0.15
        space = 0.05
        index = np.arange(len(rows))

        for i, db in enumerate(databases):
            if data[db]:
                times = [data[db].get(str(row), None) for (row) in rows]
                ax.bar(index + i * (bar_width + space), times, bar_width, label=db)

        ax.set_xlabel('Liczba wierszy')
        ax.set_ylabel('Czas (s)')
        ax.set_title(f'Czas wykonania operacji {operation}')
        ax.set_xticks(index + (len(databases) - 1) * (bar_width + space) / 2)
        ax.set_xticklabels(rows)
        ax.legend()

        plt.savefig(self.file_operations.get_filename_for_plot_for_given_operation(operation))
        plt.show()
        plt.close()
