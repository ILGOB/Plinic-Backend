from rest_framework import permissions


class PostPermission(permissions.BasePermission):

    # 기본적으로 게시물을 조회/수정/삭제/생성하려면 로그인은 기본
    def has_permission(self, request, view):
        return request.user.is_authenticated

    # object 를 직접 다루려면, 유저가 로그인된 상태이거나, 스태프이거나, 슈퍼유저여야 한다.
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            or request.user.is_staff
            or request.user.is_superuser
        )
