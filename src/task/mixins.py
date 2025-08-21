class TitleMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class UserEntityMixin:
    def get_user_entity(self):
        return self.request.user.to_domain()

