from django.db import models
from datetime import date,datetime,time


class SoEmployee(models.Model):
    em_id_key = models.AutoField(primary_key=True)
    em_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Employee')
    em_zone = models.IntegerField(blank=True, null=True, verbose_name='Zone')
 
    class Meta:
        managed = True
        db_table = 'so_employees'
        ordering = ['em_name']
    def __str__(self) -> str:
        return self.em_name


class SoOut(models.Model):
    co_id_key = models.AutoField(primary_key=True)
    co_fk_em_id_key = models.ForeignKey('SoEmployee', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Employee')
    co_fk_type_id_key = models.ForeignKey('SoType', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Type',default=1)
    co_date = models.DateField(blank=True, null=True, default=date.today(), verbose_name='Date')
    #co_time_arrived = models.TimeField(auto_now=False, auto_now_add=True)
    co_time_arrived = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='Time Arrived', default=datetime.now().time().strftime('%I:%M'))
    co_time_dif = models.CharField(max_length=45, blank=True, null=True, verbose_name='Time Difference') 
  
    # def save(self, *args, **kwargs):
    #     if self.co_fk_type_id_key_id in [2, 3]:
    #         shift = Shift.objects.first()  # Assuming you have only one Shift instance
    #         red_start = shift.red_start
    #         red_end = shift.red_end
    #         time_diff = datetime.combine(datetime.today(), red_end) - datetime.combine(datetime.today(), red_start)
    #         minutes = int(time_diff.total_seconds() // 60)
    #         if self.co_fk_type_id_key_id == 2:
    #             minutes *= 2
    #         elif self.co_fk_type_id_key_id == 3:
    #             minutes *= 3
    #         hours = minutes // 60
    #         minutes %= 60
    #         self.co_time_dif = f"{hours:02d}:{minutes:02d}"
    #     super().save(*args, **kwargs)
    
    class Meta:
        managed = True
        db_table = 'so_outs'
        verbose_name = 'SO Out' 
        ordering = ['-co_date']

    def __str__(self) -> str:
        return str(self.co_fk_em_id_key)


class SoType(models.Model):
    type_id_key = models.AutoField(primary_key=True)
    description = models.CharField(max_length=45, blank=True, null=True, default="Tardy")

    class Meta:
        managed = True
        db_table = 'so_types'
    def __str__(self) -> str:
        return self.description
    

class Shift(models.Model):
    yellow_start = models.TimeField(blank=True, null=True, verbose_name='Yellow Zone Start', default=time(hour=6, minute=15))
    red_start = models.TimeField(blank=True, null=True, verbose_name='Red Zone Start', default=time(hour=5, minute=00))
    green_start = models.TimeField(blank=True, null=True, verbose_name='Green Zone Start', default=time(hour=4, minute=45))
    
    yellow_end = models.TimeField(blank=True, null=True, verbose_name='Yellow Zone End', default=time(hour=14, minute=45))
    red_end = models.TimeField(blank=True, null=True, verbose_name='Red Zone End', default=time(hour=13, minute=15))
    green_end = models.TimeField(blank=True, null=True, verbose_name='Green Zone End', default=time(hour=12, minute=30))
   
    class Meta:
        managed = True
        db_table = 'shiftstart'

    def save(self, *args, **kwargs):
        # Delete existing Shift object before saving new one
        Shift.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return "Zone start time"