from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class Sector(models.Model):
    nombre = models.CharField(max_length = 255, blank=True, null = False)

    def __str__(self):
        return f'Sector: {self.sector}'
    
    class Meta:
        verbose_name = 'sector'
        verbose_name_plural ='Sectores'

    def clean(self):
        if not self.numero:  
            raise ValidationError("El campo numero no puede estar vacío.")

        if not self.descripcion:
            raise ValidationError("El campo descripcion no puede estar vacío.")
                          
        super().clean() 

class TipoDocumento(models.Model):
    numero = models.IntegerField(blank=True, null=False)
    descripcion = models.CharField(max_length = 255, blank=True, null = False)

    def __str__(self):
        return f'Tipo de documento: {self.descripcion}'
    
    class Meta:
        verbose_name = 'tipo de documento'
        verbose_name_plural ='Tipos de documentos'

    def clean(self):
        if not self.numero:  
            raise ValidationError("El campo numero no puede estar vacío.")

        if not self.descripcion:
            raise ValidationError("El campo descripcion no puede estar vacío.")
                          
        super().clean() 


class Documento(models.Model):
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    ejercicio = models.CharField(max_length = 4, blank=True, null=True)

    fecha_alta = models.DateField(auto_now_add=True, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, blank=True, null=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True )

    ultima_actualizacion = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Documento: {self.tipo}. Numero: {self.numero}'
    
    class Meta:
        verbose_name = 'documento'
        verbose_name_plural ='Documentos'

    def clean(self):
        if not self.tipo or not self.numero or not self.ejercicio:
            raise ValidationError("Los campos tipo, numero y ejercicio no pueden estar vacíos.")
          
        super().clean() 

    def save(self, *args, **kwargs):
        if self.existe():
            raise ValidationError("El documento ya esta registrado en el sistema")
        
        

        super(Documento, self).save(*args, **kwargs)

    def existe(instance):
        return Documento.objects.filter(tipo = instance.tipo, numero = instance.numero, ejercicio = instance.ejercicio).exclude(pk=instance.pk).exists()


class Transferencia(models.Model):
    estado_choice = (
        ('en_transito', 'en_transito'),
        ('confirmado', 'confirmado'),
    )
        
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=estado_choice, default='en_transito',  blank=True, null=True)

    fecha = models.DateField(blank=True, null=True)
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    fecha_confirmacion = models.DateField(blank=True, null=True)
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    observacion = models.TextField(blank=True, null=True)


