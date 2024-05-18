from django.urls import path

from django.contrib.auth import views as auth_views

from blog import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.post_list, name="post_list"),
    path('posts/<str:category>', views.post_list, name="post_list_category"),
    # path('posts/', views.PostListView.as_view(), name= "post_list"),
    # path('posts/<int:id>', views.post_detail, name="post_detail"),
    path('posts/detail/<pk>', views.post_detail, name="post_detail"),
    path('posts/<post_id>/comment', views.post_comment, name="post_comment"),
    path('ticket/', views.ticket, name="ticket"),
    path('postsearch/',views.post_search_view, name="post_search" ),
    path('profile/', views.profile, name="profile"),
    path('createpost/', views.create_post, name="create_post"),
    path('post_delete/<pk>', views.post_delete, name="post_delete"),
    path('post_update/<pk>', views.post_update, name="post_update"),
    path('image_delete/<image_id>', views.image_delete, name="image_delete"),
    # path('login', views.user_login, name="login"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='done'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/blog/password_reset/complete'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.user_register_view, name='register'),
    path('account/edit', views.account_edit, name='account_edit'),
    path('account/view/<int:u>/', views.account_view, name='account_view'),




]
