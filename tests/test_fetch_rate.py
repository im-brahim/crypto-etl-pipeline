from jobs.scripts.rate import get_rate
from jobs.config import EXCHANGE_API_URL

def test_fetch_usd_mad():
    result = get_rate(EXCHANGE_API_URL)

    assert isinstance(result, dict)
    assert "USD/MAD" in result
    assert "rate" in result
    assert "datetime" in result
    assert "time_next_update" in result
    assert isinstance(result["rate"], (int, float))
    assert isinstance(result["datetime"], str)