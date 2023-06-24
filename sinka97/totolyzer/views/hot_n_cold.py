from django.shortcuts import render
import plotly.express as px
from totolyzer.models import TotoResults, DrawDates
from totolyzer.forms import DateForm
from django.db.models import Sum
from .constants import TITLE_LAYOUT,MARGIN_LAYOUT


def x_numbers_chart(results,order,x):
    fields = sorted(results.items(), key=lambda x: x[1], reverse=True)
    largest = fields[0][1] + fields[0][1]*0.05
    if order == 'asc':
        fields = fields[:x]
        custom_title = 'Hot Numbers (Most Frequent)'
        customer_marker_colour = '#FF0060'
    else:
        fields = fields[:-6:-1]
        custom_title = 'Cold Numbers (Least Frequent)'
        customer_marker_colour = '#0079FF'

    columns = [str(item[0]) for item in fields]
    counts = [item[1] for item in fields]

    fig = px.bar(x=columns, y=counts, color=columns, labels={'x':'Number', 'y':'Frequency'}, title=custom_title)
    fig.update_yaxes(range=[0, largest])
    fig.update_layout(showlegend=False,title=TITLE_LAYOUT,margin=MARGIN_LAYOUT)
    fig.update_traces(marker_color=customer_marker_colour,hovertemplate='Winning Number: %{x}<br>Frequency: %{y}')

    chart = fig.to_html(full_html=False, config={'displayModeBar': False})
    return chart

def hot_n_cold_view(request):
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

    results = {}
    for i in range(1,50):
        count = toto_results.aggregate(total=Sum(f'has_{i}'))['total']
        results[i] = count

    hot_chart = x_numbers_chart(results,'asc',6)
    cold_chart = x_numbers_chart(results,'dsc',6)

    context = {
        'hot_chart': hot_chart,
        'cold_chart': cold_chart,
        'form': DateForm(),
        'start_date': start_date,
        'end_date': end_date}
    return render(request, 'totolyzer/hot_n_cold.html', context)