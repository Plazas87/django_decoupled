"""Workspaces views module."""

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import DetailView, FormView, TemplateView

from ....application.commands import (
    CreateOrUpdateWorkspaceFromUploadExcelFileCommand,
    CreateWorkspaceAndAddDataFromFileCommand,
    TrainWorkspaceCommand,
    WorkspaceMetricsCommand,
)
from ....application.exceptions import (
    WorkspaceAlreadyExistsError,
    WorkspaceDoesNotExistsError,
)
from ....dependency_injection.containers import container
from ....dependency_injection.dispatcher import Dispatcher
from .forms import WorkspaceWithFileUploadForm
from .models import Workspace


@method_decorator(csrf_exempt, name="dispatch")
class FileUploadView(LoginRequiredMixin, View):
    """FileUploadView class."""

    login_url = "admin/login/"

    template = "workspaces/upload_file.html"

    def get(self, request):
        """UploadFile GET view handler."""
        return render(request, self.template)

    @method_decorator(csrf_protect)
    def post(self, request, dispatcher: Dispatcher = container.dispatcher):
        """UploadFile POST view handler."""
        create_workspace_command = CreateOrUpdateWorkspaceFromUploadExcelFileCommand(
            file_bytes=request.FILES["file"], owner=str(request.user.id)
        )

        dispatcher.dispatch(command=create_workspace_command)

        return HttpResponse("File successfuly uploaded.")


class WorkspaceListView(LoginRequiredMixin, TemplateView):
    """WorkspaceListView class."""

    template_name = "workspaces/list.html"


class WorkspaceCreateView(LoginRequiredMixin, FormView):
    """CreateWorkspaceView class."""

    form_class = WorkspaceWithFileUploadForm
    template_name = "workspaces/create.html"
    _created_workspace_id: str

    def post(self, request: HttpRequest) -> HttpResponse:
        """CreateWorkspace POST view handler."""
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(
        self, form: forms.Form, dispatcher: Dispatcher = container.dispatcher
    ) -> HttpResponse:
        """Form valid method."""
        owner = form.cleaned_data["owner"]

        workspace_name = form.cleaned_data["name"]
        file_bytes = form.cleaned_data["dataset"]

        try:
            create_and_add_files_to_workspace_command = (
                CreateWorkspaceAndAddDataFromFileCommand(
                    file_bytes=file_bytes,
                    owner_id=str(owner.id),
                    workspace_name=workspace_name,
                )
            )

            self._created_workspace_id: str = dispatcher.dispatch(
                command=create_and_add_files_to_workspace_command
            )

        except WorkspaceAlreadyExistsError:
            form.add_error(
                field="name",
                error=f"Ya existe un proyecto de nombre '{workspace_name}'.",
            )
            return self.form_invalid(form)

        except WorkspaceDoesNotExistsError:
            form.add_error(
                field="name",
                error=(
                    "No se pudo procesar el domumento. Por favor revise que el nombre "
                    "del proyecto coincida con el nombre de una de las hojas del domumento."
                ),
            )
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Get success url method."""
        return reverse_lazy(
            "workspaces:train", kwargs={"pk": self._created_workspace_id}
        )


class WorkspaceTrainView(LoginRequiredMixin, TemplateView):
    """WorkspaceTrainView class."""

    template_name = "workspaces/train.html"

    def post(
        self,
        request: HttpRequest,
        dispatcher: Dispatcher = container.dispatcher,
        *args,
        **kwargs,
    ) -> HttpResponse:
        """Train POST view handler."""
        train_workspace_command = TrainWorkspaceCommand(
            workspace_id=str(kwargs["pk"]), owner=str(request.user.id)
        )

        calculate_metrics_command = WorkspaceMetricsCommand(
            workspace_id=str(kwargs["pk"]), owner=str(request.user.id)
        )

        dispatcher.dispatch(command=train_workspace_command)
        dispatcher.dispatch(command=calculate_metrics_command)

        redirect_location = reverse_lazy(
            "workspaces:detail", kwargs={"pk": self.kwargs["pk"]}
        )

        # This is a hack to make the redirect work with HTMX
        # https://htmx.org/docs/#requests
        return HttpResponse(
            status=204,
            headers={"HX-Redirect": redirect_location},
        )


class WorkspaceDetailView(LoginRequiredMixin, DetailView):
    """WorkspaceDetailView class."""

    model = Workspace
    template_name = "workspaces/detail.html"

    # def get_context_data(self, **kwargs):
    #     """Get context data method."""
    #     # Placeholder for the metrics
    #     json_file_path = settings.BASE_DIR / "static/metrics.json"
    #     with open(json_file_path, encoding="utf-8") as json_file:
    #         report = json.load(json_file)

    #     context = super().get_context_data(**kwargs)
    #     context["metrics"] = report["metrics"]

    #     return context
