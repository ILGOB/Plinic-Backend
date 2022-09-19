from rest_framework import permissions


class PostPermission(permissions.BasePermission):
    """
    게시물 삭제, 수정 시 비밀번호 검증, 비밀번호가 일치하지 않을 시 403 상태 코드와 에러 메시지 반환
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated or request.user.is_staff or request.user.is_superuser
