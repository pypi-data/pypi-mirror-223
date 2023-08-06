from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Extra

from likeinterface.utils.pydantic import ExcludeNone


class LikeObject(ExcludeNone, BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra=Extra.allow,
        validate_assignment=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class MutableLikeObject(LikeObject):
    model_config = ConfigDict(
        frozen=False,
    )
