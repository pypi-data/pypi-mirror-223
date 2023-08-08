# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet RA.230",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_accountant_general_audit",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "data/accountant_general_audit_worksheet_type_data.xml",
        "data/accountant_general_audit_worksheet_conclusion_data.xml",
        "views/accountant_general_audit_standard_detail_views.xml",
        "views/ws_ra230_views.xml",
        # "views/ws_ra210_account_inherent_risk_views.xml",
    ],
    "demo": [],
}
