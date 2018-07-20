from hospital.models import Hospital


def hospital_setup(num=1):
    Hospital.objects.bulk_create(
        map(
            lambda i: Hospital(
                name="Dummy Hospital %d" % (i+1)
            ),
            range(num)
        )
    )
    return list(map(lambda h: h.id, Hospital.objects.all()))


class CommonSetup:

    def __init__(self,
        hospital=0,
    ):
        self.hospital = hospital_setup(hospital)
