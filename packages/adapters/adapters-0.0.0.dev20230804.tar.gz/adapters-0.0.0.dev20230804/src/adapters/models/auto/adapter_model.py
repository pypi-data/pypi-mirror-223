import warnings
from collections import OrderedDict

from transformers.models.auto.auto_factory import _BaseAutoModelClass, auto_class_update
from transformers.models.auto.configuration_auto import CONFIG_MAPPING_NAMES

from .auto_factory import _LazyAdapterModelAutoMapping


# Make sure that children are placed before parents!
ADAPTER_MODEL_MAPPING_NAMES = OrderedDict(
    [
        ("albert", "AlbertAdapterModel"),
        ("bart", "BartAdapterModel"),
        ("beit", "BeitAdapterModel"),
        ("bert", "BertAdapterModel"),
        ("bert-generation", "BertGenerationAdapterModel"),
        ("clip", "CLIPAdapterModel"),
        ("deberta", "DebertaAdapterModel"),
        ("deberta-v2", "DebertaV2AdapterModel"),
        ("distilbert", "DistilBertAdapterModel"),
        ("gpt2", "GPT2AdapterModel"),
        ("gptj", "GPTJAdapterModel"),
        ("mbart", "MBartAdapterModel"),
        ("roberta", "RobertaAdapterModel"),
        ("t5", "T5AdapterModel"),
        ("vit", "ViTAdapterModel"),
        ("xlm-roberta", "XLMRobertaAdapterModel"),
    ]
)
MODEL_WITH_HEADS_MAPPING_NAMES = OrderedDict(
    [
        ("bart", "BartModelWithHeads"),
        ("bert", "BertModelWithHeads"),
        ("distilbert", "DistilBertModelWithHeads"),
        ("gpt2", "GPT2ModelWithHeads"),
        ("mbart", "MBartModelWithHeads"),
        ("roberta", "RobertaModelWithHeads"),
        ("t5", "T5ModelWithHeads"),
        ("xlm-roberta", "XLMRobertaModelWithHeads"),
    ]
)

ADAPTER_MODEL_MAPPING = _LazyAdapterModelAutoMapping(CONFIG_MAPPING_NAMES, ADAPTER_MODEL_MAPPING_NAMES)
MODEL_WITH_HEADS_MAPPING = _LazyAdapterModelAutoMapping(CONFIG_MAPPING_NAMES, MODEL_WITH_HEADS_MAPPING_NAMES)


class AutoAdapterModel(_BaseAutoModelClass):
    _model_mapping = ADAPTER_MODEL_MAPPING


AutoAdapterModel = auto_class_update(AutoAdapterModel, head_doc="adapters and flexible heads")


class AutoModelWithHeads(_BaseAutoModelClass):
    _model_mapping = MODEL_WITH_HEADS_MAPPING

    @classmethod
    def from_config(cls, config):
        warnings.warn(
            "This class has been renamed to `{}` in v3. "
            "Please use the new class instead as this class might be removed in a future version.".format(
                cls.__bases__[0].__name__
            ),
            FutureWarning,
        )
        return super().from_config(config)

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs):
        warnings.warn(
            "This class has been renamed to `{}` in v3. "
            "Please use the new class instead as this class might be removed in a future version.".format(
                cls.__bases__[0].__name__
            ),
            FutureWarning,
        )
        return super().from_pretrained(pretrained_model_name_or_path, *model_args, **kwargs)


AutoModelWithHeads = auto_class_update(AutoModelWithHeads, head_doc="flexible heads")
