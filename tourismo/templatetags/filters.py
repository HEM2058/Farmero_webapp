from django import template
from ..models import GuideRequest

register = template.Library()

@register.filter
def has_guide_request(plan, guide):
    guide_request = GuideRequest.objects.filter(plan=plan, guide=guide, accepted=True).first()
    if guide_request:
        return True
    else:
        return False
    
@register.filter
def get_guide_request_quantity(plan, guide):
    guide_request = GuideRequest.objects.filter(plan=plan, guide=guide).first()
    return guide_request.quantity_order if guide_request else None

