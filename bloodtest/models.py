from django.db import models

ORGAN_CHOICES = (
    ("adrenal_gland", _('Adrenal Gland')),
    ("bone", _('Bone')),
    ("heart", _('Heart')),
    ("kidney", _('Kidney')),
    ("liver", _('Liver')),
    ("pancreas", _('Pancreas')),
    ("thyroid", _('Thyroid'))
)

CONDITION_CHOICES = (
    ("diabetes", _('diabetes')),
    ("industrial_diseases", _('Industrial Diseases')),
    ("myasthenia_gravis", _('Myasthenia Gravis')),
    ("nutritional_disorders", _('Nutritional Disorders'))
)

# Create your models here.
class Organ(models.Model):
    name = models.CharField(max_length=255, choices=ORGAN_CHOICES, default=None)

    class Meta:
        verbose_name = _('Organ')
        verbose_name_plural = _("Organ")

    def __str__(self):
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length=255, choices=CONDITION_CHOICES, default=None)

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _("Condition")

    def __str__(self):
        return self.name
