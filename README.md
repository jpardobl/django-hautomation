django-hautomation
==================

REST API to control home automation deployments coded as Django apps


Django Home Automation is a set of Django apps which provides a REST API meant to
control home automation devices. It also provides a modular framework for
developing home automation drivers to enable more protocolos to be drived by this project.

The application by it self wont be enable to manage any home automation protocol
You need to install any protocol module to do this.

For example you can use https://github.com/jpardobl/hautomation_x10 to
manage X10 devices.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Create a django project, and cd into it.

2. Configure your database.

3. Add "hacore" and "harest" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'hacore',
	  'harest',
      )

4. Include the polls URLconf in your project urls.py like this::

	    url(r'rest/', include('harest.urls'))

5. Run `python manage.py syncdb` to create the homeautomation models.

6. Install any protocol module. For instance https://github.com/jpardobl/hautomation_x10

7. Initialize environ variable as follows:

  $ export DJANGO_SETTINGS_MODULE="<project_name>.settings"

8. exec script: populate_x10_db this fills the db with the info about X10 protocol

9. Start server:

  $ python manage.py runserver
