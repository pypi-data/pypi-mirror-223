use super::date_errors::TimeFractionCalculationError;
pub enum TimeFraction {
    YEAR,
    MONTH,
    WEEK,
    DAY
}
impl TimeFraction {
    pub fn get_time_fraction(frac: &str) -> Result<TimeFraction, TimeFractionCalculationError> {
        match frac {
            "YEAR" => return Ok(TimeFraction::YEAR),
            "MONTH" => return Ok(TimeFraction::MONTH),
            "WEEK" => return Ok(TimeFraction::WEEK),
            "DAY" => return Ok(TimeFraction::DAY),
            _ => Err(TimeFractionCalculationError)
            
        }
    }
}