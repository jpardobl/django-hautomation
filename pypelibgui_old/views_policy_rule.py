from pypelib.persistence.backends.django.RuleTableModel import PolicyRuleTableModel
from pypelib.persistence.backends.django.RuleModel import PolicyRuleModel
from pypelibgui.mappings import get_mappings
from pypelib.persistence.backends.django.Django import Django
from pypelibgui.forms import PolicyRuleForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


def rules_by_table(request, table_name):
    ruleset = PolicyRuleModel.objects.filter(RuleTableName=table_name).order_by('RulePosition')
    return render_to_response(
        'policy_rule_table/ruleset.html',
        {
        'ruleset': ruleset,
         },
        context_instance=RequestContext(request))


@csrf_exempt
def add_rule(request, table_name):
    print "tenemos los mappings %s" % get_mappings()
    print "recibimos el t name: %s" % table_name
    ruleset = Django.load(table_name, get_mappings(), None)

    print request.POST
    form = PolicyRuleForm(request.POST)

    if form.is_valid():
        ruleset = form.save(ruleset)

    return render_to_response(
        'policy_rule/edit.html',
        {
        'form': form,

         },
        context_instance=RequestContext(request))


@csrf_exempt
def del_rule(request, pk):
    get_object_or_404(PolicyRuleModel, pk=pk).delete()
    return HttpResponse("OK")
