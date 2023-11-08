# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Exemplo de odoo basico'

    name = fields.Char(required=True, size=20, string="Titulo")
    description = fields.Text(string="A Descripción:")
    alto_en_cms = fields.Integer(string="Alto en centímetros")
    longo_en_cms = fields.Integer(string="Longo en centímetros")
    ancho_en_cms = fields.Integer(string="Ancho en centímetros")
    peso = fields.Float(digits=(6, 2), default=2.7, string="Peso en Kg")
    sexo = fields.Selection([("Hombre", "Hombre"), ("Mujer", "Mujer"), ("Otros", "Otros")], string="Sexo")
    autorizado = fields.Boolean(default=False, string="¿Autorizado?")
