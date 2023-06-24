from django.shortcuts import render
import plotly.express as px
from totolyzer.models import TotoResults, DrawDates
from totolyzer.forms import DateForm
from django.db.models import Sum
from .constants import TITLE_LAYOUT,MARGIN_LAYOUT

def frequency_chart(results):
   
    columns = [i for i in range(1,50)]
    counts = [results[i] for i in range(1,50)]

    fig = px.bar(x=columns, y=counts, color=columns, labels={'x':'Number', 'y':'Frequency'}, title="Number of Times Won")
    fig.update_layout(title=TITLE_LAYOUT,margin=MARGIN_LAYOUT)
    fig.update_coloraxes(showscale=False)
    fig.update_traces(hovertemplate='Winning Number: %{x}<br>Frequency: %{y}')

    chart = fig.to_html(full_html=False, config={'displayModeBar': False})
    return chart

def simple_freq_view(request):
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

    chart1 = frequency_chart(results)

    context = {
        'chart1': chart1,
        'form': DateForm(),
        'start_date': start_date,
        'end_date': end_date}
    return render(request, 'totolyzer/simple_freq.html', context)
