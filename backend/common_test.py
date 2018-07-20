from hospital.models import Hospital


def common_setup(test_config):
    pass


def hospital_setup(num=1):
    for i in range(num):
        hospital = Hospital.objects.create(
            name="", # TODO: Finish this signature
        )