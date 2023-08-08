use std::{error::Error, fmt};

const TIME_FRACTION_CALCULATION_ERROR_MESSAGE: &str = "Time fraction unknown or not supported";
const PY_DATE_TO_CHRONO_NAIVE_DATE_CONVERSION_ERROR_MESSAGE: &str = "Cannot convert PyDate to chrono::NaiveDate";
const PY_DATETIME_TO_CHRONO_NAIVE_DATETIME_CONVERSION_ERROR_MESSAGE: &str = "Cannot convert PyDate to chrono::NaiveDateTime";

#[derive(Debug)]
pub struct TimeFractionCalculationError;

impl Error for TimeFractionCalculationError {}
impl fmt::Display for TimeFractionCalculationError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "{}", TIME_FRACTION_CALCULATION_ERROR_MESSAGE);
    }
}

#[derive(Debug)]
pub struct PyDateToChronoNaiveDateConversionError;

impl Error for PyDateToChronoNaiveDateConversionError {}
impl fmt::Display for PyDateToChronoNaiveDateConversionError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "{}", PY_DATE_TO_CHRONO_NAIVE_DATE_CONVERSION_ERROR_MESSAGE);
    }
}

#[derive(Debug)]
pub struct PyDateTimeToChronoNaiveDateTimeConversionError;

impl Error for PyDateTimeToChronoNaiveDateTimeConversionError {}
impl fmt::Display for PyDateTimeToChronoNaiveDateTimeConversionError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "{}", PY_DATETIME_TO_CHRONO_NAIVE_DATETIME_CONVERSION_ERROR_MESSAGE);
    }
}