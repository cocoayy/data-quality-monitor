from app.scoring import calc_rank, calc_total_score


def test_calc_total_score():
    score = calc_total_score(
        completeness=80,
        freshness=70,
        accessibility=90,
        format_quality=100,
    )
    assert score == 80


def test_calc_rank():
    assert calc_rank(95) == "A"
    assert calc_rank(80) == "B"
    assert calc_rank(60) == "C"
    assert calc_rank(30) == "D"
    assert calc_rank(10) == "E"
