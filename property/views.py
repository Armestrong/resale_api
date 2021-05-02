from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import RealEstate
from property import serializers

from core.models import Property


class RealEstateViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin
                        ):
    """Manage real estates in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = RealEstate.objects.all()
    serializer_class = serializers.RealEstateSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )

        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(property__isnull=False)

        return queryset.filter(user=self.request.user) \
            .order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class PropertyViewSet(viewsets.ModelViewSet):
    """Manage properties in database"""

    serializer_class = serializers.PropertySerializer
    queryset = Property.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the property for the authenticated user"""

        real_estates = self.request.query_params.get('real_estates')
        queryset = self.queryset
        if real_estates:
            real_estates_ids = self._params_to_ints(real_estates)
            queryset = queryset.filter(
                real_estates__id__in=real_estates_ids)

        return queryset.filter(user=self.request.user)
        # return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""

        if self.action == 'retrieve':
            return serializers.PropertyDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
