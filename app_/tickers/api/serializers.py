from rest_framework import serializers


from ..models import Ticker


class TickerSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='api_tickers:ticker_update')
    # analysis = serializers.HyperlinkedIdentityField(view_name='api_tickers:ticker_analysis')

    class Meta:
        model = Ticker
        fields = ['id', 'title', 'ticker', 'beta', 'coverage', 'market_variance', 'camp', 'price',
                  'simply_return', 'log_return', 'standard_deviation', 'sharp',
                  ]

    def create(self, validated_data):
        obj = Ticker.objects.create(**validated_data)
        obj.save()
        obj.update_data()
        return obj