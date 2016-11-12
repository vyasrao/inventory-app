from django.conf.urls import include, url
import inventory

urlpatterns = [
    url(r'^inventory/', include('inventory.urls')),
    url(r'^$',inventory.views.index, name='index'),

    url(r'^products/(?P<user_id>[\w-]+)/$', inventory.Views.ProductsView.products, name='products'),
    url(r'^add_product', inventory.Views.ProductsView.add_product, name='add_product'),
    url(r'^edit_product', inventory.Views.ProductsView.edit_product, name='edit_product'),
    url(r'^delete_product', inventory.Views.ProductsView.delete_product, name='delete_product'),

    url(r'^variants/(?P<user_id>[\w-]+)/(?P<product_id>[\w-]+)/$', inventory.Views.VariantsView.variants, name='variants'),
    url(r'^add_variant', inventory.Views.VariantsView.add_variant, name='add_variant'),
    url(r'^edit_variant', inventory.Views.VariantsView.edit_variant, name='edit_variant'),
    url(r'^delete_variant', inventory.Views.VariantsView.delete_variant, name='delete_variant'),

    url(r'^notifications/(?P<user_id>[\w-]+)/$', inventory.Views.NotificationsView.notifications, name='notifications'),
    url(r'^clear_notify/(?P<user_id>[\w-]+)/$', inventory.Views.NotificationsView.clear_notify, name='clear_notify'),
]
