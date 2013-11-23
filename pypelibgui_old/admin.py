from django.contrib import admin
from pypelib.persistence.backends.django.RuleModel import PolicyRuleModel
from pypelib.persistence.backends.django.RuleTableModel import PolicyRuleTableModel


class PolicyRuleModelAdmin(admin.ModelAdmin):
    pass
admin.site.register(PolicyRuleModel, PolicyRuleModelAdmin)


class PolicyRuleTableModelAdmin(admin.ModelAdmin):
    pass
admin.site.register(PolicyRuleTableModel, PolicyRuleTableModelAdmin)
