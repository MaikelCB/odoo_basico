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
