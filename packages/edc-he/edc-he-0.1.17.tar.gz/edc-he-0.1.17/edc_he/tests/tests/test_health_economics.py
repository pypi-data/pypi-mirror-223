from __future__ import annotations

from django import forms
from django.test import TestCase, tag
from edc_constants.constants import COMPLETE, FEMALE, NO, NOT_APPLICABLE, OTHER, YES
from edc_metadata import NOT_REQUIRED, REQUIRED, site_metadata_rules
from edc_metadata.tests import CrfTestHelper
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
from edc_he.rule_groups import HealthEconomicsRuleGroup as BaseHealthEconomicsRuleGroup
from edc_he.rule_groups import Predicates

from ...utils import get_patient_model
from ..visit_schedule import visit_schedule


def get_m2m_qs(model_cls, name: str = None):
    if name:
        qs = model_cls.objects.filter(name=name)
    else:
        name = model_cls.objects.all()[0].name
        qs = model_cls.objects.filter(name=name).exclude(name=NOT_APPLICABLE)
    return qs


def get_obj(model_cls, name: str = None):
    if name:
        obj = model_cls.objects.get(name=name)
    else:
        obj = model_cls.objects.all()[0]
    return obj


class HealthEconomicsHouseholdHeadTests(LongitudinalTestCaseMixin, CrfTestHelper, TestCase):
    visit_schedule = visit_schedule

    def setUp(self) -> None:
        self.subject_identifier = self.enroll()
        self.create_visits(self.subject_identifier)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        class HealthEconomicsRuleGroup(BaseHealthEconomicsRuleGroup):
            class Meta:
                app_label = "edc_he"
                source_model = "edc_visit_tracking.subjectvisit"
                predicates = Predicates()

        site_metadata_rules.register(HealthEconomicsRuleGroup)

    def get_cleaned_data(self, **kwargs) -> dict:
        cleaned_data = dict(
            subject_visit=self.subject_visit_baseline,
            report_datetime=get_utcnow(),
            hh_count=5,
            hh_minors_count=1,
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
            relationship_to_hoh_other=None,
            hoh_gender=FEMALE,
            hoh_age=25,
            hoh_religion=get_obj(Religions),
            hoh_religion_other=None,
            hoh_ethnicity=get_obj(Ethnicities),
            hoh_ethnicity_other=None,
            hoh_education=get_obj(Education),
            hoh_education_other=None,
            hoh_employment_status="",
            hoh_employment_type=get_obj(EmploymentType),
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

        not_applicable_opts = dict(
            hoh_religion=get_obj(Religions, NOT_APPLICABLE),
            hoh_ethnicity=get_obj(Ethnicities, NOT_APPLICABLE),
            hoh_education=get_obj(Education, NOT_APPLICABLE),
            hoh_employment_type=get_obj(EmploymentType, NOT_APPLICABLE),
            hoh_insurance=get_m2m_qs(InsuranceTypes, NOT_APPLICABLE),
        )
        cleaned_data = self.get_cleaned_data(
            hoh=YES,
            relationship_to_hoh=None,
            **not_applicable_opts,
        )
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

        cleaned_data = self.get_cleaned_data(
            hoh=YES,
            relationship_to_hoh=NOT_APPLICABLE,
            **not_applicable_opts,
        )
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

        applicable_opts = dict(
            hoh_religion=get_obj(Religions),
            hoh_ethnicity=get_obj(Ethnicities),
            hoh_education=get_obj(Education),
            hoh_employment_type=get_obj(EmploymentType),
            hoh_insurance=get_m2m_qs(InsuranceTypes),
        )

        cleaned_data.update(hoh=NO, relationship_to_hoh=WIFE_HUSBAND, **applicable_opts)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

        cleaned_data.update(hoh=NO, relationship_to_hoh=OTHER, **applicable_opts)
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("relationship_to_hoh_other", form_validator._errors)

        cleaned_data.update(
            hoh=NO,
            relationship_to_hoh=OTHER,
            relationship_to_hoh_other="blah",
            **applicable_opts,
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
        applicable_opts = dict(
            hoh_ethnicity=get_obj(Ethnicities),
            hoh_education=get_obj(Education),
            hoh_employment_type=get_obj(EmploymentType),
            hoh_insurance=get_m2m_qs(InsuranceTypes),
        )
        cleaned_data = self.get_cleaned_data()
        cleaned_data.update(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
            hoh_religion=None,
            **applicable_opts,
        )
        form_validator = HealthEconomicsHouseholdHeadFormValidator(
            cleaned_data=cleaned_data, **opts
        )
        with self.assertRaises(forms.ValidationError):
            form_validator.validate()
        self.assertIn("hoh_religion", form_validator._errors)
        self.assertIn(
            "This field is applicable",
            str(form_validator._errors.get("hoh_religion")),
        )

        cleaned_data = self.get_cleaned_data(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
            hoh_religion=get_obj(Religions, OTHER),
            **applicable_opts,
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

    def test_patient_required_if_patient_is_not_hoh(self):
        cleaned_data = self.get_cleaned_data(
            hoh=NO,
            relationship_to_hoh=WIFE_HUSBAND,
        )
        del cleaned_data["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**cleaned_data)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))

        qs = self.crf_metadata_obj(get_patient_model(), REQUIRED, "1000")
        self.assertTrue(qs.exists())

    @tag("1")
    def test_patient_required_if_patient_is_hoh(self):
        cleaned_data = self.get_cleaned_data(
            hoh=YES,
            relationship_to_hoh=NOT_APPLICABLE,
        )
        del cleaned_data["hoh_insurance"]
        hoh_obj = HealthEconomicsHouseholdHead.objects.create(**cleaned_data)
        hoh_obj.hoh_insurance.add(get_obj(InsuranceTypes))

        qs = self.crf_metadata_obj(get_patient_model(), NOT_REQUIRED, "1000")
        self.assertTrue(qs.exists())
