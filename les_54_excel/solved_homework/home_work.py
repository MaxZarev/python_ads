""""""

""" 
Реализовать метод у класса Excel:

    def get_column(self, column_name: str) -> list[str]:
        pass

    def get_row(self, row_name: str) -> list[str]:
        pass
    

Метод get_column должен возвращать список значений из столбца column_name.
Метод get_row должен возвращать список значений из строки row_name.

"""


def get_column(self, column_name: str) -> list[str]:
    col_num = self.find_col(column_name)
    if not col_num:
        raise ValueError(f"Column with name '{column_name}' not found.")
    column_values = []
    for raw in self.sheet.iter_cols(min_col=col_num, max_col=col_num, min_row=2):
        for cell in raw:
            column_values.append(cell.value)

    return column_values


def get_row(self, row_name: str) -> list[str]:
    row_num = self.find_row(row_name)
    if not row_num:
        raise ValueError(f"Row with name '{row_name}' not found.")
    row_values = []
    for raw in self.sheet.iter_rows(min_row=row_num, max_row=row_num):
        for cell in raw:
            row_values.append(cell.value)

    return row_values


