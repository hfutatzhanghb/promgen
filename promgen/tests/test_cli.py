# Copyright (c) 2019 LINE Corporation
# These sources are released under the terms of the MIT license: see LICENSE

from promgen import models
from promgen.tests import PromgenTest

from django.core import management
from django.core.management.base import CommandError


class CLITests(PromgenTest):
    def test_register_job(self):
        # Assert when project doesn't exist
        with self.assertRaises(CommandError):
            management.call_command("register-job", "missing-project", "example", 1234)

        # Create a Service and Project and then try adding our job
        shard = models.Shard.objects.create(name="TestShard")
        service = models.Service.objects.create(name="TestService")
        _ = models.Project.objects.create(name="TestProject", service=service, shard=shard)
        management.call_command("register-job", "TestProject", "example", 1234)

        # Ensure the jobs we expect exist
        self.assertCount(models.Exporter, 1)

        # Registering the same job again shouldn't change our count
        management.call_command("register-job", "TestProject", "example", 1234)
        self.assertCount(models.Exporter, 1)

        # But registering a new one will
        management.call_command("register-job", "TestProject", "example", 4321)
        self.assertCount(models.Exporter, 2)
