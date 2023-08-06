import plotly.graph_objects as go
from pandas.api.types import is_numeric_dtype
from .date import get_date_columns


def plot_pie_chart(df, categorical_col, num_col, return_fig=False):
    """
    Plot a pie chart based on the provided DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        categorical_col (str): The name of the column in the DataFrame that represents the categorical variable.
        num_col (str): The name of the column in the DataFrame that contains the numerical values.
        return_fig (bool, optional): If True (default is False), the function returns the Plotly Figure instead of showing it.

    Returns:
        plotly.graph_objs._figure.Figure (optional): A Plotly Figure representing the pie chart. 
                                                    (Returned only if 'return_fig' is True.)

    Example:
        >>> import pandas as pd
        >>> data = {
        ...     'Category': ['A', 'B', 'C', 'A', 'B', 'C'],
        ...     'Value': [100, 200, 300, 400, 500, 600]
        ... }
        >>> df = pd.DataFrame(data)
        >>> plot_pie_chart(df, 'Category', 'Value')
        # This will display a pie chart based on the 'Category' and 'Value' columns in the DataFrame.

        >>> pie_chart_figure = plot_pie_chart(df, 'Category', 'Value', return_fig=True)
        # This will return the Pie chart as a Plotly Figure without displaying it.
    """

    new_df = df[[categorical_col, num_col]]
    new_df = new_df.groupby(categorical_col).sum().reset_index()
    
    labels = new_df[categorical_col]
    values = new_df[num_col]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text="Distribution of "+ num_col + " by "+categorical_col)

    if return_fig:
        return fig
    else:
        fig.show()
    
def plot_time_series(df, date_col=None, categorical_col=None, num_cols=None):
    """
    Plot time series data from a DataFrame.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing time series data.
        date_col (str, optional): The name of the column in the DataFrame representing dates or timestamps.
                                  If not provided, the function will try to automatically detect a suitable date column.
        categorical_col (str, optional): The name of the column in the DataFrame representing categories or groups.
                                         If provided, the function will generate separate plots for each category.
        num_cols (list of str, optional): A list of column names in the DataFrame containing numerical data to be plotted.
                                          If not provided, all numeric columns will be used.

    Raises:
        ValueError: If the provided `date_col` is not found in the DataFrame, or if there is more than one potential
                    date column when `date_col` is not specified, or if any of the columns in `num_cols` are not
                    numeric columns in the DataFrame.

    Returns:
        None: The function displays the generated plots using the Plotly library.

    Example:
        # Basic usage - plot all numeric columns by default date column
        plot_time_series(df)

        # Plot specific numeric columns with a specified date column
        plot_time_series(df, date_col='date_column', num_cols=['column_A', 'column_B'])

        # Plot time series for specific categories using a categorical column
        plot_time_series(df, date_col='date_column', categorical_col='category_column', num_cols=['column_C'])
    """
    
    # Check date_col
    if date_col is None:
        date_col = get_date_columns(df)
        if type(date_col) is not str:
            raise ValueError("There is more than one date column.", date_col)
    else:
        cols = get_date_columns(df)
        if date_col not in cols:
            raise ValueError(date_col," is not a date column")
        
    # Check num_cols
    all_num_cols = []
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            all_num_cols.append(col)
    
    if num_cols is None:
        num_cols = all_num_cols
    elif set(num_cols).issubset(set(all_num_cols)) == False:
        raise ValueError(num_cols, " aren\'t all numerical columns")
    
    if categorical_col is None:
        new_df = df.groupby(date_col).sum().reset_index()
        for num in num_cols:
            fig = go.Figure(data=go.Scatter(x=list(new_df[date_col]), y=list(new_df[num]), mode='lines'))
            fig.update_layout(title_text=num + " overtime")
            fig.show()
    else:
        new_df = df.groupby([categorical_col, date_col]).sum().reset_index(date_col)
        
        for num in num_cols:
            fig = go.Figure()
            for cat in new_df.index.unique():
                fig.add_trace(go.Scatter(x=list(new_df.loc[cat][date_col]), y=list(new_df.loc[cat][num]), name=cat))
                fig.update_layout(title_text=num + " overtime")
            fig.show()



