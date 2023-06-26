from django.shortcuts import render
import plotly.express as px
from totolyzer.models import TotoResults, DrawDates
from totolyzer.forms import DateForm
from django.db.models import Sum
from .constants import TITLE_LAYOUT,MARGIN_LAYOUT

def frequency_chart(results):
   
    columns = [i for i in range(1,50)]
    counts = [results[i] for i in range(1,50)]

    fig = px.bar(x=columns, y=counts, color=counts, labels={'x':'Number', 'y':'Frequency'}, title="Number of Times Won",
                 color_continuous_scale='Viridis_r')
    fig.update_layout(title=TITLE_LAYOUT,margin=MARGIN_LAYOUT)
    fig.update_coloraxes(showscale=False)
    fig.update_traces(hovertemplate='Winning Number: %{x}<br>Frequency: %{y}')

    chart = fig.to_html(full_html=False, config={'displayModeBar': False})
    return chart

def get_frequent_numbers(results):
    fields = sorted(results.items(), key=lambda x: x[1], reverse=True)
    most_frequent_six = [item[0] for item in fields[:6]]
    least_frequent_six = [item[0] for item in fields[:-6:-1]]
    return most_frequent_six,least_frequent_six

def mean_analysis_view(request):
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

    simple_frequency_chart = frequency_chart(results)
    most_frequent_six, least_frequent_six = get_frequent_numbers(results)

    context = {
        'simple_frequency_chart': simple_frequency_chart,
        'most_frequent_six': most_frequent_six,
        'least_frequent_six': least_frequent_six,
        'form': DateForm(),
        'start_date': start_date,
        'end_date': end_date}
    return render(request, 'totolyzer/mean_analysis.html', context)
