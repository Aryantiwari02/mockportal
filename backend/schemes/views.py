from django.http import JsonResponse
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Scheme
from .serializers import SchemeSerializer


def api_status(request):
    return JsonResponse({
        "status": "success",
        "message": "Government Yojana Portal API is running",
        "project": "Government Yojana Portal"
    })


@api_view(["GET"])
def scheme_list(request):
    schemes = Scheme.objects.all()

    # Search
    search_query = request.GET.get("q", "").strip()

    if search_query:
        schemes = schemes.filter(
            Q(title__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__icontains=search_query)
        )

    # Category filter
    category = request.GET.get("category", "").strip()

    if category and category.lower() != "all":
        schemes = schemes.filter(
            category__iexact=category
        )

    schemes = schemes.order_by("category", "title")

    serializer = SchemeSerializer(schemes, many=True)

    return Response({
        "count": schemes.count(),
        "results": serializer.data
    })


@api_view(["GET"])
def scheme_detail(request, scheme_id):
    try:
        scheme = Scheme.objects.get(id=scheme_id)
    except Scheme.DoesNotExist:
        return Response(
            {"error": "Scheme not found"},
            status=404
        )

    serializer = SchemeSerializer(scheme)

    return Response(serializer.data)