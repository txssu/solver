from solver import planner


def test_required_crews():
    cfg = planner.Config(num_objects=20, network_type="star", warehouses=1)
    avg_dist = 50
    crews = planner.required_crews(cfg, months=2, avg_distance_km=avg_dist)
    assert crews >= 1


def test_cost_estimate_keys():
    cfg = planner.Config(num_objects=10)
    result = planner.cost_estimate(cfg, months=2, avg_distance_km=10)
    for key in ["бригады", "зарплата", "автомобили", "гостиницы", "командировочные", "итого"]:
        assert key in result


def test_run_variants_and_report():
    results = planner.run_variants([2])
    assert len(results) == 4
    report = planner.generate_report(results)
    assert "Технико-экономический отчёт" in report
    heur = planner.derive_heuristics(results)
    assert len(heur) > 0

