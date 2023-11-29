from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from .forms import LoginForm, RegisterForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
# 회원가입 비밀번호 조건 안맞을 시 표시
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponse
from django.shortcuts import render, redirect


# 회원정보 변경
def profile_edit_view(request):
    if request.method == 'POST':
        user_change_form = UserChangeForm(request.POST, instance=request.user)

        if user_change_form.is_valid():
            if user_change_form.has_changed():
                user_change_form.save()
                messages.success(request, '회원정보가 수정되었습니다.')
            else:
                messages.info(request, '수정 반영되지 않았습니다.')
            return render(request, 'users/profile_edit.html')
        else:
            messages.error(request, '폼 데이터가 유효하지 않습니다. 다시 확인해주세요.')
    else:
        user_change_form = UserChangeForm(instance=request.user)

    return render(request, 'users/profile_edit.html', {'user_change_form': user_change_form})


# 비밀번호 변경
@login_required
def password_edit_view(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('Information_Modification')
    else:
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'users/profile_password.html', {'password_change_form': password_change_form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        confirmation = request.POST.get('confirmation')
        withdrawal_button_value = request.POST.get('withdrawal_Button')  # 버튼의 입력값 받아오기
        if confirmation == '회원탈퇴':
            request.user.delete()  # 회원 삭제
            logout(request)  # 로그아웃 처리
        else:
            return HttpResponse(f'탈퇴 요청이 잘못되었습니다. <br>"{withdrawal_button_value}"로 입력함<br>')
    return HttpResponse('삭제되었습니다.')


def sign_in(request):
    if request.method == "GET":
        form = LoginForm()  # LoginForm 인스턴스 생성
        return render(request, 'users/login.html', {'form': form})

    elif request.method == "POST":
        form = LoginForm(request.POST)  # POST 요청 데이터를 사용하여 LoginForm 인스턴스 생성
        if form.is_valid():  # 폼이 유효한지 확인
            username = form.cleaned_data['username']  # 폼에서 사용자명 추출
            password = form.cleaned_data['password']  # 폼에서 비밀번호 추출
            user = authenticate(request, username=username, password=password)  # 사용자 인증 시도
            if user:
                login(request, user)  # 인증된 유저를 로그인시키기 위해 login() 함수 사용
                messages.success(request, f"안녕하세요, {username}님. 환영합니다!")
                return redirect('index')  # 로그인 성공 시 리다이렉트
        messages.error(request, f"유효하지 않은 아이디 또는 비밀번호입니다.")
        return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # 로그아웃 후 로그인 페이지로 리디렉션


def register(request):
    if request.method == "GET":
        form = RegisterForm()  # RegisterForm 인스턴스 생성
        return render(request, 'users/register.html', {'form': form})

    elif request.method == "POST":
        form = RegisterForm(request.POST)  # POST 요청 데이터를 사용하여 RegisterForm 인스턴스 생성
        if form.is_valid():  # 폼이 유효한지 확인
            user = form.save(commit=False)  # 폼을 기반으로 User 모델 인스턴스 생성 (아직 저장하지 않음)
            user.username = user.username.lower()  # 사용자명을 소문자로 변환하여 저장
            # 비밀번호 검증 추가
            password = form.cleaned_data.get('password1')
            from django.core.exceptions import ValidationError
            try:
                validate_password(password, user=user)
            except ValidationError as error:
                form.add_error('password1', error)
                return render(request, 'users/register.html', {'form': form})
            user.set_password(password)
            #
            user.save()  # 사용자 정보 저장
            messages.success(request, f"Signup Success")
            return redirect('login')  # 회원가입 성공 시 로그인 페이지로 리다이렉트
        messages.error(request, f"Signup 실패")
        return render(request, 'users/register.html', {'form': form})

# 20231123 아이디 찾기 화면 수정
def search_id(request):
    id_found = False  # 아이디를 찾았는지 여부를 나타내는 변수 초기화
    found_id = ""  # 찾은 아이디를 저장하는 변수 초기화
    if request.method == "POST":  # POST 요청인 경우에만 처리
        email = request.POST.get('email')  # POST 데이터에서 이메일 추출
        try:
            user = User.objects.get(email=email)  # 이메일로 사용자 검색
            id_found = True  # 아이디를 찾았음을 표시
            found_id = user.username  # 찾은 사용자의 아이디 저장
            messages.success(request, f"{email}로 등록된 아이디를 찾았습니다.")  # 성공 메시지 추가
        except User.DoesNotExist:  # 해당 이메일의 사용자가 없는 경우
            messages.error(request, f"입력한 이메일로 등록된 사용자가 없습니다.")  # 에러 메시지 추가
    return render(request, 'users/search_id.html', {'id_found': id_found, 'found_id': found_id})

# def search_id(request):
#     id_found = False  # 아이디를 찾았는지 여부를 나타내는 변수 초기화
#     found_id = ""  # 찾은 아이디를 저장하는 변수 초기화
#     if request.method == "POST":  # POST 요청인 경우에만 처리
#         first_name = request.POST.get('first_name')  # POST 데이터에서 이름 추출
#         last_name = request.POST.get('last_name')  # POST 데이터에서 성 추출
#         try:
#             user = User.objects.get(first_name=first_name, last_name=last_name)  # 이름과 성으로 사용자 검색
#             id_found = True  # 아이디를 찾았음을 표시
#             found_id = user.username  # 찾은 사용자의 아이디 저장
#             messages.success(request, f"{first_name + last_name}님의 아이디를 찾았습니다.")  # 성공 메시지 추가
#         except User.DoesNotExist:  # 해당 조건의 사용자가 없는 경우
#             messages.error(request, f"입력한 이름과 성에 해당하는 사용자가 없습니다.")  # 에러 메시지 추가
#     return render(request, 'users/search_id.html', {'id_found': id_found, 'found_id': found_id})

# 20231127 수정
# 비밀번호 재설정 뷰(비밀번호 찾기 화면 누르면 아이디와 이메일 넣고 해당 아이디와 이메일 맞으면 비밀번호 재설정으로 넘어감)
def find_password(request):
    password_found = False
    password_changed = False

    if request.method == "POST" and request.POST.get('new_password'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('new_password_confirm')  # 수정: 입력 필드 이름 수정
            return check_user_and_reset_password(request, user, new_password, confirm_password)
        except User.DoesNotExist:
            messages.error(request, f"해당 이름 또는 이메일로 된 사용자가 없습니다!")
    elif request.method == "POST":
        return check_user(request)
    # 20231128 팜업 메시지때문에 수정
    return render(request, 'users/find_password.html',
                  {'password_found': False, 'password_changed': password_changed, 'password_mismatch': False})

    #return render(request, 'users/find_password.html', {'password_found': password_found, 'password_changed': password_changed})

# def find_password(request):
#     if request.method == "POST" and request.POST.get('new_password'):
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         try:
#             user = User.objects.get(username=username, email=email)
#             new_password = request.POST.get('new_password')
#             return check_user_and_reset_password(request, user, new_password)
#         except User.DoesNotExist:
#             messages.error(request, f"해당 이름 또는 이메일로 된 사용자가 없습니다.")
#     elif request.method == "POST":
#         return check_user(request)
#     return render(request, 'users/find_password.html', {'password_found': False})

# 사용자 검증과 비밀번호 재설정 함수
def check_user_and_reset_password(request, user, new_password, confirm_password):
    if new_password == confirm_password:
        form = SetPasswordForm(user, {'new_password1': new_password, 'new_password2': confirm_password})
        if form.is_valid():
            form.save()
            logout(request)
            user = authenticate(request, username=user.username, password=new_password)
            if user:
                login(request, user)
                messages.success(request, f"비밀번호가 성공적으로 변경되었습니다. 로그인 되었습니다.")
                return render(request, 'users/find_password.html', {'password_found': True, 'password_changed': True})  # 수정: 비밀번호 변경 완료 시 플래그 변경
            else:
                messages.error(request, f"비밀번호 변경 후 로그인 중 오류가 발생했습니다.")
                return redirect('login')
        else:
            messages.error(request, f"비밀번호 변경 중 오류가 발생했습니다.")
            return redirect('find_password')
    # 20231128 팜업 메시지때문에 수정
    else:
        messages.error(request, f"입력한 비밀번호가 일치하지 않습니다!")
        return render(request, 'users/find_password.html', {'password_found': False, 'password_mismatch': True})
    # else:
    #     messages.error(request, f"입력한 비밀번호가 일치하지 않습니다!")
    #     return redirect('find_password')

# def check_user_and_reset_password(request, user, new_password):
#     form = SetPasswordForm(user, {'new_password1': new_password, 'new_password2': new_password})
#     if form.is_valid():
#         form.save()
#         logout(request)
#         user = authenticate(request, username=user.username, password=new_password)
#         if user:
#             login(request, user)
#             messages.success(request, f"비밀번호가 성공적으로 변경되었습니다. 다시 로그인해주세요.")
#             return redirect('login')
#         else:
#             messages.error(request, f"비밀번호 변경 후 로그인 중 오류가 발생했습니다.")
#             return redirect('login')
#     else:
#         messages.error(request, f"비밀번호 변경 중 오류가 발생했습니다.")
#         return redirect('find_password')


# 사용자 검증 함수
# 20231128 사용자가 존재하지 않을 때 메시지를 추가 히려고 수정
def check_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            return render(request, 'users/find_password.html', {'password_found': True, 'user': user})
        except User.DoesNotExist:
            messages.error(request, f"해당 이름 또는 이메일로 된 사용자가 없습니다!")  # 수정: 사용자 정보가 없을 때 메시지 추가
            return render(request, 'users/find_password.html', {'password_found': False, 'user': None, 'user_not_found': True})
    return render(request, 'users/find_password.html', {'password_found': False})

# def check_user(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         try:
#             user = User.objects.get(username=username, email=email)
#             return render(request, 'users/find_password.html', {'password_found': True, 'user': user})
#         except User.DoesNotExist:
#             messages.error(request, f"해당 이름 또는 이메일로 된 사용자가 없습니다.")
#     return render(request, 'users/find_password.html', {'password_found': False})

# # 20231124 비밀번호 초기화후 변경 코드 추가
# from .forms import ResetPasswordForm
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password
#
# def reset_password(request):
#     form = ResetPasswordForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
#             new_password = form.cleaned_data.get('new_password')
#             confirm_new_password = form.cleaned_data.get('confirm_new_password')
#             try:
#                 user = User.objects.get(username=username, email=email)
#                 if new_password == confirm_new_password:
#                     user.password = make_password(new_password)
#                     user.save()
#                     # messages.success(request, "비밀번호가 성공적으로 변경되었습니다. 다시 로그인해주세요.")
#                     logout(request)  # 로그아웃
#                     return redirect('login')  # 로그인 화면으로 이동
#                     # return render(request, 'users/find_password.html', {'password_changed': True})
#                 else:
#                     messages.error(request, "새 비밀번호가 일치하지 않습니다!")
#             except User.DoesNotExist:
#                 messages.error(request, f"해당 아이디 또는 이메일로 된 사용자가 없습니다!")
#     return render(request, 'users/find_password.html', {'form': form, 'password_changed': False})


def index(request):
    return render(request, 'users/index.html')

def Information_Modification(request):
    return render(request, 'users/Information_Modification.html')


def Withdrawal(request):
    return render(request, 'users/Withdrawal.html')


def profile_edit(request):
    return render(request, 'users/profile_edit.html')

# # 20231128 프로필 메인화면
from django.shortcuts import render
from .models import Profile

def profile_view(request):
    user = request.user
    user_posts = user.post_set.all()[:5]  # 최근 작성한 5개의 글 가져오기

    profile = Profile.objects.get(user=user)  # 사용자 프로필 정보 가져오기

    return render(request, 'Information_Modification.html', {'user': user, 'user_posts': user_posts, 'profile': profile})

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Profile

def Information_Modification(request):
    try:
        user_profile = Profile.objects.get(user=request.user)

        if request.method == 'POST':
            if 'profile_picture' in request.FILES:  # 파일이 업로드되었는지 확인
                profile_picture = request.FILES['profile_picture']
                # 프로필 이미지를 업로드하고 프로필 객체에 연결
                user_profile.profile_picture = profile_picture
                user_profile.save()
                messages.success(request, "프로필 이미지가 업데이트되었습니다.")

                # 업데이트된 프로필 정보를 다시 가져옵니다
                user_profile = Profile.objects.get(user=request.user)
                return render(request, 'users/Information_Modification.html', {'user_profile': user_profile})

        return render(request, 'users/Information_Modification.html', {'user_profile': user_profile})
    except Profile.DoesNotExist:
        messages.error(request, "프로필 정보를 찾을 수 없습니다.")
        return render(request, 'users/Information_Modification.html', {})


from django.http import JsonResponse

def upload_profile_picture(request):
    if request.method == 'POST':
        profile_picture = request.FILES['profile_picture']
        # 사용자의 프로필 객체 가져오기
        profile, created = Profile.objects.get_or_create(user=request.user)
        # 프로필 사진 업데이트 또는 저장
        profile.profile_picture = profile_picture
        profile.save()

        # 새 이미지 URL 가져오기
        new_image_url = profile.profile_picture.url

        # 새 이미지 URL을 JSON 형태로 반환
        return JsonResponse({'profile_picture_url': new_image_url})
    # POST 요청이 아닐 경우 다른 처리
    # ...

from django.http import HttpResponseRedirect
from django.urls import reverse

# def upload_profile_picture(request):
#     if request.method == 'POST':
#         profile_picture = request.FILES['profile_picture']
#         # 사용자의 프로필 객체 가져오기
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         # 프로필 사진 업데이트 또는 저장
#         profile.profile_picture = profile_picture
#         profile.save()
#
#         # 새 이미지 URL 가져오기
#         new_image_url = profile.profile_picture.url
#
#         # Information_Modification 페이지로 리디렉션하면서 이미지 URL을 전달합니다.
#         return redirect('Information_Modification')
#     # POST 요청이 아닐 경우 다른 처리
#     # ...


