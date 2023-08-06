import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, JsCode

# Dataset demo
data = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
col_names = ['Sepal_Length', 'Sepal_Width', 'Petal_Length', 'Petal_Width', 'Class']

# Custom CSS for AgGrid
custom_css = """
<style>
.ag-theme-alpine .ag-header-cell-text {
    font-weight: bold;
}

.ag-theme-alpine .ag-root {
    font-weight: bold;
}
</style>
"""

def upload():
    return st.file_uploader("Choose a file", type=["csv", "xls", "xlsx"])


def data_table(uploaded_file):

    if uploaded_file is not None:
        if uploaded_file.name.endswith(('.xls', '.xlsx')):
            # Read Excel (XLSX) file
            dataframe = pd.read_excel(uploaded_file)
        else:
            # Read CSV file
            dataframe = pd.read_csv(uploaded_file)
    else:
        # Load the Iris dataset by default for demonstration
        dataframe = pd.read_csv(data, names=col_names)
    # Custom CSS for AgGrid
    st.markdown(custom_css, unsafe_allow_html=True)

    # Get user-selected columns to color
    selected_features = st.multiselect("Please select training features", dataframe.columns)

    # Configure GridOptionsBuilder
    gb = GridOptionsBuilder.from_dataframe(dataframe)
    cellsytle_jscode = JsCode("""
    function(params) {
        var selectedFeatures = """ + str(selected_features) + """;
        var colName = params.colDef.field;
        var cellValue = params.value;

        if (selectedFeatures.includes(colName)) {
            return {
                'color': 'white',
                'backgroundColor': '#01205F'
            };
        } else {
            return {
                'color': 'black',
                'backgroundColor': 'white'
            };
        }
    };
    """)

    for feature in selected_features:
        gb.configure_column(feature, cellStyle=cellsytle_jscode)

    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    grid_response = AgGrid(
        dataframe,
        gridOptions=gridOptions,
        height=300,
        width='100%',
        alwaysShowHorizontalScroll=True,
        allow_unsafe_jscode=True
    )


