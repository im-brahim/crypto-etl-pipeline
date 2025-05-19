from jobs.fetch_rate import fetch_usd_mad

def test_fetch_usd_mad():
    result = fetch_usd_mad()
    assert isinstance(result, list)
    assert len(result) > 0
    assert "rate" in result[0]
    assert "base" in result[0]
    assert "target" in result[0]
    assert result[0]["base"] == "USD"
    assert result[0]["target"] == "MAD"