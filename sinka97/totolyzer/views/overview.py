from django.shortcuts import render
import pandas as pd
from totolyzer.models import TotoResults, DrawDates
from django.db.models import Sum
from .constants import TITLE_LAYOUT,MARGIN_LAYOUT
from .simple_freq import get_frequent_numbers


def overview_view(request):
    draw_dates = DrawDates.objects.all()
    draw_dates = draw_dates.filter(date__gte='2014-10-07')
    toto_draw_ids = draw_dates.values_list('toto_draw_id', flat=True)
    toto_results = TotoResults.objects.filter(toto_draw_id__in=toto_draw_ids)

    field_names = [f'has_{i}' for i in range(1,50)]
    results = toto_results.values(*field_names)

    # Get Latest Numbers
    latest_result = toto_results.latest('toto_draw_id')
    # Initialize an empty list to store winning numbers
    latest_winning_numbers = []
    # Loop over all 'has_n' fields
    for i in range(1, 50):
        if getattr(latest_result, f'has_{i}') == 1:
            latest_winning_numbers.append(i)
    latest_draw_id = latest_result.toto_draw_id
    latest_additional_number = latest_result.additional_number

    # Get Frequent Numbers
    results = {}
    for i in range(1,50):
        count = toto_results.aggregate(total=Sum(f'has_{i}'))['total']
        results[i] = count
    most_frequent_six,least_frequent_six = get_frequent_numbers(results)

    context = {
        'latest_draw_id': latest_draw_id,
        'latest_winning_numbers': latest_winning_numbers,
        'latest_additional_number': latest_additional_number,
        'most_frequent_six': most_frequent_six,
        'least_frequent_six': least_frequent_six,
        }
    return render(request, 'totolyzer/overview.html', context)