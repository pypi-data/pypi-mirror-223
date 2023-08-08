use chrono::{NaiveDateTime, ParseError, NaiveDate, NaiveTime};
use pyo3::types::{PyDateTime, PyDate, PyDateAccess, PyTimeAccess};
use super::date_errors::{PyDateTimeToChronoNaiveDateTimeConversionError, PyDateToChronoNaiveDateConversionError};

pub fn parse_datetime_from_str(date_str: &str, format: &str) -> Result<NaiveDateTime, ParseError> {
    return NaiveDateTime::parse_from_str(&date_str, &format);
}
pub fn parse_date_from_str(date_str: &str, format: &str) -> Result<NaiveDate, ParseError> {
    return NaiveDate::parse_from_str(&date_str, &format);
}

pub fn convert_pydate_to_naivedate(pydate: &PyDate) -> Result<NaiveDate, PyDateToChronoNaiveDateConversionError> {
    return NaiveDate::from_ymd_opt(
        pydate.get_year() as i32,
        pydate.get_month() as u32,
        pydate.get_day() as u32
    ).ok_or_else(|| PyDateToChronoNaiveDateConversionError);
}
pub fn convert_pydate_to_naivedatetime(pydatetime: &PyDateTime) -> Result<NaiveDateTime, PyDateTimeToChronoNaiveDateTimeConversionError> {
    let date: Result<NaiveDate, PyDateTimeToChronoNaiveDateTimeConversionError> = NaiveDate::from_ymd_opt(
        pydatetime.get_year() as i32,
        pydatetime.get_month() as u32,
        pydatetime.get_day() as u32
    ).ok_or_else(|| PyDateTimeToChronoNaiveDateTimeConversionError);
    let time: Result<NaiveTime, PyDateTimeToChronoNaiveDateTimeConversionError> = NaiveTime::from_hms_opt(
        pydatetime.get_hour() as u32,
        pydatetime.get_minute() as u32,
        pydatetime.get_second() as u32
    ).ok_or_else(|| PyDateTimeToChronoNaiveDateTimeConversionError);

    return Ok(NaiveDateTime::new(date?, time?));
}