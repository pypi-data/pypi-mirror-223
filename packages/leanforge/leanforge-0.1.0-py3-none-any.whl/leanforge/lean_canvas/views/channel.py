from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from lean_canvas.models import Channel, LeanCanvas
from lean_canvas.forms import ChannelForm


class ChannelListView(View):
    def get(self, request, lean_canvas_id):
        lean_canvas = get_object_or_404(LeanCanvas, id=lean_canvas_id)
        channels = Channel.objects.filter(lean_canvas=lean_canvas)
        return render(
            request,
            "partials/channel_list.html",
            {"channels": channels, "lean_canvas_id": lean_canvas_id},
        )


class ChannelDetailView(View):
    def get(self, request, id):
        channel = get_object_or_404(Channel, id=id)
        return render(request, "partials/channel_detail.html", {"channel": channel})


class ChannelCreateView(View):
    def get(self, request, lean_canvas_id):
        print(f"DEBUG: lean_canvas_id in get = {lean_canvas_id}")  # add this line
        form = ChannelForm()
        return render(
            request,
            "partials/channel_form.html",
            {"form": form, "lean_canvas_id": lean_canvas_id},
        )

    def post(self, request, lean_canvas_id):
        print(f"DEBUG: lean_canvas_id in post = {lean_canvas_id}")  # add this line
        lean_canvas = get_object_or_404(LeanCanvas, id=lean_canvas_id)
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.lean_canvas = lean_canvas
            channel.save()
            return redirect("channel_list", lean_canvas_id=lean_canvas.id)
        return render(
            request,
            "partials/channel_form.html",
            {"form": form, "lean_canvas_id": lean_canvas_id},
        )


class ChannelUpdateView(View):
    def get(self, request, id):
        channel = get_object_or_404(Channel, id=id)
        form = ChannelForm(instance=channel)
        return render(
            request, "partials/channel_form.html", {"form": form, "channel": channel}
        )

    def post(self, request, id):
        channel = get_object_or_404(Channel, id=id)
        form = ChannelForm(request.POST, instance=channel)
        if form.is_valid():
            form.save()
            return redirect("channel_detail", id=channel.id)
        return render(
            request, "partials/channel_form.html", {"form": form, "channel": channel}
        )


class ChannelDeleteView(View):
    def get(self, request, id):
        channel = get_object_or_404(Channel, id=id)
        return render(
            request, "partials/channel_confirm_delete.html", {"channel": channel}
        )

    def post(self, request, id):
        channel = get_object_or_404(Channel, id=id)
        channel.delete()
        return redirect("partials/channel_list", lean_canvas_id=channel.lean_canvas.id)
