from rest_framework.response import Response
from rest_framework.views import status
from .models import PURCHASE_STATE_CHOICES

def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        if 'status' not in args[0].request.data:
            return Response(
                data={
                    "message": "An status is required to update a purchase."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        status_ = args[0].request.data['status']
        possibleStatus = set()
        for e in PURCHASE_STATE_CHOICES:
            possibleStatus.add(e[0])
        possibleStatus = list(possibleStatus)
        if int(status_) not in possibleStatus:
            return Response(
                data={
                    "message": "Invalid status."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
