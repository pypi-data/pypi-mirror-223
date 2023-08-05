import re

from marshmallow import fields, Schema, INCLUDE, validate, ValidationError
from marshmallow.decorators import pre_load

from chicagorecoverypy.value_sets import CHICAGO_GEOGRAPHIES


def find_case_insensitive_match(value, value_list):
    if value is None:
        return None

    # Standardize formatting for wards and police districts
    try:
        assert int(value) <= 50
    except (ValueError, AssertionError):
        if "police" in value.lower():
            value = (
                f"police district {''.join(char for char in value if char.isdigit())}"
            )
        elif any(
            substr in value.lower()
            for substr in (
                "citywide",
                "total",
                "unknown",
                "unhoused",
                "homeless",
                "unstable",
            )
        ):
            value = "chicago"
        elif value.lower() == "o'hare":
            value = "ohare"
    else:
        value = f"ward {value}"

    try:
        (match,) = [
            v
            for v in value_list
            if v.casefold().replace(" ", "")
            == value.casefold().replace("'", "").replace(" ", "")
        ]
    except ValueError:
        if re.match(r"^\d{5}$", value):
            # Allow non-Chicago ZIP codes
            match = value
        else:
            match = None

    return match


class CaseInsensitiveOneOf(validate.OneOf):
    _jsonschema_base_validator_class = validate.OneOf

    def __call__(self, value) -> str:
        normalized_value = find_case_insensitive_match(value, self.choices)

        try:
            if not normalized_value:
                raise ValidationError(self._format_error(value))
        except TypeError as error:
            raise ValidationError(self._format_error(value)) from error

        return normalized_value


class ChicagoGeography(fields.String):
    def __init__(self, *args, **kwargs):
        # Add allowed value validation
        kwargs["validate"] = CaseInsensitiveOneOf(CHICAGO_GEOGRAPHIES)

        # Get error_messages, if provided, or create a fresh dict
        error_messages = kwargs.pop("error_messages", {})

        # Included allowed values if data missing
        error_messages["required"] = (
            "Missing data for required field. "
            f'Expected one of: {", ".join(CHICAGO_GEOGRAPHIES)}'
        )
        kwargs["error_messages"] = error_messages

        # Initialize as normal
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, obj, **kwargs):
        return find_case_insensitive_match(value, CHICAGO_GEOGRAPHIES)


class PreprocessedSchema(Schema):
    class Meta:
        unknown = INCLUDE

    @pre_load
    def preprocess_data(self, raw_data, **kwargs):
        cleaned_data = {}
        for k, v in raw_data.items():
            clean_k = k.lower().strip()

            if str(v).lower().strip() in ("not collected", "n/a", "can't count", ""):
                v = None

            clean_v = str(v).strip() if v not in ("", None) else None

            cleaned_data[clean_k] = clean_v
        return cleaned_data


class RecordLevelPlaceSchema(PreprocessedSchema):
    project_name = fields.String(data_key="project name", allow_none=True)
    applicant_organization = fields.String(
        data_key="applicant organization", allow_none=True
    )
    application_status = fields.String(data_key="application status", allow_none=True)
    announced_grant_amount = fields.Number(
        data_key="announced grant amount", allow_none=True
    )
    current_estimated_grant_amount = fields.Number(
        data_key="current estimated grant amount", allow_none=True
    )
    grant_amount_disbursed = fields.Number(
        data_key="grant amount disbursed", allow_none=True
    )
    total_project_cost = fields.Number(data_key="total project cost", allow_none=True)
    d_m_wbe_status = fields.String(data_key="d/m/wbe status", allow_none=True)
    street_address = fields.String(data_key="street address", allow_none=True)
    zip_code = fields.Number(data_key="zip code", allow_none=True)
    lat = fields.Number(data_key="lat", allow_none=True)
    lon = fields.Number(data_key="lon", allow_none=True)
    service_area = fields.String(data_key="service area", allow_none=True)
    submission_date = fields.String(data_key="submission date", allow_none=True)
    announcement_date = fields.String(data_key="announcement date", allow_none=True)
    opening_date = fields.String(data_key="opening date", allow_none=True)
    closing_date = fields.String(data_key="closing date", allow_none=True)
    project_status = fields.String(data_key="project status", allow_none=True)


class AggregatePlaceSchema(PreprocessedSchema):
    geography = ChicagoGeography(data_key="geography")
    start_date = fields.String(data_key="start date", allow_none=False)
    end_date = fields.String(data_key="end date", allow_none=False)
    number_of_projects_announced = fields.Number(
        data_key="number of projects announced", allow_none=True
    )
    number_of_projects_completed = fields.Number(
        data_key="number of projects completed", allow_none=True
    )
    number_of_applications_received = fields.Number(
        data_key="number of applications received", allow_none=True
    )
    number_of_d_m_wbe_applicants = fields.Number(
        data_key="number of d/m/wbe applicants", allow_none=True
    )
    number_of_grants_awarded_to_d_m_wbe_applicants = fields.Number(
        data_key="number of grants awarded to d/m/wbe applicants", allow_none=True
    )
    announced_grant_amount = fields.Number(
        data_key="announced grant amount", allow_none=True
    )
    current_estimated_grant_amount = fields.Number(
        data_key="current estimated grant amount", allow_none=True
    )
    grant_amount_disbursed = fields.Number(
        data_key="grant amount disbursed", allow_none=True
    )
    total_project_cost = fields.Number(data_key="total project cost", allow_none=True)


class AggregatePersonSchema(PreprocessedSchema):
    start_date = fields.String(data_key="start date", allow_none=False)
    # TODO: When template gets fixed, this should just be "end date"
    end_date = fields.String(data_key="start date end date", allow_none=False)
    age_18_24 = fields.Number(data_key="age 18 to 24", allow_none=True)
    age_25_34 = fields.Number(data_key="age 25 to 34", allow_none=True)
    age_35_49 = fields.Number(data_key="age 35 to 49", allow_none=True)
    age_50_64 = fields.Number(data_key="age 50 to 64", allow_none=True)
    age_over_65 = fields.Number(data_key="age over 65", allow_none=True)
    age_under_18 = fields.Number(data_key="age under 18", allow_none=True)
    age_unk = fields.Number(data_key="age unknown", allow_none=True)
    gender_female = fields.Number(data_key="gender identity female", allow_none=True)
    gender_male = fields.Number(data_key="gender identity male", allow_none=True)
    gender_nonbinary = fields.Number(
        data_key="gender identity nonbinary", allow_none=True
    )
    gender_none = fields.Number(
        data_key="gender identity none of these", allow_none=True
    )
    gender_unk = fields.Number(data_key="gender identity unknown", allow_none=True)
    geography = ChicagoGeography(data_key="geography")
    re_aian_hl = fields.Number(
        data_key="race/ethnicity american indian or alaska native hispanic or latino",
        allow_none=True,
    )
    re_aian_nhl = fields.Number(
        data_key="race/ethnicity american indian or alaska native not hispanic or latino",
        allow_none=True,
    )
    re_aian_unk = fields.Number(
        data_key="race/ethnicity american indian or alaska native unknown",
        allow_none=True,
    )
    re_asian_hl = fields.Number(
        data_key="race/ethnicity asian hispanic or latino", allow_none=True
    )
    re_asian_nhl = fields.Number(
        data_key="race/ethnicity asian not hispanic or latino", allow_none=True
    )
    re_asian_unk = fields.Number(
        data_key="race/ethnicity asian unknown", allow_none=True
    )
    re_black_hl = fields.Number(
        data_key="race/ethnicity black or african-american hispanic or latino",
        allow_none=True,
    )
    re_black_nhl = fields.Number(
        data_key="race/ethnicity black or african-american not hispanic or latino",
        allow_none=True,
    )
    re_black_unk = fields.Number(
        data_key="race/ethnicity black or african-american unknown", allow_none=True
    )
    re_mult_hl = fields.Number(
        data_key="race/ethnicity multiple races hispanic or latino", allow_none=True
    )
    re_mult_nhl = fields.Number(
        data_key="race/ethnicity multiple races not hispanic or latino", allow_none=True
    )
    re_mult_unk = fields.Number(
        data_key="race/ethnicity multiple races unknown", allow_none=True
    )
    re_nhpi_hl = fields.Number(
        data_key="race/ethnicity native hawaiian or other pacific islander hispanic or latino",
        allow_none=True,
    )
    re_nhpi_nhl = fields.Number(
        data_key="race/ethnicity native hawaiian or other pacific islander not hispanic or latino",
        allow_none=True,
    )
    re_nhpi_unk = fields.Number(
        data_key="race/ethnicity native hawaiian or other pacific islander unknown",
        allow_none=True,
    )
    re_none_hl = fields.Number(
        data_key="race/ethnicity none of these hispanic or latino", allow_none=True
    )
    re_none_nhl = fields.Number(
        data_key="race/ethnicity none of these not hispanic or latino", allow_none=True
    )
    re_none_unk = fields.Number(
        data_key="race/ethnicity none of these unknown", allow_none=True
    )
    re_unk_hl = fields.Number(
        data_key="race/ethnicity unknown hispanic or latino", allow_none=True
    )
    re_unk_unk = fields.Number(
        data_key="race/ethnicity unknown unknown", allow_none=True
    )
    re_unknown_nhl = fields.Number(
        data_key="race/ethnicity unknown not hispanic or latino", allow_none=True
    )
    re_while_hl = fields.Number(
        data_key="race/ethnicity white hispanic or latino", allow_none=True
    )
    re_white_nhl = fields.Number(
        data_key="race/ethnicity white not hispanic or latino", allow_none=True
    )
    re_white_unk = fields.Number(
        data_key="race/ethnicity white unknown", allow_none=True
    )
    service_center = fields.String(data_key="service center", allow_none=True)
    total_served = fields.Number(data_key="total served", allow_none=True)
