# 3:

from rest_framework import serializers
from inmueblesList_app.models import Edificacion, Empresa, Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = "__all__"
    

class EdificacionSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True) # uniendo el model con el (related_name="comentarios")  # el nombre (related_name) es importante en los serializers para UNIFICAR LOS objetos JSON

    class Meta: 
        model = Edificacion
        fields = "__all__" # mapiando toda la clase entidad
        #fields = ['id', 'pais', 'active', 'imagen'] # mostrar personalizado.
        #exclude = ['id'] # que no me muestre ese campo.

class EmpresaSerializer(serializers.HyperlinkedModelSerializer):
    edificacionList = EdificacionSerializer(many=True, read_only=True) # uniendo

    # edificacionList = serializers.StringRelatedField(many=True) # solo el campo personalizado de la clase model selecionado.
    # edificacionList = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # edificacionList = serializers.HyperlinkedRelatedField( # Genera un URL por cada inmueble.
    #     many=True, 
    #     read_only=True,
    #     view_name='edificacion-detail',
    #     )

    class Meta:
        model = Empresa
        fields = "__all__" 


























    # Metodos de validacion, etc:
        
    # longitud_direccion = serializers.SerializerMethodField()

    # def get_longitud_direccion(self, object):
    #     cantidad_caracteres = len(object.direccion) 
    #     return cantidad_caracteres

    # def validate(self, data):
    #     if data['direccion'] == data['pais']:
    #         raise serializers.ValidationError("La direccion y el pais deben ser diferentes")
    #     else:
    #         return data

    # def validate_imagen(self, data):
    #     if len(data) < 2:
    #         raise serializers.ValidationError("La url de la imangen es muy corta")
    #     else:
    #         return data   


































# def column_longitud(value): # validacion de entidades
#     if len(value) < 2:
#         raise serializers.ValidationError("El valor es demasiado corta")


# class InmuebleSerializer(serializers.Serializer):

#     id = serializers.IntegerField(read_only=True)
#     direccion =  serializers.CharField(validators=[column_longitud])
#     pais = serializers.CharField(validators=[column_longitud])
#     descripcion = serializers.CharField()
#     imagen = serializers.CharField()
#     active = serializers.BooleanField()


#     def create(self, validated_data):
#         return Inmueble.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.direccion = validated_data.get('direccion', instance.direccion)
#         instance.pais = validated_data.get('pais', instance.pais)
#         instance.descripcion = validated_data.get('descripcion', instance.descripcion)
#         instance.imagen = validated_data.get('imagen', instance.imagen)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self, data):
#         if data['direccion'] == data['pais']:
#             raise serializers.ValidationError("La direccion y el pais deben ser diferentes")
#         else:
#             return data
    
#     def validate_imagen(self, data):
#         if len(data) < 2:
#             raise serializers.ValidationError("La url de la imangen es muy corta")
#         else:
#             return data
        