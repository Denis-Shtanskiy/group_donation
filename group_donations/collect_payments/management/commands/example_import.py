"""Пример импорта из CSV-файла, для модели Reason."""

from collect_payments.management.commands.base_command import ImportCsvCommand
from collect_payments.models import Reason


class Command(ImportCsvCommand):
    help = 'Импорт поводов из файла CSV.'

    def process_row(self, row):
        Reason.objects.get_or_create(
            name=row['день рождения'], color=row['#AAA34F'],
            slug=row['birthday']
        )
