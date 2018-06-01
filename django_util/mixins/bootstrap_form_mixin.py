class BootstrapFormMixin(object):
    """
    For use with Django forms.
    Sets class="form-control" on all form fields except checkboxes and radios,
    for which it applies class="form-check-input".

    See: https://getbootstrap.com/docs/4.1/components/forms/
    """
    def __init__(self, *args, **kwargs):
        super(BootstrapFormMixin, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            widget = self.fields[field_name].widget
            if hasattr(widget, 'input_type') and (widget.input_type == 'checkbox' or widget.input_type == 'radio'):
                widget.attrs.update({'class': 'form-check-input'})
            else:
                widget.attrs.update({'class': 'form-control'})
