from django.shortcuts import render
import plotly.express as px
from totolyzer.models import DrawDates
from totolyzer.forms import DateForm
from .constants import TITLE_LAYOUT
from .daily_breakdown import get_daily_sum_df

def monthly_breakdown_view(request):
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

    ## Start of Month Name Section
    df_month_name = df[['date','sum_all','sum_even','sum_odd']].copy()
    # Extract month from the date
    df_month_name['Month'] = df_month_name['date'].dt.month_name()
    # Calculate the average values for each month
    df_avg = df_month_name.groupby('Month').mean().reset_index()

    ## Month Name Value Retrieval
    # Get Highest Month for each cat
    highest_sum_all_month = df_avg.loc[df_avg['sum_all'].idxmax(), 'Month']
    lowest_sum_all_month = df_avg.loc[df_avg['sum_all'].idxmin(), 'Month']
    # Calculate the difference between 'sum_even' and 'sum_odd' values
    df_avg['even_odd_difference'] = df_avg['sum_even'] - df_avg['sum_odd']
    # Find the month with the biggest difference
    month_with_biggest_difference = df_avg.loc[df_avg['even_odd_difference'].idxmax(), 'Month']

    # Plot bar chart using Plotly Express
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    colors = {'sum_all': '#FF0060', 'sum_odd': '#c6db28', 'sum_even': '#0079FF'}
    bar_fig = px.bar(df_avg, x='Month', y=['sum_all','sum_even','sum_odd'],category_orders={'Month': month_order},color_discrete_map=colors)
    # Set the x-axis and y-axis labels
    bar_fig.update_layout(xaxis_title='Month', yaxis_title='Average Value', title=TITLE_LAYOUT, margin={'t': 0})
    # Convert chart to HTML
    month_name_chart = bar_fig.to_html(full_html=False, config={'displayModeBar': False})


    ## Start of Year-Month Section
    # Resample to calculate average values per month
    df_monthly = df[['date','sum_all','sum_even','sum_odd']].copy()
    df_monthly = df_monthly.resample('M', on='date').mean()
    # Plot multiple line graph using Plotly Express
    line_fig = px.line(df_monthly, x=df_monthly.index, y=['sum_all', 'sum_even', 'sum_odd'])
    # Set the x-axis and y-axis labels
    line_fig.update_layout(xaxis_title='Month', yaxis_title='Value', title=TITLE_LAYOUT, margin={'t': 0})
    monthly_chart = line_fig.to_html(full_html=False, config={'displayModeBar': False})
    average_sum = round(df['sum_all'].mean(),2)
    average_even = round(df['sum_even'].mean(),2)
    average_odd = round(df['sum_odd'].mean(),2)

    context = {
        'form': DateForm(),
        'start_date': start_date,
        'end_date': end_date,
        'month_name_chart': month_name_chart,
        'highest_sum_all_month': highest_sum_all_month,
        'lowest_sum_all_month': lowest_sum_all_month,
        'month_with_biggest_difference': month_with_biggest_difference,
        'monthly_breakdown_chart': monthly_chart,
        'average_sum': average_sum,
        'average_even': average_even,
        'average_odd': average_odd,
    }
    return render(request, 'totolyzer/monthly_breakdown.html', context)