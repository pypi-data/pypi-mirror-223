#[cfg(test)]
mod date_parsing_tests {
    use chrono::format::ParseErrorKind;
    use test_case::test_case;
    use crate::dateutil::date_parsing::*;
    
    #[test_case("2010-12-12 16:21:45", "%Y-%m-%d %H:%M:%S"; "when is valid datetime format")]
    fn test_valid_parse_datetime_from_str(date_str: &str, fmt: &str){
        let result: bool = parse_datetime_from_str(date_str, fmt).is_ok();
        let expected: bool = true;
        assert_eq!(expected, result);
    }
    
    #[test_case("2010-12-12 16:21", "%Y-%m-%d", ParseErrorKind::TooLong; "when passed datetime too long for format")]
    #[test_case("2010-12-12", "%Y-%m-%d %H:%M", ParseErrorKind::TooShort; "when passed datetime too short for format")]
    #[test_case("2010-12-12 16:21", "%Y-%m-%d %h:%m", ParseErrorKind::Invalid; "when passed invalid datetime format")]
    #[test_case("2010-2012-12-12 16:21", "%Y-%Y-%m-%d %h:%m", ParseErrorKind::Impossible; "when passed year twice in datetime and format")]
    #[test_case("2010-04-12 16:21", "%Y-%-%d %h:%m", ParseErrorKind::BadFormat; "when passed format with missing specifier")]
    #[test_case("2012-13-12 16:21", "%Y-%m-%d %H:%M", ParseErrorKind::OutOfRange; "when passed datetime is out of calendar possibilities")]
    fn test_invalid_parse_datetime_from_str(date_str: &str, fmt: &str, expected_error: ParseErrorKind){
        let result: Result<chrono::NaiveDateTime, ParseErrorKind> = parse_datetime_from_str(date_str, fmt).map_err(|e| e.kind());
        let expected: Result<chrono::NaiveDateTime, ParseErrorKind> = Err(expected_error);
        assert_eq!(expected, result);
    }

    #[test_case("2010-12-12", "%Y-%m-%d"; "when is valid date format")]
    fn test_valid_parse_date_from_str(date_str: &str, fmt: &str){
        let result: bool = parse_date_from_str(date_str, fmt).is_ok();
        let expected: bool = true;
        assert_eq!(expected, result);
    }
    #[test_case("2010-12-12", "%Y-%m", ParseErrorKind::TooLong; "when date is too long for format")]
    #[test_case("2010-12", "%Y-%m-%d", ParseErrorKind::TooShort; "when passed date too short for format")]
    #[test_case("2010-12-12", "%S-%m-%d", ParseErrorKind::Invalid; "when passed date format is invalid")]
    #[test_case("2010-12-12", "%Y-%m-%H", ParseErrorKind::NotEnough; "when passed  hours instead of day in date format")]
    #[test_case("2010-2012-12-12", "%Y-%Y-%m-%d", ParseErrorKind::Impossible; "when passed year twice in date and format")]
    #[test_case("2010-04-12", "%Y-%-%d", ParseErrorKind::BadFormat; "when passed format with missing specifier")]
    #[test_case("2012-13-12", "%Y-%m-%d", ParseErrorKind::OutOfRange; "when passed datetime is out of calendar possibilities")]
    fn test_invalid_parse_date_from_str(date_str: &str, fmt: &str, expected_error: ParseErrorKind){
        let result: Result<chrono::NaiveDateTime, ParseErrorKind> = parse_datetime_from_str(date_str, fmt).map_err(|e| e.kind());
        let expected: Result<chrono::NaiveDateTime, ParseErrorKind> = Err(expected_error);
        assert_eq!(expected, result);
    }
}
