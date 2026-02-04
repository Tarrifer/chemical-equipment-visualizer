from rest_framework import serializers

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, value):
        max_size = 10 * 1024 * 1024
        
        if value.size > max_size:
            raise serializers.ValidationError(
                "File size cannot exceed 10MB"
            )
        
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError(
                "Only CSV files are allowed"
            )
        
        return value
