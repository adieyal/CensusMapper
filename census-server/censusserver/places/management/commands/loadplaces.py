from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import places.models as pmodels
import csv
import sys

class Command(BaseCommand):
    args = '<filename>'
    help = 'Populate the StatsSA place data'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        """
        """
        if len(args) != 1:
            raise CommandError("Expected a file path")

        reader = csv.reader(open(args[0]))
        headers = reader.next()

        cache = {}
        pmodels.Location.objects.all().delete()
        for i, line in enumerate(reader):
            try:
                sys.stderr.write("\r%d" % i)
                
                datum = dict(zip(headers, line))
                province = cache.get(datum["Province"], None)
                if not province:
                    province = pmodels.Location.objects.create(
                        type="PR", 
                        name=datum["Province"],
                        code=datum["Province"],
                    )
                    cache[datum["Province"]] = province

                district = cache.get(datum["DC_Code"], None)
                if not district:
                    district = pmodels.Location.objects.create(
                        type="DC", 
                        name=datum["DC_Name"],
                        code=datum["DC_Code"], 
                        parent=province
                    )
                    cache[datum["DC_Code"]] = district

                main_place = cache.get(datum["MP_Code"], None)
                if not main_place:
                    main_place = pmodels.Location.objects.create(
                        type="MP", 
                        name=datum["Main_Place"],
                        code=datum["MP_Code"], 
                        parent=district
                    )
                    cache[datum["MP_Code"]] = main_place

                sub_place = cache.get(datum["SP_Code"], None)
                if not sub_place:
                    sub_place = pmodels.Location.objects.create(
                        type="SP", 
                        name=datum["Sub_Place"],
                        code=datum["SP_Code"], 
                        parent=main_place
                    )
                    cache[datum["SP_Code"]] = sub_place

            except Exception, e:
                import traceback
                traceback.print_exc()
                
