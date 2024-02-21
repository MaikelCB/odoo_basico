# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import os


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Exemplo de odoo basico'
    _sql_constraints = [('nomeUnico', 'unique(name)', 'Non se pode repetir o nome')]
    _order = "descripcion desc"

    name = fields.Char(required=True, size=20, string="Titulo")
    descripcion = fields.Text(string="A Descripción:")
    alto_en_cms = fields.Integer(string="Alto (cm)")
    longo_en_cms = fields.Integer(string="Longo (cm)")
    ancho_en_cms = fields.Integer(string="Ancho (cm)")
    volume = fields.Float(digits=(6, 7), compute="_volume", store=True, string="Volume (m³)")
    literal = fields.Char(store=False)
    peso = fields.Float(digits=(6, 2), default=2.7, string="Peso (Kg)")
    densidade = fields.Float(compute="_densidade", store=True, string="Densidade (Kg/ m³)")
    sexo_traducido = fields.Selection([("Hombre", "Home"), ("Mujer", "Muller"), ("Otros", "Outros")], string="Sexo")
    autorizado = fields.Boolean(default=False, string="¿Autorizado?")
    foto = fields.Binary(string='Foto')
    adxunto_nome = fields.Char(string="Nome Adxunto")
    adxunto = fields.Binary(string="Arquivo adxunto")
    # Os campos Many2one crean un campo na BD
    moeda_id = fields.Many2one('res.currency', domain="[('position','=','after')]")
    # con domain, filtramos os valores mostrados. Pode ser mediante unha constante (vai entre comillas) ou unha variable
    moeda_euro_id = fields.Many2one('res.currency',
                                    default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")],
                                                                                         limit=1))
    gasto_en_euros = fields.Monetary("Gasto en Euros", 'moeda_euro_id')
    moeda_en_texto = fields.Char(related="moeda_id.currency_unit_label",
                                 string="Moeda en formato texto", store=True)
    creador_da_moeda = fields.Char(related="moeda_id.create_uid.login",
                                   string="Usuario creador da moeda", store=True)

    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = (float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(
                rexistro.ancho_en_cms)) / 1000000

    @api.depends('volume', 'peso')
    def _densidade(self):
        for rexistro in self:
            if rexistro.volume != 0:
                rexistro.densidade = float(rexistro.peso) / float(rexistro.volume)
            else:
                rexistro.densidade = 0

    @api.onchange('alto_en_cms')
    def _avisoAlto(self):
        for rexistro in self:
            if rexistro.alto_en_cms > 7:
                rexistro.literal = 'O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto_en_cms
            else:
                rexistro.literal = ""

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):  # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 4:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)

    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"

    def envio_email(self):
        meu_usuario = self.env.user
        # mail_de     Odoo pon o email que configuramos en gmail para facer o envio
        mail_reply_to = meu_usuario.partner_id.email  # o enderezo email que ten asociado o noso usuario
        mail_para = 'braisiessg@gmail.com'  # o enderezo email de destino
        mail_valores = {
            'subject': 'Aquí iría o asunto do email ',
            'author_id': meu_usuario.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': 'Aquí iría o corpo do email cos datos por exemplo de "%s" ' % self.descripcion,
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.sudo().send()
        return True

    ''' 
    def ver_contexto(self):  # Este método é chamado dende un botón de informacion.xml
        for rexistro in self:
            # Ao usar warning temos que importar a libreria mediante from odoo.exceptions import Warning
            # Importamos tamén a libreria os mediante import os
            raise Warning(
                'Contexto: %s Ruta: %s Contido %s' % (rexistro.env.context, os.getcwd(), os.listdir(os.getcwd())))
            # env.context é un diccionario  https://www.w3schools.com/python/python_dictionaries.asp
        return True
    '''

    def ver_contexto(self):  # Este método é chamado dende un botón de informacion.xml
        for rexistro in self:
            # Ao usar warning temos que importar a libreria mediante from odoo.exceptions import Warning
            # Importamos tamén a libreria os mediante import os
            # raise Warning('Contexto: %s Ruta: %s Contido do directorio %s' % (rexistro.env.context, os.getcwd(), os.listdir(os.getcwd())))

            # Warning is deprecated por iso usamos ValidationError

            raise ValidationError('Contexto: %s Ruta: %s Contido do directorio %s' % (
                rexistro.env.context, os.getcwd(), os.listdir(os.getcwd())))
            # env.context é un diccionario  https://www.w3schools.com/python/python_dictionaries.asp
        return True
