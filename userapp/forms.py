from django import forms
from captcha.fields import CaptchaField


class Login_Form(forms.Form):
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs={'class':'form-control login-field',"placeholder":"输入用户名","id":"login-name" }))
    password = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control login-field',"placeholder":"输入密码"}))
    captcha = CaptchaField(label='验证码')

class Register_Form(forms.Form):
    gender = (
        ('male',"男"),
        ('female',"女")
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control login-field',"placeholder":"输入用户名"}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control login-field',"placeholder":"输入密码"}))
    re_password = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control login-field',"placeholder":"再次输入密码"}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control login-field',"placeholder":"输入邮箱"}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    phoneNO = forms.CharField(label="电话号码", max_length=256,widget=forms.TextInput(attrs={'class': 'form-control login-field',"placeholder":"输入手机号码"}))
    captcha = CaptchaField(label='验证码')