import json

from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from ..models.card import Card


class CardView(View):
    @staticmethod
    def get(request: HttpRequest):  # pylint: disable=unused-argument
        cards = Card.objects.all()  # pylint: disable=no-member
        context = [
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
        ]
        if request.headers.get('accept') == 'application/json':
            return JsonResponse(context, safe=False)

        return render(request, 'cards/cards_view_form.html', {'cards': context}, 'text/html')

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
            owner_id=int(request_body['owner_id']),
            status=request_body['status'],
        )
        card.save()
        return JsonResponse({'id': str(card.id)})


def cards_create_form(request):
    if request.method == 'GET':
        # pylint: disable=no-member
        return render(request, 'cards/cards_create_form.html', {'cards': Card.objects.all()})

    if request.method == 'POST':
        # pylint: disable=no-member
        Card.objects.create(
            pan=request.POST['pan'],
            expiry_date=request.POST['expiry_date'],
            issue_date=request.POST['issue_date'],
            cvv=request.POST['cvv'],
            owner_id=int(request.POST['owner_id']),
            status=request.POST['status'],
        )
        return HttpResponseRedirect(reverse('cards'))

    return render(request, 'cards/invalid_request.html')
