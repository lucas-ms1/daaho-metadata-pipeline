import unittest

from app.derivations import derive_normalized_title
from app.validation_core import validate_core


def _base_metadata(**overrides):
    metadata = {
        "title": "Letter to Mr. Kiyoshi Tomizawa from the President, 1937",
        "date": "1937",
        "decade": "1930-1939",
        "place": "Ohio--Oxford",
        "subjects": ["Education"],
    }
    metadata.update(overrides)
    return metadata


class ValidationCoreTests(unittest.TestCase):
    def test_missing_place_is_optional(self):
        report = validate_core(
            md=_base_metadata(place=None),
            transcript=None,
            approved_places={"Ohio--Oxford"},
            approved_subjects={"Education"},
        )
        place_errors = [entry for entry in report["errors"] if entry.get("field") == "place"]
        self.assertEqual(place_errors, [])

    def test_invalid_place_format_is_error(self):
        report = validate_core(
            md=_base_metadata(place="Oxford, Ohio"),
            transcript=None,
            approved_places={"Ohio--Oxford"},
            approved_subjects={"Education"},
        )
        codes = {entry.get("code") for entry in report["errors"] if entry.get("field") == "place"}
        self.assertIn("invalid_place_format", codes)

    def test_canonicalized_place_variant_is_accepted(self):
        report = validate_core(
            md=_base_metadata(place="Massachusetts--Glouchester"),
            transcript=None,
            approved_places={"Massachusetts--Gloucester"},
            approved_subjects={"Education"},
        )
        place_errors = [entry for entry in report["errors"] if entry.get("field") == "place"]
        self.assertEqual(place_errors, [])

    def test_subject_outside_approved_list_is_error(self):
        report = validate_core(
            md=_base_metadata(subjects=["History"]),
            transcript=None,
            approved_places={"Ohio--Oxford"},
            approved_subjects={"Education"},
        )
        subject_errors = [entry for entry in report["errors"] if entry.get("field") == "subjects"]
        codes = {entry.get("code") for entry in subject_errors}
        self.assertIn("subject_not_in_locally_approved_list", codes)
        self.assertTrue(any(entry.get("suggestions") for entry in subject_errors))

    def test_case_insensitive_subject_match_passes(self):
        report = validate_core(
            md=_base_metadata(subjects=["education"]),
            transcript=None,
            approved_places={"Ohio--Oxford"},
            approved_subjects={"Education"},
        )
        codes = {entry.get("code") for entry in report["errors"] if entry.get("field") == "subjects"}
        self.assertNotIn("subject_not_in_locally_approved_list", codes)


class DerivationsTests(unittest.TestCase):
    def test_title_suffix_normalization_variants(self):
        cases = [
            (
                "Letter to Mr. Kiyoshi Tomizawa from the President",
                "1937",
                "Letter to Mr. Kiyoshi Tomizawa from the President, 1937",
            ),
            (
                "Letter to Mr. Kiyoshi Tomizawa from the President",
                "1937-10",
                "Letter to Mr. Kiyoshi Tomizawa from the President, October 1937",
            ),
            (
                "Letter to Mr. Kiyoshi Tomizawa from the President, 16 November",
                "1937-11-16",
                "Letter to Mr. Kiyoshi Tomizawa from the President, 16 November 1937",
            ),
            (
                "Itinerary document for Upham",
                None,
                "Itinerary document for Upham, undated",
            ),
        ]
        for raw_title, date_value, expected in cases:
            with self.subTest(date_value=date_value):
                normalized_title, _, changed = derive_normalized_title(raw_title, date_value)
                self.assertEqual(normalized_title, expected)
                self.assertTrue(changed)

    def test_title_validation_passes_after_normalization(self):
        normalized_title, _, _ = derive_normalized_title(
            "Letter to Mr. Kiyoshi Tomizawa from the President, 16 November",
            "1937-11-16",
        )
        report = validate_core(
            md=_base_metadata(
                title=normalized_title,
                date="1937-11-16",
                decade="1930-1939",
            ),
            transcript=None,
            approved_places={"Ohio--Oxford"},
            approved_subjects={"Education"},
        )
        title_errors = [entry for entry in report["errors"] if entry.get("field") == "title"]
        self.assertEqual(title_errors, [])


if __name__ == "__main__":
    unittest.main()
