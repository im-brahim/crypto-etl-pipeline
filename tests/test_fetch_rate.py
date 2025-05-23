from jobs.scripts.rate import get_rate
from jobs.utils.config import EXCHANGE_API_URL

def test_fetch_rate():
    result = get_rate(EXCHANGE_API_URL)
    
    assert isinstance(result, dict)
    assert "base/target" in result
    assert "rate" in result
    assert "datetime" in result
    assert "time_next_update" in result
    
    assert result["base/target"] == "USD/MAD"
    assert isinstance(result["rate"], float)
    assert isinstance(result["datetime"], str)
    assert isinstance(result["time_next_update"], str)