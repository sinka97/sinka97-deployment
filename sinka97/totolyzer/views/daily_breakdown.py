from django.shortcuts import render
import plotly.graph_objects as go
import pandas as pd
from totolyzer.models import DrawDates
from totolyzer.forms import DateForm
from .constants import TITLE_LAYOUT

def get_daily_sum_df(draw_dates):
    draw_dates = draw_dates.select_related('toto_draw_id')

    # Generating fields programmatically
    fields = ['date'] + [f'toto_draw_id__has_{i}' for i in range(1, 50)]

    # Retrieving only required fields
    draw_dates = draw_dates.values(*fields)

    # Converting QuerySet into DataFrame
    df = pd.DataFrame.from_records(draw_dates)
    one_to_fifty = [i for i in range(1, 50)]
    # Rename Columns
    df.columns = ['date'] + one_to_fifty
    df['date'] = pd.to_datetime(df['date'])
    one_to_fifty_odd = [i for i in range(1, 50, 2)]
    one_to_fifty_even = [i for i in range(2, 50, 2)]
    
    df['sum_all'] = df[one_to_fifty].mul(one_to_fifty).sum(axis=1)
    df['sum_delta'] = df['sum_all'].diff().abs()
    df.loc[df.index[0], 'sum_delta'] = 0
    df['sum_odd'] = df[one_to_fifty_odd].mul(one_to_fifty_odd).sum(axis=1)
    df['sum_even'] = df[one_to_fifty_even].mul(one_to_fifty_even).sum(axis=1)

    return df

def daily_breakdown_view(request):
    draw_dates = DrawDates.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        draw_dates = draw_dates.filter(date__gte=start_date)
    else:
        draw_dates = draw_dates.filter(date__gte='2014-10-07')
    if end_date:
        draw_dates = draw_dates.filter(date__lte=end_date)

    df = get_daily_sum_df(draw_dates)

    # Create the scatter plot using Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['sum_all'],
        mode='lines+markers',
        name='Total',
        marker=dict(color='#FF0060', size=4),
        line=dict(width=0.5),
        hovertemplate='<b>Date</b>: %{text}<br><b>Value</b>: %{y}<extra></extra>',
        text=df['date'].dt.strftime('%Y-%m-%d')
    ))

    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['sum_odd'],
        mode='lines+markers',
        name='Sum Odd',
        marker=dict(color='#c6db28', size=4),
        line=dict(width=0.5),
        hovertemplate='<b>Date</b>: %{text}<br><b>Value</b>: %{y}<extra></extra>',
        text=df['date'].dt.strftime('%Y-%m-%d')
    ))

    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['sum_even'],
        mode='lines+markers',
        name='Sum Even',
        marker=dict(color='#0079FF', size=4),
        line=dict(width=0.5),
        hovertemplate='<b>Date</b>: %{text}<br><b>Value</b>: %{y}<extra></extra>',
        text=df['date'].dt.strftime('%Y-%m-%d')
    ))

    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['sum_delta'],
        mode='markers',
        name='Delta',
        marker=dict(color='#5e28db', size=4, symbol='triangle-up'),
        hovertemplate='<b>Date</b>: %{text}<br><b>Value</b>: %{y}<extra></extra>',
        text=df['date'].dt.strftime('%Y-%m-%d')
    ))


    # Set the x-axis and y-axis labels
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Value',
        title=TITLE_LAYOUT,
        margin={'t':0}
    )

    sum_chart = fig.to_html(full_html=False, config={'displayModeBar': False})

    average_sum = round(df['sum_all'].mean(),2)
    average_even = round(df['sum_even'].mean(),2)
    average_odd = round(df['sum_odd'].mean(),2)
    average_delta = round(df['sum_delta'].mean(),2)

    ## Box-and-whisker
    # Create the box and whisker plots using Plotly graph objects
    box_fig = go.Figure()

    box_fig.add_trace(go.Box(
        y=df['sum_all'],
        name='sum_all',
        marker=dict(color='#FF0060')
    ))

    box_fig.add_trace(go.Box(
        y=df['sum_even'],
        name='sum_even',
        marker=dict(color='#0079FF')
    ))

    box_fig.add_trace(go.Box(
        y=df['sum_odd'],
        name='sum_odd',
        marker=dict(color='#c6db28')
    ))

    box_fig.update_layout(yaxis_title='Value', title=TITLE_LAYOUT, margin={'t': 0})
    box_fig.update_yaxes(range=[0, 279])
    box_chart = box_fig.to_html(full_html=False, config={'displayModeBar': False})

    sum_all_max = round(df['sum_all'].max())
    sum_all_min = round(df['sum_all'].min())
    sum_odd_max = round(df['sum_odd'].max())
    sum_odd_min = round(df['sum_odd'].min())
    sum_even_max = round(df['sum_even'].max())
    sum_even_min = round(df['sum_even'].min())

    context = {
        'form': DateForm(),
        'start_date': start_date,
        'end_date': end_date,
        'daily_breakdown_chart': sum_chart,
        'box_chart': box_chart,
        'average_sum': average_sum,
        'average_even': average_even,
        'average_odd': average_odd,
        'average_delta': average_delta,
        'sum_all_max': sum_all_max,
        'sum_odd_max': sum_odd_max,
        'sum_even_max': sum_even_max,
        'sum_all_min': sum_all_min,
        'sum_odd_min': sum_odd_min,
        'sum_even_min': sum_even_min}
    return render(request, 'totolyzer/daily_breakdown.html', context)