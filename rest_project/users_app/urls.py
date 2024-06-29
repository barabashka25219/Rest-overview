from django.urls import path
from .views import BasketViewList, BasketDetail, FeedBackViewList, FeedbackViewRetriveUpdateDestroy

app_name = 'users'

urlpatterns = [
    path('basket/', BasketViewList.as_view(), name='basket-list'),
    path('basket/<int:pk>/', BasketDetail.as_view(), name='basket-detail'),
    path('feedbacks/', FeedBackViewList.as_view(), name='feedback-list'),
    path('feedbacks/<int:pk>/', FeedbackViewRetriveUpdateDestroy.as_view(), name='feedback-detail'),
]