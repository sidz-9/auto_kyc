from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework import status
from .models import user_details, pan_db
from .serializers import user_detailsSerializer
from .utils.ocr_demo_3 import ocr

from django.core.files.storage import FileSystemStorage

# Create your views here.
class user_details_list(APIView, UpdateModelMixin, DestroyModelMixin):

    # def get(self, request):
    #     user_details_1 = user_details.objects.all()
    #     serializer = user_detailsSerializer(user_details_1, many=True)
    #     return Response(serializer.data)

    def get(self, request, id=None):
        if id:
            # If an id is provided in the GET request, retrieve the user_details item by that id
            try:
                # Check if the user_details item the user wants to update exists
                queryset = user_details.objects.get(id=id)
            except user_details.DoesNotExist:
                # If the user_details item does not exist, return an error response
                return Response({'errors': 'This user_details item does not exist.'}, status=400)

            # Serialize user_details item from Django queryset object to JSON formatted data
            read_serializer = user_detailsSerializer(queryset)

        else:
            # Get all user_details items from the database using Django's model ORM
            queryset = user_details.objects.all()

            # Serialize list of user_details item from Django queryset object to JSON formatted data
            read_serializer = user_detailsSerializer(queryset, many=True)

        # Return a HTTP response object with the list of user_details items as JSON
        return Response(read_serializer.data)

    def post(self, request):
        # Pass JSON data from user POST request to serializer for validation
        create_serializer = user_detailsSerializer(data=request.data)

        # Check if user POST data passes validation checks from serializer
        if create_serializer.is_valid():
            # If user data is valid, create a new user_details item record in the database
            user_details_object = create_serializer.save()

            # Serialize the new user_details item from a Python object to JSON format
            read_serializer = user_detailsSerializer(user_details_object)

            # Return a HTTP response with the newly created user_details item data
            return Response(read_serializer.data, status=201)

        # If the users POST data is not valid, return a 400 response with an error message
        return Response(create_serializer.errors, status=400)

    def put(self, request, id=None):
        try:
            # Check if the user_details item the user wants to update exists
            user_details_item = user_details.objects.get(id=id)
        except user_details.DoesNotExist:
            # If the user_details item does not exist, return an error response
            return Response({'errors': 'This user_details item does not exist.'}, status=400)

        # If the user_details item does exists, use the serializer to validate the updated data
        update_serializer = user_detailsSerializer(user_details_item, data=request.data)

        # If the data to update the user_details item is valid, proceed to saving data to the database
        if update_serializer.is_valid():
            # Data was valid, update the user_details item in the database
            user_details_object = update_serializer.save()

            # Serialize the user_details item from Python object to JSON format
            read_serializer = user_detailsSerializer(user_details_object)

            # Return a HTTP response with the newly updated user_details item
            return Response(read_serializer.data, status=200)

        # If the update data is not valid, return an error response
        return Response(update_serializer.errors, status=400)

    def delete(self, request, id=None):
        try:
            # Check if the user_details item the user wants to update exists
            user_details_item = user_details.objects.get(id=id)
        except user_details.DoesNotExist:
            # If the user_details item does not exist, return an error response
            return Response({'errors': 'This user_details item does not exist.'}, status=400)

        # Delete the chosen user_details item from the database
        user_details_item.delete()

        # Return a HTTP response notifying that the user_details item was successfully deleted
        return Response(status=204)


class auto_kyc_view(APIView, UpdateModelMixin, DestroyModelMixin):
    def post(self, request):

        uploaded_file = request.FILES['file']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        print(name + "heyy")

        # print(ocr(name))
        user_data = ocr(name)
        print("printing user_data")
        print(user_data)

        pan_objs = pan_db.objects.get(pan_number=user_data['PAN'])
        print(pan_objs.name, pan_objs.pan_number, pan_objs.dob)

        if (user_data['Date of Birth'] == pan_objs.dob and user_data['Name'] == pan_objs.name and user_data[
            'PAN'] == pan_objs.pan_number):
            # update kyc status of user to success and send a success email to user
            return Response(r"Success", status=status.HTTP_200_OK)
        else:
            # update kyc status of user to unsuccessful and send an unsuccessful email to user
            return Response(r"Unsuccessful", status=status.HTTP_200_OK)

        # return Response(r"Success", status=HTTP_200_OK)

    def get(self, request):
        return Response(r"Hi")

    # def compare_user_info(user_data, pan_objs):
    #     if(user_data['Date of Birth'] == pan_objs.dob & user_data['NAME'] == pan_objs.name & user_data['PAN'] == pan_objs.pan_number):
    #         return True
    #     else:
    #         return False
    #     pass