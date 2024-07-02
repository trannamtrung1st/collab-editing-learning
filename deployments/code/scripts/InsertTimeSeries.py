# /opt/collaboraoffice/share/Scripts/python
# Reference: https://sdk.collaboraonline.com/docs/Using_Python_scripting_in_Collabora_Online.html

import uno
import datetime
import random

def uno_dispatch(command: str, args: list):
    """
    Dispatches a UNO command in LibreOffice with arguments.

    :param command: The UNO command to dispatch.
    :param args: A list of dictionaries, each representing an argument with "Name" and "Value".
    """
    # Access the current document and its context
    doc = XSCRIPTCONTEXT.getDocument()
    ctx = XSCRIPTCONTEXT.getComponentContext()

    # Create the dispatch helper
    smgr = ctx.getServiceManager()
    dispatcher = smgr.createInstanceWithContext("com.sun.star.frame.DispatchHelper", ctx)

    # Get the frame of the current document
    frame = doc.getCurrentController().getFrame()

    # Convert the arguments into a tuple of PropertyValue
    prop_values = []
    for arg in args:
        prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        if prop is None:
            raise RuntimeError("Failed to create PropertyValue instance")
        prop.Name = arg["Name"]
        prop.Value = arg["Value"]
        prop_values.append(prop)

    # Dispatch the command with arguments
    dispatcher.executeDispatch(frame, command, "", 0, tuple(prop_values))


def InsertTimeSeries(attribute, rows):
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
        ctrlr = model.CurrentController
        sel = ctrlr.getSelection()
        oArea = sel.getRangeAddress()
        first_row = oArea.StartRow
        first_col = oArea.StartColumn
        cell = sheet.getCellByPosition(first_col, first_row)  # Column A, Row i
        cell.setString(f'{attribute} {rows}')

        for i in range(rows):
            row = first_row + i
            timestamp = start_date + i * time_step
            value = random.uniform(0, 100)  # Random value between 0 and 100

            # Insert timestamp into column A and value into column B
            cell_A = sheet.getCellByPosition(first_col, row)  # Column A, Row i
            cell_B = sheet.getCellByPosition(first_col + 1, row)  # Column B, Row i

            # Convert datetime to a string format
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            # Set cell values
            if first_row == row:
                command = ".uno:SetHyperlink"
                args = [
                    {"Name": "Hyperlink.Text", "Value": timestamp_str},
                    {"Name": "Hyperlink.URL", "Value": f'app://open-mapping-panel?current_attribute={attribute}&rows={rows}'},
                    {"Name": "Hyperlink.Target", "Value": '_self'}
                ]
                uno_dispatch(command, args)
            else:
                cell_A.setString(timestamp_str)
            cell_B.setValue(value)

    else:
        raise Exception("Current document is not a spreadsheet")

# Only the specified function will show in the Tools > Macro > Organize Macro dialog:
g_exportedScripts = (InsertTimeSeries,)