from django import forms

from .models import (
    Department,
    RequestType,
    Ticket,
    TicketComment
)


class TicketForm(forms.ModelForm):
    attachment = forms.FileField(
        widget=forms.FileInput(),
        required=False
    )


    class Meta:

        model = Ticket

        fields = [
            'title',
            'department',
            'request_type',
            'other_request',
            'remarks'
        ]


        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a clear, concise subject'
                }
            ),

            'department': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'id_department'
                }
            ),

            'request_type': forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'id_request_type'
                }
            ),

            'other_request': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Specify your request'
                }
            ),

            'remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Provide detailed information about your issue...'
                }
            ),
        }


    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )


        self.fields[
            'department'
        ].queryset = Department.objects.filter(
            is_active=True
        )


        self.fields[
            'request_type'
        ].queryset = RequestType.objects.none()


        department_id = (
            self.data.get('department')
            if self.is_bound
            else (
                self.instance.department_id
                if self.instance.pk
                else None
            )
        )


        if department_id:

            self.fields[
                'request_type'
            ].queryset = RequestType.objects.filter(
                department_id=department_id,
                is_active=True
            )


    def clean(self):

        cleaned = super().clean()


        department = cleaned.get(
            'department'
        )

        request_type = cleaned.get(
            'request_type'
        )


        if (
            department
            and request_type
            and request_type.department_id != department.id
        ):

            self.add_error(
                'request_type',
                'Select a request belonging to the chosen department.'
            )


        if (
            request_type
            and request_type.name.lower() == 'other'
            and not cleaned.get(
                'other_request',
                ''
            ).strip()
        ):

            self.add_error(
                'other_request',
                'Please specify the other request.'
            )


        return cleaned


class TicketCommentForm(forms.ModelForm):

    class Meta:

        model = TicketComment

        fields = [
            'comment'
        ]


        widgets = {

            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Write your comment here...'
                }
            )
        }