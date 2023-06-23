from django.shortcuts import render
import plotly.express as px
from totolyzer.models import TotoResults, DrawDates
from totolyzer.forms import DateForm
from django.db.models import Sum,F,IntegerField
from django.db.models.functions import Concat

title_layout = {
            'font_size': 16,
            'xanchor': 'center',
            'x': 0.5
        }
margin_layout = {
            't': 26
        }

def frequency_chart(results):

    x = [i for i in range(1,50)]
    y = [results[i] for i in range(1,50)]
    fig = px.line(
        x=x,
        y=y,
        title="Number of Times Won",
        labels={'x': 'Winning Number', 'y': 'Frequency'}
    )
    fig.update_layout(title=title_layout,margin=margin_layout)
    chart = fig.to_html()
    return chart

def most_frequent_numbers_chart(results):

    top_10_fields = sorted(results.items(), key=lambda x: x[1], reverse=True)[:6]
    
    columns = [str(item[0]) for item in top_10_fields]
    counts = [item[1] for item in top_10_fields]
    # create the bar chart
    fig = px.bar(x=columns, y=counts, color=columns, labels={'x':'Winning Number', 'y':'Frequency', 'color':'Legend'}, title='Top 6 Winning Numbers')
    fig.update_layout(title=title_layout,margin=margin_layout)
    chart = fig.to_html()
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

    results = {}
    for i in range(1,50):
        count = toto_results.aggregate(total=Sum(f'has_{i}'))['total']
        results[i] = count

    chart3 = frequency_chart(results)
    chart4 = most_frequent_numbers_chart(results)

    context = {
        'chart3': chart3,
        'chart4': chart4,
        'form': DateForm(),
        'start_date': start_date,
        'end_date': end_date}
    return render(request, 'totolyzer/simple_freq.html', context)
