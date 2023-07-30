from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *


# Create your views here.


def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        auth_user = auth.authenticate(username=username, password=password)

        if auth_user is not None:
            auth.login(request, auth_user)
            return redirect('frontpage')
        
        else:
            messages.error(request, "No identity matched, retry")
            return redirect('index')
    else:
        return render(request, "index.html")



def logout(request):
    auth.logout(request)
    return redirect('index')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if len(username) <= 0:
                messages.error(request, "Enter username!")
                return redirect('register')
            elif len(email) <= 0:
                messages.error(request, "Enter email!")
                return redirect('register')
            elif len(password) < 8:
                messages.error(request, "Password is weak, enter strong password!")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username taken!")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email taken!")
                return redirect('register')
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()

                user_obi = User.objects.get(username=username)

                new_profile = Profile.objects.create(user=user_obi)
                new_profile.save()
                return redirect('frontpage')
            


        else:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
    else:
        return render(request, "register.html")



# def frontpage(request):
#     user_obj = User.objects.get(username=request.user)
#     get_profile = Profile.objects.get(user=user_obj)
    

#     post = Posts.objects.all()
#     post_get = Posts.objects.get(post)

#     comment = Comment.objects.filter(post=post_get.post_id)[0:2]
#     context ={
#         "profile": get_profile,
#         "comments": comment,
#     }

#     return render(request, "frontpage.html", context)
    

def frontpage(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)

    posts = Posts.objects.all()
    context ={
        "profile": get_profile,
        "post": posts,
        # "post_comments": post_comments,
        # "likes": likes,
    }

    return render(request, "frontpage.html", context)




def profile(request, user):
    user_obj = User.objects.get(username=user)
    profile =  Profile.objects.get(user=user_obj)
    post = Posts.objects.filter(profile=profile)
    likes = Like_post.objects.filter(user=profile)
    user_obj = Profile.objects.get(user=request.user)

    follower = user_obj
    following = profile

    if Follow.objects.filter(user=follower, following=following):
        switch = "Following"
    else:
        switch = "Follow"

    profile_visited_followers = len(Follow.objects.filter(user=profile))
    profile_visited_following = len(Follow.objects.filter(following=profile))


    context ={
        "profile": profile,
        "post": post,
        "switch": switch,
        "profile_visited_followers": profile_visited_followers,
        "profile_visited_following": profile_visited_following,
        # "post_comments": post_comments,
        # "likes": likes,  # Add the list of post_ids to the context
    }

    return render(request, "profile.html", context)



def follow(request):

    if request.method == "POST":
        current_user = request.POST['follower']
        followed_user = request.POST['following']
        follower = User.objects.get(username=current_user)
        following = User.objects.get(username=followed_user)

        user_obj = Profile.objects.get(user=follower)

        u = Profile.objects.get(user=following)


        if Follow.objects.filter(user=user_obj, following=u).first():
            del_follower = Follow.objects.get(user=user_obj, following=u)
            del_follower.delete()
            return redirect(profile, followed_user)
        else:
            new_follower = Follow.objects.create(user=user_obj, following=u)
            new_follower.save()
            return redirect(profile, followed_user)




def likethis(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("like_id")

    posts = Posts.objects.get(post_id=post_id)

    post_like = Like_post.objects.filter(post_id=post_id, user=get_profile).first()

    if post_like == None:
        new_like = Like_post.objects.create(post_id=post_id, user=get_profile)
        new_like.save()
        posts.likes +=1
        posts.save()
        return redirect('frontpage')
    
    else:
        post_like.delete()
        posts.likes -=1
        posts.save()
        return redirect('frontpage')


def likethiss(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    posts = Posts.objects.get(post_id=post_id)

    post_like = Like_post.objects.filter(post_id=post_id, user=get_profile).first()

    if post_like == None:
        new_like = Like_post.objects.create(post_id=post_id, user=get_profile)
        new_like.save()
        posts.likes +=1
        posts.save()
        return redirect(pana_details, post_id)
    
    else:
        post_like.delete()
        posts.likes -=1
        posts.save()
        return redirect(pana_details, post_id)
    

def likethissinprofile(request, user):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post_id = request.GET.get("post_id")

    u = User.objects.get(username=user)
    visit_profile = Profile.objects.get(user=u)

    posts = Posts.objects.get(post_id=post_id)

    post_like = Like_post.objects.filter(post_id=post_id, user=get_profile).first()

    if post_like == None:
        new_like = Like_post.objects.create(post_id=post_id, user=get_profile)
        new_like.save()
        posts.likes +=1
        posts.save()
        return redirect(profile, visit_profile)
    
    else:
        post_like.delete()
        posts.likes -=1
        posts.save()
        return redirect(profile, visit_profile)


def pana(request):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)

    if request.method == "POST":
        user = get_profile
        caption = request.POST['caption']
        # tag = request.POST['tag']
        upload = request.FILES['upload']

        new_post = Posts.objects.create(profile=user, image=upload, caption=caption)
        new_post.save()
        return redirect('frontpage')

    context ={
        "profile": get_profile,
    }

    return render(request, "pana.html", context)


def pana_details(request, post_id):
    user_obj = User.objects.get(username=request.user)
    get_profile = Profile.objects.get(user=user_obj)
    post = Posts.objects.get(post_id=post_id)
    return render(request, "details.html", {'posts':post, "profile":get_profile})




def setting(request):
    user_obj = User.objects.get(username=request.user)
    profile =  Profile.objects.get(user=user_obj)

    if request.method == 'POST':
        if request.FILES.get('backimg') == None:
            back_img = profile.back_img
            name = request.POST['display_name']
            bio = request.POST['bio']
            web = request.POST['web']
            
            profile.back_img=back_img
            profile.display_name=name
            profile.bio=bio
            profile.web=web
            

        if request.FILES.get('backimg') != None:
            back_img = request.FILES.get('backimg')
            name = request.POST['display_name']
            bio = request.POST['bio']
            web = request.POST['web']

            profile.back_img=back_img
            profile.display_name=name
            profile.bio=bio
            profile.web=web


        if request.FILES.get('profileim') == None:
            profile_img = profile.profile_img
            name = request.POST['display_name']
            web = request.POST['web']
            bio = request.POST['bio']

            profile.profile_img = profile_img
            profile.display_name = name
            profile.web = web
            profile.bio = bio
            profile.save()
            return redirect('setting')
        

        if request.FILES.get('profileim') != None:
            profile_img = request.FILES.get('profileim')
            name = request.POST['display_name']
            web = request.POST['web']
            bio = request.POST['bio']

            profile.profile_img = profile_img
            profile.display_name = name
            profile.web = web
            profile.bio = bio
            profile.save()
            return redirect('setting')
    else:
        return render(request, "settings.html", {'profile': profile})
    