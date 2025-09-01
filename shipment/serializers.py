from rest_framework import serializers
from .models import Address, Service, Shipment

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    address = serializers.SlugRelatedField(
        queryset=Address.objects.all(),
        slug_field='street'
    )
    service = serializers.SlugRelatedField(
        queryset=Service.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Shipment
        fields = ['id', 'shipment_type', 'address', 'service', 'price']
        read_only_fields = ['price']

    def create(self, validated_data):
            shipment = Shipment(**validated_data)
            shipment.save()
            return shipment

    def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance