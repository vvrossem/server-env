# Copyright 2018 Camptocamp (https://www.camptocamp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

""" Models used for testing server_environment

Create models that will be used in tests.

"""

from odoo import fields, models


class ServerEnvTest(models.Model):
    _name = 'server.env.test'
    _description = 'Server Environment Test Model'

    name = fields.Char(required=True)
    # if the original field is required, it must not
    # be required anymore as we set it with config
    host = fields.Char(required=True)
    port = fields.Integer()
    user = fields.Char()
    password = fields.Char()
    ssl = fields.Boolean()

    # we'll use these ones to stress the custom
    # compute/inverse for the default value
    alias = fields.Char()
    alias_default = fields.Char()


# Intentionally re-declares a class to stress the inclusion of the mixin
class ServerEnvTestWithMixin(models.Model):
    _name = 'server.env.test'
    _inherit = ['server.env.test', 'server.env.mixin']

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        sftp_fields = {
            "host": {},
            "port": {},
            "user": {},
            "password": {},
            "ssl": {},
            "alias": {
                "no_default_field": True,
                "compute_default": "_compute_alias_default",
                "inverse_default": "_inverse_alias_default",
            }
        }
        sftp_fields.update(base_fields)
        return sftp_fields

    def _compute_alias_default(self):
        for record in self:
            record.alias = record.alias_default

    def _inverse_alias_default(self):
        for record in self:
            record.alias_default = record.alias
