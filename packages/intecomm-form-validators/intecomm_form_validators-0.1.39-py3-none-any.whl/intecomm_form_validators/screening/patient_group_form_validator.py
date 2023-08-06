from django.utils.html import format_html
from edc_constants.constants import COMPLETE, NEW
from edc_form_validators import FormValidator

from ..constants import RECRUITING
from ..utils import (
    PatientGroupRatioError,
    PatientGroupSizeError,
    PatientNotConsentedError,
    PatientNotScreenedError,
    PatientNotStableError,
    PatientUnwillingToScreenError,
    confirm_patient_group_size_or_raise,
    confirm_patients_stable_and_screened_and_consented_or_raise,
    get_group_size_for_ratio,
    verify_patient_group_ratio_raise,
)
from .patient_group_rando_form_validator import INVALID_RANDOMIZE

INVALID_PATIENT_COUNT = "INVALID_PATIENT_COUNT"
INVALID_PATIENT = "INVALID_PATIENT"
INVALID_CONDITION_RATIO = "INVALID_CONDITION_RATIO"
INVALID_STATUS = "INVALID_STATUS"


class PatientGroupFormValidator(FormValidator):
    def clean(self):
        self.block_changes_if_already_randomized()
        if self.cleaned_data.get("status") and self.cleaned_data.get("status") not in [
            NEW,
            RECRUITING,
            COMPLETE,
        ]:
            self.raise_validation_error({"status": "Invalid selection"}, INVALID_STATUS)

        # if (
        #     self.cleaned_data.get("status") != COMPLETE
        #     and self.cleaned_data.get("randomize_now") == YES
        # ):
        #     self.raise_validation_error(
        #         {"randomize_now": "Invalid. Group is not complete"}, INVALID_RANDOMIZE
        #     )

        # if (
        #     self.cleaned_data.get("status") == COMPLETE
        #     and self.instance.status != COMPLETE
        #     and self.cleaned_data.get("randomize_now") == YES
        # ):
        #     self.raise_validation_error(
        #         {
        #             "randomize_now": (
        #                 "First set to NO and set status to complete/ready and save. "
        #                 "Reopen and try again with YES."
        #             )
        #         },
        #         INVALID_RANDOMIZE,
        #     )

        if self.cleaned_data.get("status") == COMPLETE:
            self.confirm_patients_stable_and_screened_and_consented_or_raise()
            self.confirm_patient_group_size_or_raise()
            self.verify_patient_group_ratio_raise()

    def block_changes_if_already_randomized(self):
        if self.instance.randomized:
            self.raise_validation_error(
                "A randomized group may not be changed", INVALID_RANDOMIZE
            )

    def confirm_patient_group_size_or_raise(self):
        try:
            confirm_patient_group_size_or_raise(
                bypass_group_size_min=self.cleaned_data.get("bypass_group_size_min"),
                patients=self.cleaned_data.get("patients") or self.instance.patients,
            )
        except PatientGroupSizeError as e:
            self.raise_validation_error({"__all__": str(e)}, INVALID_PATIENT_COUNT)

    def confirm_patients_stable_and_screened_and_consented_or_raise(self):
        try:
            confirm_patients_stable_and_screened_and_consented_or_raise(
                patients=self.cleaned_data.get("patients") or self.instance.patients
            )
        except (
            PatientNotStableError,
            PatientNotScreenedError,
            PatientNotConsentedError,
            PatientUnwillingToScreenError,
        ) as e:
            self.raise_validation_error({"__all__": str(e)}, INVALID_PATIENT)

    def verify_patient_group_ratio_raise(self):
        patients = self.cleaned_data.get("patients") or self.instance.patients
        if (
            not self.cleaned_data.get("bypass_group_ratio")
            and patients.all().count() >= get_group_size_for_ratio()
        ):
            try:
                verify_patient_group_ratio_raise(patients=patients.all())
            except PatientGroupRatioError as e:
                group_name = self.cleaned_data.get("name")
                errmsg = (
                    f'See group <a href="{self.instance.get_changelist_url(group_name)}">'
                    f"{group_name}</a>"
                )
                self.raise_validation_error(
                    {"__all__": format_html(f"{e} {errmsg}")}, INVALID_CONDITION_RATIO
                )
