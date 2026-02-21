class AllFormMixin:
    def __init__(self, *args, **kwargs):
        super(AllFormMixin, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
