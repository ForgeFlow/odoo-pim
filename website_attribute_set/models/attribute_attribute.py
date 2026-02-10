# Copyright 2025 Kencove (http://www.kencove.com).
# @author Mohamed Alkobrosli <malkobrosly@kencove.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class AttributeAttribute(models.Model):
    _inherit = "attribute.attribute"

    e_com_visibility = fields.Boolean(
        string="E-Commerce Visibility",
        default=False,
        help="""If selected, the attribute will be shown in e-commerce website app.""",
    )
    is_filter = fields.Boolean(
        default=False,
        help="""If selected, the attribute will be shown as a filter
         in e-commerce website app (and appear in search).""",
    )
    is_specification = fields.Boolean(
        default=False,
        help="""If selected, the attribute will be shown as specification
             in e-commerce website app product view.""",
    )

    @api.constrains("is_filter")
    def _check_is_filter(self):
        for rec in self:
            if rec.is_filter and not rec.e_com_visibility:
                raise ValidationError(
                    self.env._(
                        "Cannot use attribute as filter "
                        "if it doesn't have E-Commerce Visibility enabled."
                    )
                )

    @api.constrains("is_specification")
    def _check_is_specification(self):
        for rec in self:
            if rec.is_specification and not rec.e_com_visibility:
                raise ValidationError(
                    self.env._(
                        "Cannot use attribute as specification "
                        "if it doesn't have E-Commerce Visibility enabled."
                    )
                )

    @api.onchange("e_com_visibility")
    def onchange_e_com_visibility(self):
        for rec in self:
            if rec.e_com_visibility:
                rec.is_filter = True
                rec.is_specification = True
            else:
                rec.is_filter = False
                rec.is_specification = False

    @api.constrains("domain")
    def _validate_domain(self):
        """Validate that the domain input is a valid Odoo domain."""
        for record in self:
            if record.domain:
                try:
                    domain = safe_eval(record.domain)
                    if not isinstance(domain, list):
                        continue

                    if not domain:  # Empty domain is valid
                        continue

                    for i, element in enumerate(domain):
                        if isinstance(element, str) and element in ["|", "&", "!"]:
                            if i > 0:
                                prev_element = domain[i - 1]
                                if isinstance(prev_element, list | tuple):
                                    raise ValueError(
                                        f"'{element}' at pos {i} wrong position."
                                        f"Operators must precede exprs."
                                    )
                        elif isinstance(element, list | tuple):
                            if len(element) < 2 or len(element) > 3:
                                raise ValueError(
                                    f"Domain at pos {i}, need 2-3, got {len(element)}"
                                )
                            field, operator = element[0], element[1]
                            if not isinstance(field, str):
                                raise ValueError(
                                    f"Field at pos {i}, must be str, got {type(field)}"
                                )
                            if not isinstance(operator, str):
                                raise ValueError(
                                    f"Op at pos {i}, must be str, got {type(operator)}"
                                )
                        else:
                            raise ValueError(
                                f"Domain elem must be op/cond list, got {type(element)}"
                            )
                except (Exception, TypeError, ValueError) as e:
                    raise ValidationError(
                        self.env._("Invalid domain: %s", str(e))
                    ) from e
