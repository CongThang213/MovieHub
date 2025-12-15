from enum import Enum


class PromotionType(str, Enum):
    DISCOUNT = "discount"
    FEATURED = "featured"
    PREMIERE = "premiere"
    SPECIAL_EVENT = "special_event"
