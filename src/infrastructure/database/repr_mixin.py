class ReprMixin:
    def __repr__(self):
        try:
            # noinspection PyUnresolvedReferences
            attrs = ", ".join(
                f"{k}={getattr(self, k)!r}" for k in self.__mapper__.c.keys()
            )
            return f"<{self.__class__.__name__}({attrs})>"
        except Exception as e:
            return f"<{self.__class__.__name__}(error: {e})>"
