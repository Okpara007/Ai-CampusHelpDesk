# from allauth.socialaccount.models import SocialAccount

# Assuming 'request.user' is the authenticated user
# social_accounts = SocialAccount.objects.filter(user=request.user, provider='google')

# if social_accounts.exists():
#     google_account = social_accounts.first()

#     # Access Google account data, including profile picture
#     google_email = google_account.extra_data.get('email')
#     google_name = google_account.extra_data.get('name')
#     google_picture = google_account.extra_data.get('picture')  # or 'avatar_url'

#     # Use retrieved data as needed
#     # For example, print the email, name, and profile picture URL
#     print(f"Google Email: {google_email}")
#     print(f"Google Name: {google_name}")
#     print(f"Profile Picture URL: {google_picture}")

#     profile_picture_url = None
#     if social_accounts.exists():
#         google_account = social_accounts.first()
#         profile_picture_url = google_account.extra_data.get('picture')


# def SocialProfile(request):
#     social_accounts = SocialAccount.objects.filter(user=request.user, provider='google')
#     if social_accounts.exists():
#         google_pics = social_accounts[0].extra_data['picture']
#         google_email = social_accounts[0].extra_data['email']
#         google_name = social_accounts[0].extra_data['name']
    
#     return {"google_pics":google_pics, "google_email":google_email, "google_name":google_name}


