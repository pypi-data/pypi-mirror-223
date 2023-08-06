from __future__ import annotations

from django import forms
from django.test import TestCase
from edc_constants.constants import COMPLETE, FEMALE, NO, NOT_APPLICABLE, OTHER, YES
from edc_utils import get_utcnow
from edc_utils.test_case_mixins.longitudinal_test_case_mixin import (
    LongitudinalTestCaseMixin,
)

from edc_he.constants import WIFE_HUSBAND
from edc_he.form_validators import HealthEconomicsHouseholdHeadFormValidator
from edc_he.models import (
    Education,
    EmploymentType,
    Ethnicities,
    HealthEconomicsHouseholdHead,
    InsuranceTypes,
    Religions,
)

from ..visit_schedule import visit_schedule


def get_m2m_qs(model_cls):
    name = model_cls.objects.all()[0].name
    return model_cls.objects.filter(name=name).exclude(name=NOT_APPLICABLE)


class HealthEconomicsHouseholdHeadTests(LongitudinalTestCaseMixin, TestCase):
    visit_schedule = visit_schedule

    def setUp(self) -> None:
        self.subject_identifier = self.enroll()
        self.create_visits(self.subject_identifier)

    def get_cleaned_data(self, **kwargs) -> dict:
        cleaned_data = dict(
            subject_visit=self.subject_visit_baseline,
            report_datetime=get_utcnow(),
            hh_count=5,
            hh_minors_count=1,
            hoh=YES,
            relationship_to_hoh=NOT_APPLICABLE,
            relationship_to_hoh_other=None,
            hoh_gender=FEMALE,
            hoh_age=25,
            hoh_religion=get_m2m_qs(Religions),
            hoh_religion_other=None,
            hoh_ethnicity=get_m2m_qs(Ethnicities),
            hoh_ethnicity_other=None,
            hoh_education=get_m2m_qs(Education),
            hoh_education_other=None,
            hoh_employment_status="",
            hoh_employment_type=get_m2m_qs(EmploymentType),
            hoh_employment_type_other=None,
            hoh_marital_status=OTHER,
            hoh_marital_status_other="blah",
            hoh_insurance=get_m2m_qs(InsuranceTypes),
            hoh_insurance_other=None,
            crf_status=COMPLETE,
            crf_status_comments="",
        )
        cleaned_data.update(**kwargs)
        return cleaned_data

    def test_cleaned_data_ok(self):
        instance = HealthEconomicsHouseholdHead()
        cleaned_data = self.get_cleaned_data()
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data,
            instance=instance,
            model=HealthEconomicsHouseholdHead,
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_relationship_to_hoh_applicable_if_not_hoh(self):
        instance = HealthEconomicsHouseholdHead()
        opts = dict(
            instance=instance,
            model=HealthEconomicsHouseholdHead,
        )
        cleaned_data = self.get_cleaned_data(hoh=YES, relationship_to_hoh=None)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("relationship_to_hoh", form_validator._errors)
        self.assertIn(
            "This field is not applicable",
            str(form_validator._errors.get("relationship_to_hoh")),
        )

        cleaned_data = self.get_cleaned_data(hoh=YES, relationship_to_hoh=NOT_APPLICABLE)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

        cleaned_data.update(hoh=NO, relationship_to_hoh=None)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("relationship_to_hoh", form_validator._errors)
        self.assertIn(
            "This field is applicable", str(form_validator._errors.get("relationship_to_hoh"))
        )

        cleaned_data.update(hoh=NO, relationship_to_hoh=NOT_APPLICABLE)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("relationship_to_hoh", form_validator._errors)
        self.assertIn(
            "This field is applicable", str(form_validator._errors.get("relationship_to_hoh"))
        )

        cleaned_data.update(hoh=NO, relationship_to_hoh=WIFE_HUSBAND)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

        cleaned_data.update(hoh=NO, relationship_to_hoh=OTHER)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("relationship_to_hoh_other", form_validator._errors)

        cleaned_data.update(
            hoh=NO, relationship_to_hoh=OTHER, relationship_to_hoh_other="blah"
        )
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_hoh_religion_other(self):
        instance = HealthEconomicsHouseholdHead()
        opts = dict(
            instance=instance,
            model=HealthEconomicsHouseholdHead,
        )
        cleaned_data = self.get_cleaned_data(
            hoh=YES,
            relationship_to_hoh=NOT_APPLICABLE,
            hoh_religion=OTHER,
            hoh_religion_other=None,
        )
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_religion_other", form_validator._errors)
        self.assertIn(
            "This field is required",
            str(form_validator._errors.get("hoh_religion_other")),
        )
