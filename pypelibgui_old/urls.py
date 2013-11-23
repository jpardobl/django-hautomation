from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^rules_by_table/(\w+)?/?', "pypelibgui.views_policy_rule.rules_by_table", name="policy_rules_by_table"),
    url(r'^del_rule/(\d+)?/?', "pypelibgui.views_policy_rule.del_rule", name="policy_del_rule"),
    url(r'^add_rule/(\w+)?/?', "pypelibgui.views_policy_rule.add_rule", name="policy_add_rule"),


    url(r'^rule_table/(\w+)?/?', "pypelibgui.views_policy_rule_table.edit", name="policy_rule_table"),



)
