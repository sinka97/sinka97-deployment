from django.shortcuts import render
import plotly.express as px
import pandas as pd
import numpy as np
from totolyzer.models import TotoResults, DrawDates
from totolyzer.forms import DateForm
from .constants import TITLE_LAYOUT,MARGIN_LAYOUT

def best_pairs_view(request):
    draw_dates = DrawDates.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        draw_dates = draw_dates.filter(date__gte=start_date)
    else:
        draw_dates = draw_dates.filter(date__gte='2014-10-07')
    if end_date:
        draw_dates = draw_dates.filter(date__lte=end_date)
    
    toto_draw_ids = draw_dates.values_list('toto_draw_id', flat=True)
    toto_results = TotoResults.objects.filter(toto_draw_id__in=toto_draw_ids)

    if len(toto_results) == 0:
        context = {
            'form': DateForm(),
            'start_date': start_date,
            'end_date': end_date}
        return render(request, 'totolyzer/invalid_date.html', context)
    
    field_names = [f'has_{i}' for i in range(1,50)]
    results = toto_results.values(*field_names)
    df = pd.DataFrame.from_records(results)
    co_occur = pd.DataFrame(np.zeros((49, 49)), columns=['has_'+str(i+1) for i in range(49)], 
                            index=['has_'+str(i+1) for i in range(49)])
    for col1 in df.columns:
        for col2 in df.columns:
            co_occur.loc[col1, col2] = np.sum((df[col1] == 1) & (df[col2] == 1))

    # Set diagonal to be none to not count how often each number occurs with itself
    np.fill_diagonal(co_occur.values, np.nan)

    # Reshape the DataFrame into a Series and sort
    s = co_occur.unstack().sort_values(ascending=False)
    top_10_pairs = s[:10]
    # Get the indices of the top 10 values as a list of tuples
    top_10_pairs_list = [(pair[0].replace('has_','Number '),pair[1].replace('has_','Number '), int(co_occur.loc[pair])) for pair in top_10_pairs.index]

    # Rename the columns and the index
    new_names = [str(i+1) for i in range(49)]
    co_occur.columns = new_names
    co_occur.index = new_names
    
    fig = px.imshow(co_occur,
                    labels=dict(x="Winning Number", y="Winning Number", color="Co-occurrence"),
                    x=co_occur.columns,
                    y=co_occur.index,
                    color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)
    fig.update_layout(width=500, height=500)
    best_pairs_chart = fig.to_html(full_html=False, config={'displayModeBar': False})

    context = {
        'best_pairs_chart': best_pairs_chart,
        'top_10_pairs': top_10_pairs_list,
        'form': DateForm(),
        'start_date': start_date,
        'end_date': end_date}
    return render(request, 'totolyzer/best_pairs.html', context)