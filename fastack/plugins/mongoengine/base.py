from datetime import datetime

from mongoengine import Document, fields


class Model(Document):
    date_created = fields.DateTimeField(default=datetime.now)
    date_updated = fields.DateTimeField()
    meta = {"abstract": True}

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save(force_insert=True)
        return obj

    def update(self, **kwargs):
        kwargs["date_updated"] = datetime.utcnow()
        for k, v in kwargs.items():
            setattr(self, k, v)

        return super().update(**kwargs)

    def save(
        self,
        force_insert=False,
        validate=True,
        clean=True,
        write_concern=None,
        cascade=None,
        cascade_kwargs=None,
        _refs=None,
        save_condition=None,
        signal_kwargs=None,
        **kwargs
    ):
        self.date_updated = datetime.utcnow()
        return super().save(
            force_insert=force_insert,
            validate=validate,
            clean=clean,
            write_concern=write_concern,
            cascade=cascade,
            cascade_kwargs=cascade_kwargs,
            _refs=_refs,
            save_condition=save_condition,
            signal_kwargs=signal_kwargs,
            **kwargs
        )

    def serialize(self) -> dict:
        return {
            "id": str(self.pk),
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }
