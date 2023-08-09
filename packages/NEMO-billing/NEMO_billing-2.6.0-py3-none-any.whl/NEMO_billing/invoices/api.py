from NEMO.serializers import ModelSerializer
from NEMO.utilities import export_format_datetime
from NEMO.views.api import ModelViewSet
from NEMO.views.api_billing import BillingFilterForm
from django.db.models import Q
from drf_excel.mixins import XLSXFileMixin
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import status
from rest_framework.fields import CharField, DateTimeField, DecimalField, IntegerField, empty
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from NEMO_billing.invoices.customization import BillingCustomization
from NEMO_billing.invoices.models import InvoiceConfiguration, InvoicePayment, ProjectBillingDetails
from NEMO_billing.invoices.processors import invoice_data_processor_class as data_processor
from NEMO_billing.invoices.views.usage import augment_with_invoice_items


class ProjectBillingDetailsSerializer(FlexFieldsSerializerMixin, ModelSerializer):
    class Meta:
        model = ProjectBillingDetails
        fields = "__all__"
        expandable_fields = {
            "project": "NEMO.serializers.ProjectSerializer",
            "category": "NEMO_billing.rates.api.RateCategorySerializer",
            "institution": "NEMO_billing.api.InstitutionSerializer",
            "department": "NEMO_billing.api.DepartmentSerializer",
        }


class ProjectBillingDetailsViewSet(ModelViewSet):
    filename = "project_billing_details"
    queryset = ProjectBillingDetails.objects.all()
    serializer_class = ProjectBillingDetailsSerializer
    filterset_fields = {
        "id": ["exact", "in"],
        "project_id": ["exact", "in"],
        "category_id": ["exact", "in"],
        "department_id": ["exact", "in"],
        "institution_id": ["exact", "in"],
    }


class InvoicePaymentSerializer(ModelSerializer):
    class Meta:
        model = InvoicePayment
        fields = "__all__"


class InvoicePaymentViewSet(ModelViewSet):
    filename = "invoice_payments"
    queryset = InvoicePayment.objects.all()
    serializer_class = InvoicePaymentSerializer
    filterset_fields = {
        "id": ["exact", "in"],
        "payment_received": ["exact", "gte", "gt", "lte", "lt"],
        "payment_processed": ["exact", "gte", "gt", "lte", "lt", "isnull"],
        "created_date": ["exact", "gte", "gt", "lte", "lt"],
        "updated_date": ["exact", "gte", "gt", "lte", "lt"],
        "invoice_id": ["exact", "in"],
    }


class BillingDataSerializer(Serializer):
    item_type = CharField(source="item_type.display_name", read_only=True)
    item_id = IntegerField(source="item.id", read_only=True)
    core_facility = CharField(max_length=200, read_only=True)
    name = CharField(max_length=200, read_only=True)
    account = CharField(source="project.account.name", read_only=True)
    account_id = IntegerField(source="project.account.id", read_only=True)
    project = CharField(source="project.name", read_only=True)
    project_id = IntegerField(source="project.id", read_only=True)
    reference_po = CharField(source="project.application_identifier", read_only=True)
    user = CharField(source="user.username", read_only=True)
    user_fullname = CharField(source="user.get_name", read_only=True)
    proxy_user = CharField(source="proxy_user.username", read_only=True)
    proxy_user_fullname = CharField(source="proxy_user.get_name", read_only=True)
    start = DateTimeField(read_only=True)
    end = DateTimeField(read_only=True)
    quantity = DecimalField(read_only=True, decimal_places=2, max_digits=8)
    rate = CharField(source="billable_rate", read_only=True)
    amount = DecimalField(source="invoiced_amount", read_only=True, decimal_places=2, max_digits=14)
    discount_amount = DecimalField(source="invoiced_discount", read_only=True, decimal_places=2, max_digits=14)
    pending_amount = DecimalField(source="amount", read_only=True, decimal_places=2, max_digits=14)
    merged_amount = DecimalField(label="amount", read_only=True, decimal_places=2, max_digits=14)

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        pending_vs_final = BillingCustomization.get_bool("billing_usage_show_pending_vs_final")
        if not pending_vs_final:
            self.fields["amount"] = self.fields["merged_amount"]
            del self.fields["pending_amount"]
        del self.fields["merged_amount"]

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        fields = "__all__"


class BillingDataViewSet(XLSXFileMixin, GenericViewSet):
    serializer_class = BillingDataSerializer

    def list(self, request, *args, **kwargs):
        billing_form = BillingFilterForm(self.request.GET)
        if not billing_form.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=billing_form.errors)
        try:
            queryset = self.get_queryset()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def check_permissions(self, request):
        if not request or not request.user.has_perm("NEMO.use_billing_api"):
            self.permission_denied(request)

    def get_queryset(self):
        billing_form = BillingFilterForm(self.request.GET)
        billing_form.full_clean()

        queryset = Q()
        start, end = billing_form.get_start_date(), billing_form.get_end_date()
        if billing_form.get_account_id():
            queryset = Q(project__account_id=billing_form.get_account_id())
        if billing_form.get_account_name():
            queryset = Q(project__account__name=billing_form.get_account_name())
        if billing_form.get_project_id():
            queryset = Q(project_id=billing_form.get_project_id())
        if billing_form.get_project_name():
            queryset = Q(project__name=billing_form.get_project_name())
        if billing_form.get_application_name():
            queryset = Q(project__application_identifier=billing_form.get_application_name())
        user_filter, customer_filter, trainee_filter = queryset, queryset, queryset
        if billing_form.get_username():
            user_filter = user_filter & Q(user__username=billing_form.get_username())
            customer_filter = customer_filter & Q(customer__username=billing_form.get_username())
            trainee_filter = trainee_filter & Q(trainee__username=billing_form.get_username())

        config = InvoiceConfiguration.first_or_default()
        billables = data_processor.get_billable_items(start, end, config, customer_filter, user_filter, trainee_filter)
        augment_with_invoice_items(billables)
        billables.sort(key=lambda x: x.start, reverse=True)
        return billables

    def get_filename(self, *args, **kwargs):
        return f"billing-{export_format_datetime()}.xlsx"
