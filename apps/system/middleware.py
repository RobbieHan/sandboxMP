import re

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import render


class MenuCollection(MiddlewareMixin):

    def get_user(self, request):
        return request.user

    def get_menu_from_role(self, request, user=None):
        if user is None:
            user = self.get_user(request)
        try:
            menus = user.roles.values(
                'permissions__id',
                'permissions__name',
                'permissions__url',
                'permissions__icon',
                'permissions__code',
                'permissions__parent'
            ).distinct()
            return [menu for menu in menus if menu['permissions__id'] is not None]
        except AttributeError:
            return None

    def get_permission_url(self, request):
        role_menus = self.get_menu_from_role(request)
        if role_menus is not None:
            permission_url_list = [menu['permissions__url'] for menu in role_menus]
            return permission_url_list

    def get_permission_menu(self, request):
        permission_menu_list = []
        role_menus = self.get_menu_from_role(request)
        if role_menus is not None:
            for item in role_menus:
                menu = {
                    'id': item['permissions__id'],
                    'name': item['permissions__name'],
                    'url': item['permissions__url'],
                    'icon': item['permissions__icon'],
                    'code': item['permissions__code'],
                    'parent': item['permissions__parent'],
                    'status': False,
                    'sub_menu': [],
                }
                permission_menu_list.append(menu)
            return permission_menu_list

    def get_top_reveal_menu(self, request):
        top_menu = []
        permission_menu_dict = {}
        request_url = request.path_info
        permission_menu_list = self.get_permission_menu(request)
        if permission_menu_list is not None:
            for menu in permission_menu_list:

                url = menu['url']
                if url and re.match(url, request_url):
                    menu['status'] = True
                if menu['parent'] is None:
                    top_menu.insert(0, menu)
                permission_menu_dict[menu['id']] = menu

            menu_data = []
            for i in permission_menu_dict:
                if permission_menu_dict[i]['parent']:
                    pid = permission_menu_dict[i]['parent']
                    parent_menu = permission_menu_dict[pid]
                    parent_menu['sub_menu'].append(permission_menu_dict[i])
                else:
                    menu_data.append(permission_menu_dict[i])
            if [menu['sub_menu'] for menu in menu_data if menu['url'] in request_url]:
                reveal_menu = [menu['sub_menu'] for menu in menu_data if menu['url'] in request_url][0]
            else:
                reveal_menu = None
            return top_menu, reveal_menu

    def process_request(self, request):
        if self.get_top_reveal_menu(request):
            request.top_menu, request.reveal_menu = self.get_top_reveal_menu(request)
            request.permission_url_list = self.get_permission_url(request)


class RbacMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if hasattr(request, 'permission_url_list'):
            request_url = request.path_info
            permission_url = request.permission_url_list
            for url in settings.SAFE_URL:
                if re.match(url, request_url):
                    return None
            if request_url in permission_url:
                return None
            else:
                return render(request, 'page404.html')