from edc_constants.constants import DONT_KNOW, NO, NONE, OTHER
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin
from edc_form_validators import FormValidator


class HealthEconomicsHouseholdHeadFormValidator(
    CrfFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        self.applicable_if(NO, field="hoh", field_applicable="relationship_to_hoh")
        self.validate_other_specify(field="relationship_to_hoh")

        self.validate_other_specify(field="hoh_religion")
        self.validate_other_specify(field="hoh_ethnicity")
        self.validate_other_specify(field="hoh_education")
        self.validate_other_specify(field="hoh_employment_type")
        self.validate_other_specify(field="hoh_marital_status")
        self.m2m_single_selection_if(DONT_KNOW, NONE, m2m_field="hoh_insurance")
        self.m2m_other_specify(
            OTHER, m2m_field="hoh_insurance", field_other="hoh_insurance_other"
        )
