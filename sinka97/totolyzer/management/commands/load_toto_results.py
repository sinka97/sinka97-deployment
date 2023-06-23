from django.core.management.base import BaseCommand
import csv
from datetime import datetime,date
from django.conf import settings
from totolyzer.models import TotoResults,DrawDates

class Command(BaseCommand):
    help = 'Load seed data from csv file into TotoResults and DrawDates tables'

    def handle(self,*args,**kwargs):
        datafile = settings.BASE_DIR / 'totolyzer' / 'data' / 'ToTo.csv'
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row_draw_id = row['Draw']
                row_date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
                row_year = row_date.year
                row_month = row_date.month
                row_day = row_date.day
                row_day_of_week = row_date.strftime("%A")
                winning_num_1 = row['Winning Number 1']
                winning_num_2 = row['2']
                winning_num_3 = row['3']
                winning_num_4 = row['4']
                winning_num_5 = row['5']
                winning_num_6 = row['6']
                additional_num = row['Additional Number ']
                
                toto_results, _ = TotoResults.objects.get_or_create(toto_draw_id=row_draw_id,
                                                  defaults={
                                                      f'has_{winning_num_1}':1,
                                                      f'has_{winning_num_2}':1,
                                                      f'has_{winning_num_3}':1,
                                                      f'has_{winning_num_4}':1,
                                                      f'has_{winning_num_5}':1,
                                                      f'has_{winning_num_6}':1,
                                                      'additional_number': additional_num
                                                  })
                DrawDates.objects.get_or_create(date=row_date,toto_draw_id=toto_results,
                                                year=row_year,month=row_month,day=row_day,
                                                day_of_week=row_day_of_week)
                