from django.db import models
from lean_canvas.models import LeanCanvas


class Solution(models.Model):
    lean_canvas = models.ForeignKey(LeanCanvas, on_delete=models.CASCADE)
    solution = models.TextField()

    def __str__(self) -> str:
        return self.solution
