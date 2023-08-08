mod dateutil;

use pyo3::{
    prelude::*,
    types::{PyDateTime, PyDate},
    exceptions::PyValueError
};
use chrono::{NaiveDateTime, NaiveDate, Duration, ParseError};
use dateutil::{
    date_parsing::*,
    date_functions::*,
    date_errors::*
};

#[pymodule]
fn rusty_chrono(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(datediff, m)?)?;
    m.add_function(wrap_pyfunction!(datediff_from_pydatetime, m)?)?;
    m.add_function(wrap_pyfunction!(datediff_from_pydate, m)?)?;
    
    return Ok(());
}


#[pyfunction()]
fn datediff(start_date: &str, end_date: &str, fmt: &str, frac: &str, fmt_type: Option<&str>) -> PyResult<f64> {
    let duration: Duration;
    if fmt_type.unwrap_or("date") == "datetime" {
        let start: NaiveDateTime = parse_datetime_from_str(start_date, fmt).map_err(|e: ParseError| PyValueError::new_err(e.to_string()))?;
        let end: NaiveDateTime = parse_datetime_from_str(end_date, fmt).map_err(|e: ParseError| PyValueError::new_err(e.to_string()))?;
        duration = get_duration_from_datetime(start, end);
    }
    else {
        let start: NaiveDate = parse_date_from_str(start_date, fmt).map_err(|e: ParseError| PyValueError::new_err(e.to_string()))?;
        let end: NaiveDate = parse_date_from_str(end_date, fmt).map_err(|e: ParseError| PyValueError::new_err(e.to_string()))?;
        duration = get_duration_from_date(start, end);
    }

    return get_fraction_calculation(duration, frac).map_err(|e: TimeFractionCalculationError| PyValueError::new_err(e.to_string()));
}

#[pyfunction]
fn datediff_from_pydatetime(start_date: &PyDateTime, end_date: &PyDateTime, frac: &str) -> PyResult<f64> {
    let start: NaiveDateTime = convert_pydate_to_naivedatetime(start_date).map_err(|e: PyDateTimeToChronoNaiveDateTimeConversionError| PyValueError::new_err(e.to_string()))?;
    let end: NaiveDateTime = convert_pydate_to_naivedatetime(end_date).map_err(|e: PyDateTimeToChronoNaiveDateTimeConversionError| PyValueError::new_err(e.to_string()))?;
    let duration: Duration = end.signed_duration_since(start);

    return get_fraction_calculation(duration, frac).map_err(|e: TimeFractionCalculationError| PyValueError::new_err(e.to_string()));
}

#[pyfunction]
fn datediff_from_pydate(start_date: &PyDate, end_date: &PyDate, frac: &str) -> PyResult<f64> {
    let start: NaiveDate = convert_pydate_to_naivedate(start_date).map_err(|e: PyDateToChronoNaiveDateConversionError| PyValueError::new_err(e.to_string()))?;
    let end: NaiveDate = convert_pydate_to_naivedate(end_date).map_err(|e: PyDateToChronoNaiveDateConversionError| PyValueError::new_err(e.to_string()))?;
    let duration: Duration = end.signed_duration_since(start);

    return get_fraction_calculation(duration, frac).map_err(|e: TimeFractionCalculationError| PyValueError::new_err(e.to_string()));
}