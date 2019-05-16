from czaSpider import pipelines


def get_custom_settings(name, parse_item=False):  # todo, wait for code transplant, to pipeline?
    if not parse_item:
        return getattr(pipelines, "sourcePipeline_setting")
    pipelineName = name[name.rfind('-') + 1:] + "Pipeline_setting"
    return getattr(pipelines, pipelineName) if hasattr(pipelines, pipelineName) else {}
