from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, Optional, Union

from pydantic import BaseModel

from likeinterface.constants import UPDATE_FORWARD_REFS


class ExcludeNone:
    def model_dump(
        self,
        *,
        mode: str = "python",
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,  # noqa
        round_trip: bool = False,
        warnings: bool = True,
    ) -> Dict[str, Any]:
        return super(ExcludeNone, self).model_dump(  # type: ignore[misc]
            mode=mode,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=True,
            round_trip=round_trip,
            warnings=warnings,
        )

    def model_dump_json(
        self,
        *,
        indent: Optional[int] = None,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,  # noqa
        round_trip: bool = False,
        warnings: bool = True,
    ) -> str:
        return super(ExcludeNone, self).model_dump_json(  # type: ignore[misc]
            indent=indent,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=True,
            round_trip=round_trip,
            warnings=warnings,
        )


def update_forward_refs_helper(
    __all__: Iterable[str], __models__: Dict[str, Union[Any, BaseModel]]
) -> None:
    """
    Update forward references for given pydantic models.

    :param __all__: model names for updating
    :param __models__: all models
    :return: :class:`None`
    """

    for __entity_name__ in __all__:
        __entity__: Optional[Union[Any, BaseModel]] = __models__.get(__entity_name__, None)

        if hasattr(__entity__, UPDATE_FORWARD_REFS):
            __update_forwards_refs__: Callable[..., Any] = getattr(__entity__, UPDATE_FORWARD_REFS)
            __update_forwards_refs__(
                **{k: v for k, v in __models__.items() if k in __all__},
                **{"Optional": Optional},
            )
