from pypelib.persistence.backends.django.RuleTableModel import PolicyRuleTableModel
from pypelib.persistence.backends.django.RuleModel import PolicyRuleModel
from django.forms import ModelForm
from django.forms.widgets import TextInput


class PolicyRuleTableForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PolicyRuleTableForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget = TextInput()

    class Meta:
        model = PolicyRuleTableModel
        fields = ("uuid", "name", "type", )


class PolicyRuleForm(ModelForm):

    def save(self, ruleset, *args, **kwargs):
        obj = super(PolicyRuleForm, self).save(commit=False)
        pos = len(ruleset.getRuleSet()) + 1
        print obj
        print "llega la rule: %s" % obj.Rule
        print "lo ponemos en la posicion: %s" % pos
        ruleset.addRule(
            obj.Rule,
            obj.RuleIsEnabled,
            pos,
            None,
            "Django")
        ruleset.save("Django")
        return ruleset

    class Meta:
        model = PolicyRuleModel
        fields = ("Rule", "RuleIsEnabled")
