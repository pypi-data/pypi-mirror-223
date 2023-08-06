from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from lean_canvas.models import LeanCanvas

base = "lean_canvas/"


class LeanCanvasListView(ListView):
    model = LeanCanvas
    template_name = base + "lean_canvas_list.html"
    context_object_name = "canvases"


class LeanCanvasDetailView(DetailView):
    model = LeanCanvas
    template_name = base + "lean_canvas_detail.html"
    context_object_name = "canvas"


class LeanCanvasCreateView(CreateView):
    model = LeanCanvas
    template_name = base + "lean_canvas_new.html"
    fields = ("title",)


class LeanCanvasUpdateView(UpdateView):
    model = LeanCanvas
    template_name = base + "lean_canvas_edit.html"
    fields = ("title",)


class LeanCanvasDeleteView(DeleteView):
    model = LeanCanvas
    template_name = base + "lean_canvas_delete.html"
    context_object_name = "canvas"
    success_url = reverse_lazy("canvas_list")  # adjust to your URL pattern
