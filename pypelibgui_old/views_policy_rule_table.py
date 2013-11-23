from pypelib.persistence.backends.django.RuleTableModel import PolicyRuleTableModel
from pypelib.persistence.backends.django.RuleModel import PolicyRuleModel
from pypelib.persistence.backends.django.Django import Django
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from pypelibgui.forms import PolicyRuleTableForm, PolicyRuleForm
from django.template import RequestContext
from django.contrib import messages

#from mappings import get_mappings
#from pypelib.RuleTable import RuleTable


def edit(request, name=None):
    if name is None:
        obj = PolicyRuleTableModel()
    #    rs_obj = None
    else:
        obj = PolicyRuleTableModel.objects.get(name=name)
      #  rs_obj = Django.load(name, get_mappings(), "")

    if request.method == "POST":
        form = PolicyRuleTableForm(request.POST, instance=obj)

        if form.is_valid():
            print "ESTAMOS EN VALID ************************"
            obj = form.save(commit=False)
            obj.type = False
            obj.defaultParser = "RegexParser"
            obj.save()
            print "OBJETO SALVADO **************************"

            messages.info(request, 'Rule table successfully saved')
            return redirect(reverse('policy_rule_table', args=[obj.name]))
        print "No hemos pasado el formulario OOOOOOOOOOOOOOOOOOOOOOO"
        messages.error(request, "Wrong fields!")

    else:
        form = PolicyRuleTableForm(initial=request.GET, instance=obj)

    return render_to_response(
            'policy_rule_table/edit.html',
            {
            'form': form,
             "id": obj.pk,
             "obj": obj,
             "ruleset": PolicyRuleModel.objects.filter(RuleTableName=obj.name).order_by('RulePosition'),
             "r_form": PolicyRuleForm(),
             },
            context_instance=RequestContext(request))
