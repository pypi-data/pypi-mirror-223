from django.db.models import QuerySet
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from utils.custom_functions import find_all


class ContextMixin:
    """
    A default context mixin that passes the keyword arguments received by
    get_context_data() as the template context.
    """

    extra_context = None

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs


class SingleObjectMixin(ContextMixin):
    """
    Provide the ability to retrieve a single object for further manipulation.
    """

    model = None
    queryset = None
    slug_field = "slug"
    context_object_name = None
    slug_url_kwarg = "slug"
    pk_url_kwarg = "pk"
    query_pk_and_slug = False

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.

        This method is called by the default implementation of get_object() and
        may not be called if get_object() is overridden.
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
                )
        return self.queryset.all()


class MultipleObjectMixin(ContextMixin):
    """A mixin for views manipulating multiple objects."""

    queryset = None
    model = None
    form_filter = None
    context_object_name = None
    limit = -1
    offset = 0

    slug_field = "alias"
    slug_url_kwarg = "slug"
    pk_url_kwarg = "pk"
    query_pk_and_slug = False

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.slug_field
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            return None

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = find_all(self.model, {})
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )

        return queryset


class FormMixin(ContextMixin):
    """Provide a way to show and handle a form in a request."""

    initial = {}
    form_class = None
    success_url = None
    prefix = None

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy()

    def get_prefix(self):
        """Return the prefix to use for forms."""
        return self.prefix

    def get_form_class(self):
        """Return the form class to use."""
        return self.form_class

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {}

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs


class ModelFormMixin(FormMixin, SingleObjectMixin):
    """Provide a way to show and handle a ModelForm in a request."""

    fields = None

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, "object") and self.object is not None:
            kwargs.update({"instance": self.object})
        return kwargs


class BaseView(View):
    is_xml_http_request = False
    template_name = None
    model = None
    form = None

    def render_to_response(self, context, **response_kwargs):
        pass


class BaseCrudView(MultipleObjectMixin, ModelFormMixin, BaseView):
    """A base view for displaying a list of objects."""
    redirect_url = None
    serializer = None
    context = dict()
    result = None
    result_count = None

    def render_to_response(self, many=False, context=None, **response_kwargs):
        self.is_xml_http_request = self.request.headers.get(
            'X-Requested-With') == 'XMLHttpRequest'

        if self.is_xml_http_request:
            serializer = self.serializer(self.result, many=many)
            data = {
                'code': 1,
                'msg': 'success',
                'data': serializer.data
            }

            if many:
                data['total'] = self.result_count

            return JsonResponse(data)

        if context:
            self.context = context

        return render(self.request, self.template_name, self.context)

    def render_to_error(self, errors=None, **response_kwargs):
        self.is_xml_http_request = self.request.headers.get(
            'X-Requested-With') == 'XMLHttpRequest'

        if self.is_xml_http_request:
            return JsonResponse({
                'code': 0,
                'msg': str(errors),
                'data': None
            })

        messages.error(self.request, errors)

        return render(self.request, self.template_name, errors)

    def compute_query(self):
        request_params = self.request.GET.dict()
        limit = int(request_params.get('limit', self.limit))
        offset = int(request_params.get('offset', self.offset))

        queryset = self.get_queryset()
        filters = self.form_filter(self.request.GET, queryset=queryset)
        query_set = filters.qs if int(limit) < 0 else filters.qs[offset:offset + limit]

        self.result = query_set
        self.result_count = filters.qs.count()

        return {
            'qs': query_set,
            'count': filters.qs.count()
        }

    def get(self, request, *args, **kwargs):
        self.compute_query()
        return self.render_to_response(True)

    def post(self, request, id=None, *args, **kwargs):
        self.object = None
        instance = self.get_object()

        if instance:
            self.object = instance

        form = self.get_form()
        confirm = request.POST.get('confirm', False)
        self.result = None
        try:
            form.is_valid()
            if confirm:
                self.object.delete()
            else:
                self.result = form.save()
        except Exception as ex:
            return self.render_to_error(form.errors)

        return self.render_to_response()


class BaseEditView(ModelFormMixin, BaseView):
    """A base view for displaying a list of objects."""
    redirect_url = None
    serializer = None
    context = dict()
    result = None

    def render_to_response(self, context=None, **response_kwargs):
        self.is_xml_http_request = self.request.headers.get(
            'X-Requested-With') == 'XMLHttpRequest'

        if self.result:
            if self.is_xml_http_request:
                data = self.serializer(self.result).data
                return JsonResponse({
                    'code': 1,
                    'msg': 'success',
                    'data': data
                })
            return redirect(self.redirect_url)

        if context:
            self.context = context

        return render(self.request, self.template_name, self.context)

    def render_to_error(self, errors=None, **response_kwargs):
        self.is_xml_http_request = self.request.headers.get(
            'X-Requested-With') == 'XMLHttpRequest'

        if self.is_xml_http_request:
            return JsonResponse({
                'code': 0,
                'msg': str(errors),
                'data': None
            })

        return render(self.request, self.template_name, errors)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.result = None
        try:
            form.is_valid()
            self.result = form.save()
        except Exception as ex:
            self.render_to_error(ex)

        return self.render_to_response()


class BaseDeleteView(ModelFormMixin, BaseView):
    """A base view for displaying a list of objects."""
    redirect_url = None
    serializer = None
    context = dict()
    result = None

    def render_to_response(self, context=None, **response_kwargs):
        self.is_xml_http_request = self.request.headers.get(
            'X-Requested-With') == 'XMLHttpRequest'

        if self.is_xml_http_request:
            return JsonResponse({
                'code': 1,
                'msg': 'success',
                'data': None
            })
        return redirect(self.redirect_url)

    def render_to_error(self, errors=None, **response_kwargs):
        self.is_xml_http_request = self.request.headers.get(
            'X-Requested-With') == 'XMLHttpRequest'

        if self.is_xml_http_request:
            return JsonResponse({
                'code': 0,
                'msg': str(errors),
                'data': None
            })

        return render(self.request, self.template_name, errors)

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        self.object = self.get_object()
        form = self.get_form()

        try:
            form.is_valid()
            self.object.delete()
        except Exception as ex:
            self.render_to_error(ex)

        return self.render_to_response()


class BaseReportView(View):
    is_xml_http_request = False
    template_name = None
    redirect_url = None
    result = None
    context = {}

    def render_to_response(self, context=None, **response_kwargs):
        self.is_xml_http_request = self.request.headers.get(
            'X-Requested-With') == 'XMLHttpRequest'

        if self.result:
            if self.is_xml_http_request:
                # data = self.serializer(self.result).data
                return JsonResponse({
                    'code': 1,
                    'msg': 'success',
                    'data': self.result
                })
            return redirect(self.redirect_url)

        if context:
            self.context = context

        return render(self.request, self.template_name, self.context)
