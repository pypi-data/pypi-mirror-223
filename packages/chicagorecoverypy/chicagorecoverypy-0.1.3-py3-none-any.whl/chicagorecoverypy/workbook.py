class ActivityWorkbook(object):
    def __init__(self, workbook):
        self.workbook = workbook

    @property
    def cover_sheet(self):
        (sheet_name,) = [
            c for c in self.workbook.ws_names if c.lower() == "cover sheet"
        ] or ["Cover Sheet"]
        worksheet = self.workbook.ws(sheet_name)
        return dict(zip(worksheet.row(1), worksheet.row(4)))

    @property
    def records(self):
        try:
            worksheet = self.workbook.ws("Records")
        except:  # noqa
            worksheet = self.workbook.ws("Template")

        n_rows, _ = worksheet.size
        header = worksheet.row(1)
        start_row = 4

        try:
            assert "race/ethnicity" not in header
        except AssertionError:
            header = self.concatenate_nested_header(worksheet)
            start_row = 6

        for n in range(start_row, n_rows + 1):
            yield dict(zip(header, worksheet.row(n)))

    def concatenate_nested_header(self, worksheet):
        header = []
        current_grouping = ""
        current_category = ""

        try:
            n_cols = worksheet.row(2).index("Community Areas")
        except ValueError:
            n_cols = len(worksheet.row(2))

        for grouping, category, subcategory in zip(
            worksheet.row(1)[:n_cols],
            worksheet.row(2)[:n_cols],
            worksheet.row(3)[:n_cols],
        ):
            if grouping:
                current_grouping = grouping
                current_category = ""

            if category:
                current_category = category

            if subcategory.startswith("additional"):
                current_grouping = ""

            header.append(
                " ".join(
                    [
                        field
                        for field in (current_grouping, current_category, subcategory)
                        if field
                    ]
                ).strip()
            )

            # Remove grouping after last age field
            if (
                current_grouping == "age" and subcategory == "unknown"
            ) or current_grouping.lower() == "sexual orientation":
                current_grouping = ""

        return header
