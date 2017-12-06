from django import forms


class LotteryForm(forms.Form):
    no1 = forms.IntegerField(label='first field', max_value=38, min_value=1)
    no2 = forms.IntegerField(label='first field', max_value=38, min_value=1)
    no3 = forms.IntegerField(label='first field', max_value=38, min_value=1)
    no4 = forms.IntegerField(label='first field', max_value=38, min_value=1)
    no5 = forms.IntegerField(label='first field', max_value=38, min_value=1)
    no6 = forms.IntegerField(label='first field', max_value=38, min_value=1)
    no7 = forms.IntegerField(label='secand field', max_value=8, min_value=1)

    def clean(self):
        cleaned_data = super(LotteryForm, self).clean()

        datalist = []
        for data in list(cleaned_data):
            if data == 'no7':
                continue
            if cleaned_data[data] not in datalist:
                datalist.append(cleaned_data[data])
            else:
                msg = "Do not choose a duplicate number."
                self.add_error(data, msg)
