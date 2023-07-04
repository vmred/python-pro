import json

from django.http import HttpRequest, JsonResponse
from django.views import View

from ..models.card import Card


class CardView(View):
    @staticmethod
    def get(request: HttpRequest):  # pylint: disable=unused-argument
        cards = Card.objects.all()  # pylint: disable=no-member
        return JsonResponse(
            [
                {
                    'id': str(card.id),
                    'pan': card.pan,
                    'expiry_date': card.expiry_date,
                    'cvv': card.cvv,
                    'issue_date': card.issue_date,
                    'owner_id': card.owner_id,
                    'status': card.status,
                }
                for card in cards
            ],
            safe=False,
        )

    @staticmethod
    def post(request: HttpRequest):
        request_body = json.loads(request.body)
        Card.validate_card_requests_fields(request_body)
        pan = request_body['pan']

        Card.validate_card_number(pan)

        card = Card(
            pan=pan,
            expiry_date=request_body.get('expiry_date'),
            issue_date=request_body.get('issue_date'),
            cvv=request_body['cvv'],
            owner_id=request_body['owner_id'],
            status=request_body['status'],
        )
        card.save()
        return JsonResponse({'id': str(card.id)})
