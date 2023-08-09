from lida import TextGenerationConfig, llm
from lida.modules import Manager


lida = Manager(text_gen=llm("openai"))


cars_data_url = "https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv"


def test_summarizer():
    textgen_config = TextGenerationConfig(n=1, temperature=0.5, use_cache=False, max_tokens=None)
    summary_no_enrich = lida.summarize(cars_data_url, enrich=False)
    summary = lida.summarize(
        "https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv",
        textgen_config=textgen_config, enrich=True)

    assert summary_no_enrich != summary
    assert "dataset_description" in summary and len(summary["dataset_description"]) > 0


def test_goals():
    textgen_config = TextGenerationConfig(n=1, temperature=0.5, use_cache=False, max_tokens=None)
    summary = lida.summarize(
        cars_data_url,
        textgen_config=textgen_config, enrich=False)

    goals = lida.generate_goals(summary, n=2, textgen_config=textgen_config)
    assert len(goals) == 2
    assert len(goals[0].question) > 0


def test_vizgen():
    textgen_config = TextGenerationConfig(
        n=1,
        temperature=0.1,
        use_cache=True,
        max_tokens=None)
    summary = lida.summarize(
        cars_data_url,
        textgen_config=textgen_config, enrich=False)

    goals = lida.generate_goals(summary, n=2, textgen_config=textgen_config)
    vis_specs = lida.generate_viz(
        summary=summary,
        goal=goals[0],
        textgen_config=textgen_config,
        library="seaborn")
    charts = lida.execute_viz(
        code_specs=vis_specs,
        data=lida.data,
        summary=summary,
        library="seaborn")

    assert len(charts) > 0
    assert len(charts[0].raster) > 0
