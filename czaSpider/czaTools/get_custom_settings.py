from czaSpider import pipelines


def get_custom_settings(name, parse_item=False):
    if not parse_item:
        return getattr(pipelines, "sourcePipeline_setting")
    pipelineName = name[name.rfind('-') + 1:] + "Pipeline_setting"  # 为定义特殊管道，则使用公共管道
    return getattr(pipelines, pipelineName) if hasattr(pipelines, pipelineName) else getattr(pipelines, "publicPipeline_setting")
