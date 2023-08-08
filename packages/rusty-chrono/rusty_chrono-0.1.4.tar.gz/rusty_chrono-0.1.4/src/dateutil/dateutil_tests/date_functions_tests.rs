#[cfg(test)]
mod date_functions_tests {
    use test_case::test_case;
    use std::any::Any;
    use chrono::{NaiveDate, NaiveDateTime, NaiveTime, Duration};
    use crate::dateutil::{date_functions::*, date_errors::TimeFractionCalculationError};

    #[test_case(
        NaiveDate::from_ymd_opt(2020, 1, 1).unwrap(),
        NaiveDate::from_ymd_opt(2023, 12, 31).unwrap();
        "function should return a chrono::Duration object"
    )]
    fn test_object_get_duration_from_date(start_date: NaiveDate, end_date: NaiveDate) {
        let duration: Duration = get_duration_from_date(start_date, end_date);
        let actual: Box<dyn Any> = Box::new(duration);
        let expected: bool = true;

        assert_eq!(actual.is::<Duration>(), expected);
    }

    #[test_case(
        NaiveDateTime::new(NaiveDate::from_ymd_opt(2020, 1, 1).unwrap(), NaiveTime::from_hms_opt(0, 0, 0).unwrap()),
        NaiveDateTime::new(NaiveDate::from_ymd_opt(2023, 12, 31).unwrap(), NaiveTime::from_hms_opt(23, 59, 59).unwrap());
        "function should return a chrono::Duration object"
    )]
    fn test_object_get_duration_from_datetime(start_date: NaiveDateTime, end_date: NaiveDateTime) {
        let duration: Duration = get_duration_from_datetime(start_date, end_date);
        let actual: Box<dyn Any> = Box::new(duration);
        let expected: bool = true;

        assert_eq!(actual.is::<Duration>(), expected);
    }

    #[test_case(
        NaiveDate::from_ymd_opt(2023, 1, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2020, 1, 1).unwrap()),
        "YEAR",
        3.0,
        true;
        "function should return 3 years when fraction is year with duration"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 9, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2020, 1, 1).unwrap()),
        "YEAR",
        3.0,
        false;
        "function should not return 3 years when fraction is year with duration more in upper half of the third year"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2020, 1, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2023, 1, 1).unwrap()),
        "YEAR",
        -3.0,
        true;
        "function should return negative 3 years when fraction is year with duration"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 9, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2020, 1, 1).unwrap()),
        "YEAR",
        4.0,
        true;
        "function should return 4 years when fraction is year with duration more in upper half of the third year"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 2, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2023, 1, 1).unwrap()),
        "MONTH",
        1.0,
        true;
        "function should return 1 month when fraction is month with duration"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 1, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2023, 2, 1).unwrap()),
        "MONTH",
        -1.0,
        true;
        "function should return negative 1 month when fraction is month with duration"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 2, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2023, 1, 25).unwrap()),
        "MONTH",
        0.0,
        true;
        "function should return 0 month when fraction is month with duration when is in upper half of month"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 2, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2022, 12, 14).unwrap()),
        "MONTH",
        2.0,
        true;
        "function should return 0 month when fraction is month with duration when is in lower half of last month"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 1, 8).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2023, 1, 1).unwrap()),
        "WEEK",
        1.0,
        true;
        "function should return 1 week when fraction is week with duration"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 1, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2023, 1, 8).unwrap()),
        "WEEK",
        -1.0,
        true;
        "function should return negative 1 week when fraction is week with duration"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 1, 15).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2023, 1, 1).unwrap()),
        "WEEK",
        2.0,
        true;
        "function should return 2 weeks when fraction is week with duration"
    )]
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 1, 24).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2023, 1, 1).unwrap()),
        "DAY",
        23.0,
        true;
        "function should return 23 days when fraction is day with duration"
    )]
    fn test_get_fraction_calculation(duration: Duration, frac: &str, expected: f64, equal: bool) {
        let date_diff: f64 = get_fraction_calculation(duration, frac).unwrap();
        let actual = date_diff.round();
        if equal {
            assert_eq!(actual, expected);
        }
        else {
            assert_ne!(actual, expected)
        }
    }
    
    #[test_case(
        NaiveDate::from_ymd_opt(2023, 1, 1).unwrap().signed_duration_since(NaiveDate::from_ymd_opt(2020, 1, 1).unwrap()),
        "unknown";
        "function should raise FractionCalculationError"
    )]
    fn test_fraction_error(duration: Duration, frac: &str) {

        let actual = get_fraction_calculation(duration, frac).unwrap_err();
        let expected: TimeFractionCalculationError = Err::<f64, TimeFractionCalculationError>(TimeFractionCalculationError).unwrap_err();
        assert_eq!(actual.to_string(), expected.to_string());
    }
}