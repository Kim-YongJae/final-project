from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


#비밀번호 변경 폼 정의
class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })

# 내 정보 수정
class UserChangeForm(UserChangeForm):
    password = None
    last_name = forms.CharField(label='성', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength':'80', 'oninput':"maxLengthCheck(this)",}),
    )
    first_name = forms.CharField(label='이름', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength':'80', 'oninput':"maxLengthCheck(this)",}),
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']


# 사용자 로그인 폼 정의
# placeholder + 입력창 가로길이 꽉 채우기 20231201
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=65,
        widget=forms.TextInput(attrs={'placeholder': '아이디', 'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호', 'class': 'form-control'})
    )

# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'placeholder': '아이디'}))
#     password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))


# 사용자 회원가입 폼 정의
# placeholder + 가로길이 꽉 채우기 20231201
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '아이디'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '성'}))
    email = forms.CharField(max_length=30, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'}))
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'}))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호 확인'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

# class RegisterForm(UserCreationForm):
#     username = forms.CharField(max_length=30, label='아이디')
#     first_name = forms.CharField(max_length=30, label='이름')  # 이름 입력 필드
#     last_name = forms.CharField(max_length=30, label='성')   # 성 입력 필드
#     email = forms.CharField(max_length=30, label='이메일')
#     password1 = forms.CharField(max_length=30, label='비밀번호')
#     password2 = forms.CharField(max_length=30, label='비밀번호 확인')
#     # 20231127 수정
#     # nickname = forms.CharField(max_length=50, label='닉네임')  # 닉네임 입력 필드
#     # age = forms.IntegerField(label='나이')  # 나이 입력 필드
#     class Meta:
#         model = User  # 내장 User 모델을 사용
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
#         # 폼에서 사용할 필드들을 지정


# 20231124 비밀번호 찾기 화면에서 초기화랑 비밀번호 새로 변경
# class ResetPasswordForm(forms.Form):
#     username = forms.CharField(max_length=65, label='아이디')
#     email = forms.EmailField(label='이메일')
#     new_password = forms.CharField(max_length=65, widget=forms.PasswordInput, label='새 비밀번호')
#     confirm_new_password = forms.CharField(max_length=65, widget=forms.PasswordInput, label='새 비밀번호 확인')
#     # 새로운 비밀번호가 일치하는지 확인하는 코드인데 필요한가?
#     # def clean(self):
#     #     cleaned_data = super().clean()
#     #     new_password = cleaned_data.get('new_password')
#     #     confirm_new_password = cleaned_data.get('confirm_new_password')
#     #
#     #     if new_password and confirm_new_password and new_password != confirm_new_password:
#     #         raise forms.ValidationError("새 비밀번호가 일치하지 않습니다.")
#     #     return cleaned_data



# 20231128 프로필 메인화면
from django import forms
from .models import Profile

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']  # Profile 모델의 필드 이름을 여기에 정확하게 기입




