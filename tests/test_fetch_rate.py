from jobs.scripts.rate import get_rate
from jobs.config import EXCHANGE_API_URL

def test_fetch_usd_mad():
    result = get_rate(EXCHANGE_API_URL)
    assert isinstance(result, list)
    assert len(result) > 0
    assert "rate" in result[0]
    assert "base" in result[0]
    assert "target" in result[0]
    assert result[0]["base"] == "USD"
    assert result[0]["target"] == "MAD"