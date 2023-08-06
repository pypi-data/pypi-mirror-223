from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.response import Response
from django.conf import settings
from djangoldp.views import LDPAPIView, NoCSRFAuthentication
import requests


class BabelfishServiceCreate(LDPAPIView):
    authentication_classes = (NoCSRFAuthentication,)

    def post(self, request):
        # Retrieve the user-specific access token
        token_url = getattr(settings, 'BABELFISH_BASE_URL', "https://babelfish.data-container.net") + '/oauth/token'
        data = {
            'client_id': request.user.babelfish_profile.client_id,
            'client_secret': request.user.babelfish_profile.client_secret,
            'grant_type': 'client_credentials',
            'scope': 'write'
        }
        response = requests.post(token_url, data=data)
        access_token = response.json().get('access_token')

        print(access_token)
        print(access_token)
        print(access_token)
        print(request.user)
        print(request)
        print(request.POST)
        # Call the service registration endpoint with the proper info
        service_registration_url = getattr(settings, 'BABELFISH_BASE_URL', "https://babelfish.data-container.net") + '/service/'  # Replace with the actual registration endpoint URL
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        print(request.data.get('title'))

        json = {
            "interface": {
                "info": { "title": request.data.get('title') },
                "servers": [{"url": request.data.get('url')}],
                "party": request.data.get('party'),
                "paths": {
                    "/api/validate": {
                        "post": {
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {} 
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "data": {
                "description": request.data.get('description')
            },
            "governance": {
                "dpv:hasProcessing": ["dpv:Use"],
                "dpv:hasPurpose": "dpv:Purpose",
                "dpv:hasExpiryTime": "6 months"
            }
        }

        try:
            response = requests.post(service_registration_url, headers=headers, json=json)
            response = response.json()
        except Exception as e:
            print(e)
            print(e)
            print(e)
            print(e)
            print(e)
            print("HEHEHEHEHEEHHEHEEH")
            return Response({'message': 'Service registration failed'}, status=500)

        print(json)
        response = requests.post(registration_url, headers=headers, json=json)
        # Refresh the list of services to display the new one
        print(response)
        if response.status_code != 201:
            return Response({'message': 'Service registration failed'}, status=500)

        return Response({'message': 'Service properly registered'})