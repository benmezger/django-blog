from django.views import generic
from django.conf import settings

from blog.models import Post, NavBarLink


class BaseBlogPage:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["navlinks"] = NavBarLink.objects.filter(enabled=True)
        return context


class PostList(BaseBlogPage, generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created")
    template_name = "blog/index.html"


class PostDetail(BaseBlogPage, generic.DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object = self.get_object()
        author = settings.AUTHOR_INFO.get("name")

        context["description"] = f"{object.title} | {author}"

        return context


class PageDetail(BaseBlogPage, generic.DetailView):
    model = NavBarLink
    context_object_name = "page"
    template_name = "blog/post.html"
    queryset = NavBarLink.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object = self.get_object()
        author = settings.AUTHOR_INFO.get("name")

        context["description"] = f"{object.title} | {author}"

        return context
