from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Sum

from .models import Collect, Payment, Reason

admin.site.empty_value_display = 'Не задано'
admin.site.site_header = 'Администрирование проекта "Group Donations"'
admin.site.site_title = 'Портал администраторов "Group Donations"'
admin.site.index_title = 'Добро пожаловать, на самый благотворительный сайт'

User = get_user_model()
LIMIT_POSTS_PER_PAGE = 10


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name',
        'amount',
        'created_at',
        'comments',
    )
    fields = (
        (
            'user',
            'amount',
            'collect',
        ),
        ('comments',),
    )
    search_fields = (
        'user',
        'amount',
        'collect',
    )
    list_filter = (
        'user',
        'amount',
        'collect',
    )
    list_per_page = LIMIT_POSTS_PER_PAGE

    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    get_full_name.short_description = 'Владелец платежа'
    get_full_name.admin_order_field = 'user__first_name'


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_full_name',
        'pub_date',
        'get_collect_amount',
        'get_payments_count',
    )
    fields = (
        (
            'name',
            'planned_amount',
            'end_date',
        ),
        ('description',),
        (
            'author',
            'reason',
        ),
        ('cover_image',),
    )
    search_fields = (
        'name',
        'author',
        'end_date',
        'reason__name',
    )
    list_filter = (
        'name',
        'author',
        'end_date',
        'reason__name',
    )
    list_per_page = LIMIT_POSTS_PER_PAGE

    def get_payments_count(self, obj):
        return obj.payments.count()

    get_payments_count.short_description = 'Число платежей'

    def get_collect_amount(self, obj):
        return obj.payments.annotate(Sum('amount'))

    get_collect_amount.short_description = 'Собранная сумма'

    def get_full_name(self, obj):
        return f'{obj.author.first_name} {obj.author.last_name}'

    get_full_name.short_description = 'Владелец сборов'
    get_full_name.admin_order_field = 'author__first_name'


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = ('name',)
    search_fields = (
        'name',
        'slug',
    )
    list_editable = (
        'color',
        'slug',
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'surname',
        'username',
        'email',
    )
    list_editable = (
        'first_name',
        'last_name',
        'surname',
    )
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        'email',
        'username',
        'last_name',
    )
    list_display_links = (
        'username',
        'email',
    )
    list_per_page = LIMIT_POSTS_PER_PAGE
