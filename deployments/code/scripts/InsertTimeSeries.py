# /opt/collaboraoffice/share/Scripts/python
# Reference: https://sdk.collaboraonline.com/docs/Using_Python_scripting_in_Collabora_Online.html

import uno
import datetime
import random

def InsertTimeSeries(args):
    # Get the doc from the scripting context which is made available to
    # all scripts.
    
    # The context variable is of type XScriptContext and is available to
    # all BeanShell scripts executed by the Script Framework
    model = XSCRIPTCONTEXT.getDocument()

    # Check if the current component is a spreadsheet document
    if model.supportsService("com.sun.star.sheet.SpreadsheetDocument"):
        # Access the first sheet (0-index based)
        sheet = model.Sheets.getByIndex(0)

        # Generate 10,000 random time series data points
        start_date = datetime.datetime(2023, 1, 1, 0, 0, 0)  # Starting date
        time_step = datetime.timedelta(minutes=1)  # Time step (1 minute interval)
        num_rows = 10000
        ctrlr = model.CurrentController
        sel = ctrlr.getSelection()
        oArea = sel.getRangeAddress()
        first_row = oArea.StartRow
        first_col = oArea.StartColumn

        for i in range(num_rows):
            row = first_row + i
            timestamp = start_date + i * time_step
            value = random.uniform(0, 100)  # Random value between 0 and 100

            # Insert timestamp into column A and value into column B
            cell_A = sheet.getCellByPosition(first_col, row)  # Column A, Row i
            cell_B = sheet.getCellByPosition(first_col + 1, row)  # Column B, Row i
            cell_C = sheet.getCellByPosition(first_col + 2, row)  # Column B, Row i

            # Convert datetime to a string format
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            # Set cell values
            cell_A.setString(timestamp_str)
            cell_B.setValue(value)
            cell_C.setString(f"This is input {args}")
        
        first_cell = sheet.getCellByPosition(first_row, first_col)
        first_cell.Formula = f'=HYPERLINK("app://open-mapping-panel";"{first_cell.getString()}")'

    else:
        raise Exception("Current document is not a spreadsheet")

# Only the specified function will show in the Tools > Macro > Organize Macro dialog:
g_exportedScripts = (InsertTimeSeries,)