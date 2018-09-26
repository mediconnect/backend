# deprecated slot model
# from django.db import models
#
# # Create your models here.
# from hospital.models import Hospital
# from disease.models import Disease
#
# class Slot:
#     hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, unique=False, default=None, null=True,
#                                  related_name='hospital_slot')
#     disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, unique=False, default=None, null=True,
#                                 related_name='disease_slot')
#     default_slots = models.IntegerField(default=20)
#     slots_open_0 = models.IntegerField(default=20)
#     slots_open_1 = models.IntegerField(default=20)
#     slots_open_2 = models.IntegerField(default=20)
#     slots_open_3 = models.IntegerField(default=20)
#
#     class Meta:
#         db_table = 'db_slot'
#
#     def reset_slot(self):
#         self.slots_open_0 = self.slots_open_1
#         self.slots_open_1 = self.slots_open_2
#         self.slots_open_2 = self.slots_open_3
#         self.slots_open_3 = self.default_slots
#         self.save()
#
#     def set_slots(self, slot_dic={}):
#         self.default_slots = slot_dic[0]
#         self.slots_open_0 = slot_dic[1]
#         self.slots_open_1 = slot_dic[2]
#         self.slots_open_2 = slot_dic[3]
#         self.slots_open_3 = slot_dic[4]
#         self.save()
