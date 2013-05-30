from django.conf.urls import patterns, include, url
import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sakara.views.home', name='home'),
    # url(r'^sakara/', include('sakara.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.LoginView.as_view()),
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^home/$', views.HomeView.as_view()),
    url(r'^client/$', views.ClientView.as_view()),
    url(r'^client/(?P<id>[0-9]+)/edit/$', views.AddClientView.as_view()),
    url(r'^client/add/$', views.AddClientView.as_view())
)
