from django.test.runner import DiscoverRunner


class NoDbTestRunner(DiscoverRunner):
  """ Avoid de creation database test """

  def setup_databases(self, **kwargs):
    """ Override the database creation defined in parent class """
    pass

  def teardown_databases(self, old_config, **kwargs):
    """ Override the database teardown defined in parent class """
    pass
