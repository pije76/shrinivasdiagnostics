import datetime

from shop.models import *


# For _footer_bottom.html template file
def current_year_context_processor(request):
    current_datetime = datetime.datetime.now()
    return {
        'current_year': current_datetime.year
    }


# For _footer.html template file
def posts_context_processor(request):
    posts = Post.objects.order_by('-updated')  # By updated date.

    return {
        'posts': posts
    }
