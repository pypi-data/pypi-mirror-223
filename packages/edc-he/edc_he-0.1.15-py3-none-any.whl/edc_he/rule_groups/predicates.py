from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import NO
from edc_metadata.metadata_rules import PredicateCollection


class Predicates(PredicateCollection):
    app_label = "edc_he"
    visit_model = "edc_visit_tracking.subjectvisit"

    assets_model = "edc_he.healtheconomicsassets"
    household_head_model = "edc_he.healtheconomicshouseholdhead"
    income_model = "edc_he.healtheconomicsincome"
    patient_model = "edc_he.healtheconomicspatient"
    property_model = "edc_he.healtheconomicsproperty"

    @property
    def hoh_model_cls(self):
        return django_apps.get_model(self.household_head_model)

    @property
    def patient_model_cls(self):
        return django_apps.get_model(self.patient_model)

    @property
    def assets_model_cls(self):
        return django_apps.get_model(self.assets_model)

    @property
    def property_model_cls(self):
        return django_apps.get_model(self.property_model)

    @property
    def income_model_cls(self):
        return django_apps.get_model(self.income_model)

    def get_hoh(self, visit):
        try:
            obj = self.hoh_model_cls.objects.get(
                subject_visit__subject_identifier=visit.subject_identifier
            )
        except ObjectDoesNotExist:
            obj = None
        return obj

    def household_head_required(self, visit, **kwargs):
        return not self.hoh_model_cls.objects.filter(
            subject_visit__subject_identifier=visit.subject_identifier
        ).exists()

    def patient_required(self, visit, **kwargs):
        required = False
        if hoh_obj := self.get_hoh(visit):
            if not self.patient_model_cls.objects.filter(
                subject_visit__subject_identifier=visit.subject_identifier
            ).exists():
                required = hoh_obj.hoh == NO
        return required

    def assets_required(self, visit, **kwargs):
        return not self.assets_model_cls.objects.filter(
            subject_visit__subject_identifier=visit.subject_identifier
        ).exists()

    def property_required(self, visit, **kwargs):
        return not self.property_model_cls.objects.filter(
            subject_visit__subject_identifier=visit.subject_identifier
        ).exists()

    def income_required(self, visit, **kwargs):
        return not self.income_model_cls.objects.filter(
            subject_visit__subject_identifier=visit.subject_identifier
        ).exists()
