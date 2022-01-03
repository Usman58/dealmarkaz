from django.urls import path
from .import views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('signup/', views.UserRegistrationView.as_view(), name="signup"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='Products/login.html',authentication_form=LoginForm),name="login"),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'),name="logout"),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='Products/changepassword.html',form_class=MyPasswordChangeForm,success_url='/products/password_change_done/'), name="password_change"),
    path('password_change_done/',auth_view.PasswordChangeDoneView.as_view(template_name='Products/passwordchangedone.html')),
    path('password_reset/',auth_view.PasswordResetView.as_view(template_name='Products/passwordreset.html',form_class=MyPasswordResetForm),name="password_reset"),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='Products/passwordresetdone.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='Products/passwordresetconfirm.html',form_class=MySetPasswordForm), name="password_reset_confirm"),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='Products/passwordresetcomplete.html'),name="password_reset_complete"),

    path('',views.Productlist,name="product_list"),
    path('category/<slug:c_slug>/', views.Productlist, name="product_list_category"),
    path('createproduct/', views.create_product, name='createproduct'),
    path('createbrand/', views.create_brand, name='create_brand'),
    path('detail/<int:pk>/',views.ProductDetail,name="product_detail"),
    path('updateproduct/<int:id>/', views.update_product, name='updateproduct'),
    path('delete/<int:id>/', views.delete_product, name='deleteproduct'),
    path('like/<int:pk>/',views.LikeView,name="like_ad"),


    path('user/profile/', views.user_profile, name='profile'),
    path('userdetail/<int:pk>/',views.user_detail, name='userdetail'),
    path('user/delete<int:pk>/',views.deleteUserProfile, name='deleteuserprofile'),

]
