# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class lineapedido(models.Model):
    _name = 'odoo_basico.lineapedido'
    _description = 'Exemplo de Many2one'
    _sql_constraints = [('nomeUnico', 'unique(name)', 'Non se pode repetir o nome')]
    _order = "descripcion desc"

    name = fields.Char(required=True, size=20, string="Titulo")
    descripcion = fields.Text(string="A Descripción:")
    # Os campos Many2one crean un campo na BD
    pedido_id = fields.Many2one('odoo_basico.pedido',
                                ondelete="cascade", required=True)
    # Os campos Many2many crean unha táboa na BD
    informacion_ids = fields.Many2many("odoo_basico.informacion",
                                       string="Rexistro de Información",
                                       relation="odoo_basico_lineapedido_informacion",
                                       column1="lineapedido_id", column2="informacion_id")
