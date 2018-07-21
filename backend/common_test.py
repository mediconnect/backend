from collections import defaultdict
from typing import List

from hospital.models import Hospital
from disease.models import Disease


def hospital_setup(num: int = 1) -> List:
    Hospital.objects.bulk_create(
        map(
            lambda i: Hospital(
                name="Dummy Hospital %d" % (i+1)
            ),
            range(num)
        )
    )
    return list(map(lambda h: h.id, Hospital.objects.all()))


def disease_setup(num: int = 1) -> List:
    Disease.objects.bulk_create(
        map(
            lambda i: Disease(
                name="Disease %d" % (i + 1)
            ),
            range(num)
        )
    )
    return list(map(lambda d: d.id, Disease.objects.all()))


class CommonSetup:

    def __init__(self,
                 hospital: int = 0,
                 disease: int = 0,
                 **kwargs
                 ):
        kwargs_map = defaultdict(dict)
        for kw, arg in kwargs.items():
            kwsplits = kw.split('_')
            if len(kwsplits) == 1:
                continue
            kwspace = kwsplits.pop(0)
            kwkey = '_'.join(kwsplits)
            kwargs_map[kwspace][kwkey] = arg

        self.hospital = hospital_setup(hospital)
        self.disease = disease_setup(disease)
