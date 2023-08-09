from NEMO.urls import router
from django.urls import path

from NEMO_billing.prepayments import api
from NEMO_billing.prepayments.views import prepayments

# Rest API URLs
router.register(r"funds", api.FundViewSet)
router.register(r"fund_types", api.FundTypeViewSet)
router.register(r"project_prepayments", api.ProjectPrepaymentDetailViewSet)

urlpatterns = [
	path("usage_project_prepayments/", prepayments.usage_project_prepayments, name="usage_project_prepayments"),
	path("prepaid_project_status/", prepayments.prepaid_project_status, name="prepaid_project_status"),
]