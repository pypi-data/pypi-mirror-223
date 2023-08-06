from django.contrib import admin
from lean_canvas.models import (
    Channel,
    CostStructure,
    CustomerSegment,
    KeyMetric,
    LeanCanvas,
    Problem,
    RevenueStream,
    Solution,
    UnfairAdvantage,
    UniqueValueProposition,
)


# Register your models here.
admin.site.register(LeanCanvas)
admin.site.register(CostStructure)
admin.site.register(CustomerSegment)
admin.site.register(KeyMetric)
admin.site.register(Channel)
admin.site.register(Problem)
admin.site.register(RevenueStream)
admin.site.register(UnfairAdvantage)
admin.site.register(UniqueValueProposition)
