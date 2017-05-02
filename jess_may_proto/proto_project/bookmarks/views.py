# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *


def main_page(request):
    # template = get_template('main_page.html')
    # variables = Context({ 'user':request.user })
    # #     'head_titel':'장고 북마크',
    # #     'page_title':'장고북마크에 오신것을 환영합니다.',
    # #     'page_body':'북마크를 저장하고 공유하세요.',
    # # })
    # output = template.render(variables)
    # return HttpResponse(output)
    # return render_to_response(
    #     'main_page.html',
    #     { 'user' : request.user }
    # )
    return render_to_response(
        'main_page.html', RequestContext(request)
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')



def user_page(request, username):
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-id')

    variables = RequestContext(request, {
        'bookmarks':bookmarks,
        'username': username,
        'show_tags':True
    })

    return render_to_response('user_page.html', variables)

    # try:
    #     user = User.objects.get(username=username)
    # except:
    #     raise Http404('사용자를 찾을 수 없습니다')
    #
    # bookmarks = user.bookmark_set.all()
    # variables = RequestContext(request, {
    #     'username' : username,
    #     'bookmarks': bookmarks
    # })
    # return render_to_response('user_page.html', variables)

    # bookmarks = user.bookmark_set.all()
    # template = get_template('user_page.html')
    # variables = Context({
    #     'username':username,
    #     'bookmarks':bookmarks
    # })
    # output = template.render(variables)
    # return HttpResponse(output)

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'registration/register.html',
        variables
    )

@login_required
def bookmark_save_page(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():

            # URL이 있으면 가져오고 없으면 새로 저장합니다
            link, dummy = Link.objects.get_or_create(
                url=form.cleaned_data['url']
            )

            # 북마크가 있으면 가져오고 없으면 새로 저장합니다
            bookmark, created = Bookmark.objects.get_or_create(
                user=request.user,
                link=link
            )

            # 북마크 제목을 수정합니다
            bookmark.title = form.cleaned_data['title']

            # 북마크를 수정한 경우 이전에 입력된 태그들을 모두 지웁니다
            if not created:
                bookmark.tag_set.clear()

            # 태그 목록을 새로 만듭니다
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names :
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                bookmark.tag_set.add(tag)

            # 북마크를 저장합니다.
            bookmark.save()
            return HttpResponseRedirect(
                '/user/%s/' % request.user.username
            )
    else:
        form = BookmarkSaveForm()
    variables = RequestContext(request, {
        'form':form
    })
    return render_to_response('bookmark_save.html', variables)


# def main_page(request):
#     output = '''
#     <html>
#     <head><title>%s</title></head>
#     <body>
#     <h1>%s</h1><p>%s</p>
#     </body>
#     </html>
#     ''' % (
#         '장고|북마크',
#         '장고 북마크에 오신 것을 환영합니다',
#         '여기에 북마크를 저장하고 공유할 수 있습니다'
#     )
#     return HttpResponse(output)

def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmarks.order_by('-id')
    variables = RequestContext(request, {
        'bookmarks':bookmarks,
        'tag_name':tag_name,
        'show_tags':True,
        'show_user':True
    })
    return render_to_response('tag_page.html', variables)


# if __name__ == '__main__':


def tag_cloud_page(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')

    #calculate tag, min and max counts
    min_count = max_count = tags[0].bookmarks.count()
    for tag in tags:
        tag.count = tag.bookmarks.count()
        if tag.count < min_count:
            min_count = tag.count
        if __name__ == '__main__':
            if max_count < tag.count:
                max_count = tag.count

    #calculate count range. Avoid dividing by zero
    range  = float(max_count - min_count)
    if range == 0.0:
        range = 1.0

    #calculate tag weights
    for tag in tags:
        tag.weight = int(
            MAX_WEIGHT * (tag.count - min_count) / range
        )
    variables = RequestContext(request, {
        'tags':tags
    })
    return render_to_response('tag_cloud_page.html', variables)

def search_page(request):
    form = SearchForm()
    bookmarks = []
    show_results = False
    if ('query') in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query :
            form = SearchForm({'query':query})
            bookmarks = \
              Bookmark.objects.filter(title__icontains=query)[:10]
    variables = RequestContext(request, {
        'form':form,
        'bookmarks':bookmarks,
        'show_results':show_results,
        'show_tags':True,
        'show_user':True
    })
    #아래부분 ajax를 위한 부분임
    if request.is_ajax():
        return render_to_response('bookmark_list.html', variables)
    else:
        return render_to_response('search.html', variables)
    # return render_to_response('search.html', variables)