from django.shortcuts import render
from .serializers import CategorySerializer, CourseSerializer, CourseDetailSerializer
from .models import Course, Category
from rest_framework import generics, permissions
from rest_framework.authentication import BasicAuthentication
from drf_multiple_model.views import MultipleModelAPIView
import datetime
from venues.models import CourseVenue
from venues.serializers import CitySerializer, CourseVenueSerializer



class PreparedCourseListAPIView(generics.ListAPIView):
    authentication_classes = [BasicAuthentication, ]
    permissions_classes = [permissions.IsAuthenticated, ]
    queryset = Course.objects.filter(publish = True, open_registration = False).order_by('updated_date')
    serializer_class = CourseSerializer


class OpenCourseListAPIView(generics.ListAPIView):
    authentication_classes = [BasicAuthentication, ]
    permissions_classes = [permissions.IsAuthenticated, ]
    queryset = Course.objects.filter(publish = True, open_registration = True).order_by('updated_date')
    serializer_class = CourseSerializer

class CourseRetrieveAPIView(generics.RetrieveAPIView):
	authentication_classes = [BasicAuthentication, ]
	permissions_classes = [permissions.IsAuthenticated, ]
	queryset = Course.objects.filter(publish = True)
	serializer_class = CourseDetailSerializer

class CategoryListAPIView(MultipleModelAPIView):
    authentication_classes = [BasicAuthentication, ]
    permissions_classes = [permissions.IsAuthenticated, ]

    def get_queryList(self):
        timestamp = float(self.kwargs['timestamp'])
        date_value = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S%Z')

        queryList = (
            (Category.objects.filter(updated_date__gte = date_value).order_by('updated_date').distinct(), CategorySerializer),
            (Course.objects.filter(updated_date__gte = date_value).order_by('updated_date').distinct(), CourseDetailSerializer),
            (CourseVenue.objects.filter(updated_date__gte = date_value).order_by('updated_date').distinct(), CourseVenueSerializer),
            (CourseVenue.objects.filter(updated_date__gte = date_value).order_by('updated_date').distinct(), CitySerializer)
        )

        return queryList
