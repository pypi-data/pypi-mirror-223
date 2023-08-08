use chrono::{NaiveDateTime, NaiveDate, Duration};
use super::{
    time_fractions::{TimeFraction::*, self},
    date_errors::TimeFractionCalculationError
};

pub fn get_duration_from_date(start: NaiveDate, end: NaiveDate) -> Duration {
    return end.signed_duration_since(start);
}

pub fn get_duration_from_datetime(start: NaiveDateTime, end: NaiveDateTime) -> Duration {
    return end.signed_duration_since(start);
}

pub fn get_fraction_calculation(duration: Duration, frac: &str) -> Result<f64,TimeFractionCalculationError> {
    let days: i64 = duration.num_days();
    
    match time_fractions::TimeFraction::get_time_fraction(frac)? {
        YEAR =>
            return Ok(calculate_years(days)),
        MONTH => 
            return Ok(calculate_months(days)),
        WEEK =>
            return Ok(duration.num_weeks() as f64), 
        DAY => 
            return Ok(days as f64)
    }
}

fn calculate_years(days: i64) -> f64 {
    let f_days: f64 = days as f64;
    return f_days / 365.25 as f64
}
fn calculate_months(days: i64) -> f64 {
    let years: f64 = calculate_years(days);
    return years * 12.0;
}
