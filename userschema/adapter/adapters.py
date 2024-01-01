# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# # from allauth.account.adapter import DefaultAccountAdapter
# from django.urls import reverse
# from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
# from userschema.models import CustomUser



# # class MyAccountAdapter(DefaultAccountAdapter):

# #     def get_login_redirect_url(self, request):
# #         print('I am entering get_login_redirect_url')
# #         if 'team_membership_project_id' in request.session:
# #             parameters = {}
# #             parameters['invitation_id'] = request.session['invitation_id']
# #             path = reverse('action:accept_invitation', urlconf=None, args=None, kwargs=parameters)
# #             return path

# #         path = '/'

# #         return path

# #     def is_open_for_signup(self, request):
# #         """
# #         Checks whether or not the site is open for signups.Next to simply returning True/False you can also intervene the
# #         regular flow by raising an ImmediateHttpResponse. (Comment reproduced from the overridden method.)
# #         """
# #         return True






# class CustomAdapter(DefaultSocialAccountAdapter):
#     def is_safe_url(self, url):
#         return is_safe_url(url, allowed_hosts=None) 

#     def new_user(self, request, sociallogin):
#         # Create a new user if one doesn't exist based on the social account details
#         user = CustomUser(email=sociallogin.user.email)  # Adjust as per your CustomUser model fields
#         # Set any additional attributes from the social account if needed
#         user.save()
#         return user

#     # def pre_social_login(self, request, sociallogin):
#     #     user = CustomUser.objects.filter(email = sociallogin.user.email).first()
#     #     if user and not sociallogin.is_existing:
#     #         # sociallogin.connect(request, user)
#     #         try:
#     #             google_account = sociallogin.account
#     #             if google_account.provider == 'google':
#     #                 return reverse('google_verification')
#     #         except:
#     #             pass
    
#     def is_open_for_signup(self, request):
#         """
#         Checks whether or not the site is open for signups.Next to simply returning True/False you can also intervene the
#         regular flow by raising an ImmediateHttpResponse. (Comment reproduced from the overridden method.)
#         """
#         return True

#     def get_connect_redirect_url(self, request, socialaccount):
#         url = reverse('google_verification')
#         return url


