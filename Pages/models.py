from django.db import models

# x


class Hospital(models.Model):
    Hospital_id = models.IntegerField(
        primary_key=True, unique=True, null=False, blank=False)
    Hospital_name = models.CharField(max_length=100, default='')
    Image = models.ImageField(upload_to="Hospital_images/", default="")

    def __str__(self):
        x = str(self.Hospital_id)
        return x


class Dept(models.Model):
    class Meta:
        unique_together = (('Uid', 'Hospital_id'),)

    Uid = models.IntegerField()
    Type = models.CharField(max_length=20, default='')
    Desc = models.TextField(default = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatem dignissimos aut voluptatum vero. Blanditiis officia natus odio placeat minima vero quod, magnam laborum, deleniti corporis, excepturi porro quo sunt perspiciatis ea ipsa fugit nihil atque! Nobis dolore explicabo officiis voluptatibus dignissimos odit perferendis, quam iste veniam. Aperiam nihil tenetur voluptatibus! Minus rem deserunt quas illo ipsum explicabo, officia illum sed accusantium, deleniti eveniet non. Labore quaerat tempora officiis ab fuga itaque dolor, sint fugit? Qui, obcaecati! Error in eius numquam officia inventore, assumenda consectetur fugit unde quasi quidem quos ea voluptas incidunt explicabo non reiciendis excepturi quo alias asperiores autem!")
    image = models.ImageField(upload_to="department_images/", default="")    
    route_image = models.ImageField(upload_to="Department_route", default="")
    Hospital_id = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, default='null')

    def __str__(self):
        return self.Type
