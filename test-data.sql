INSERT INTO providertool.entities_attributeset
(attribute_set_id, attribute_set_name, attribute_set_code, created_at)
VALUES('735f6747f5b945acbe544de20c4b2cdb', 'Personal Info', 'client_personal_info', '2021-09-14 20:43:55.426');
INSERT INTO providertool.entities_attributeset
(attribute_set_id, attribute_set_name, attribute_set_code, created_at)
VALUES('8bcbb15d59064063ac9783ef7b3fb909', 'Client Interventions', 'casemanager_client_interventions', '2021-09-16 16:39:21.524');
INSERT INTO providertool.entities_attributeset
(attribute_set_id, attribute_set_name, attribute_set_code, created_at)
VALUES('a99d47f5168d4c099dc0d5e84e9dfa85', 'Client Assessment', 'casemanager_client_assessment', '2021-09-10 16:59:47.819');
INSERT INTO providertool.entities_attributeset
(attribute_set_id, attribute_set_name, attribute_set_code, created_at)
VALUES('b23d42fd97f14493a5cbb291268a38ea', 'Daily Workload', 'casemanager_daily_workload', '2021-09-10 16:59:35.004');



INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('0c51cc42d67442fa8ebb2b2c55dbba34', 0, 'daily_workload_research_related_activities', 'Research Related Activity', '2021-09-17 01:35:50.392', 'b23d42fd97f14493a5cbb291268a38ea', NULL, 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('0fab350fcbcc4245836fb06d7c760646', 0, 'client_assessment_existing_em_client_need_reassess', 'Existing Extra-Mural Client - Need to re-assess', '2021-09-17 02:56:30.656', 'a99d47f5168d4c099dc0d5e84e9dfa85', NULL, 1, 2000);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('461655a5f029451c87892409f59c712f', 0, 'dailyworkload_administration', 'Administration (e.g., protocol, process, meetings, etc.)', '2021-09-13 17:31:05.908', 'b23d42fd97f14493a5cbb291268a38ea', '7ecca6bdfc874d48a2a78b1dce7862fc', 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('4619f055a0c847cc84bbae357c17a6a4', 0, 'daily_workload_research_meetings', 'Research Meetings', '2021-09-17 01:36:43.439', 'b23d42fd97f14493a5cbb291268a38ea', '0c51cc42d67442fa8ebb2b2c55dbba34', 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('594146da66194973b1d731f151c1ce6c', 0, 'client_assessment_provider_specific_assessment_forms', 'Select Provider Specific Assessment Forms', '2021-09-17 03:00:25.243', 'a99d47f5168d4c099dc0d5e84e9dfa85', '0fab350fcbcc4245836fb06d7c760646', 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('5e08c7b457234153baa27f07c75984b6', 0, 'client_assessment_existing_em_select_assessment_forms', 'Select Assessment Forms', '2021-09-17 03:12:42.450', 'a99d47f5168d4c099dc0d5e84e9dfa85', '0fab350fcbcc4245836fb06d7c760646', 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('71d00ba5de9e444aaf199633ad9c8923', 0, 'daily_workload_research_administration', 'Administration (e.g., data gathering, sharing institutional documents, etc.)', '2021-09-17 01:37:14.868', 'b23d42fd97f14493a5cbb291268a38ea', '0c51cc42d67442fa8ebb2b2c55dbba34', 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('7ecca6bdfc874d48a2a78b1dce7862fc', 0, 'dailyworkload_clinical_activities', 'Project Related Clinical Activities', '2021-09-13 17:30:01.493', 'b23d42fd97f14493a5cbb291268a38ea', NULL, 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('8ed9c06ca5f24c448f228e375d6aa904', 0, 'dailyworkload_caseload', 'Client Daily Caseload', '2021-09-13 17:28:57.034', 'b23d42fd97f14493a5cbb291268a38ea', NULL, 0, 1000);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('aa3317f4faaf41858c4681b40a0acbe3', 0, 'client_assessment_new_em_client', 'New Extra-Mural Client', '2021-09-17 02:56:54.134', 'a99d47f5168d4c099dc0d5e84e9dfa85', NULL, 1, 3000);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('acf41cb9424044a0a251e4215d32cb8e', 0, 'dailyworkload_review_board', 'Case Management Review Board', '2021-09-13 17:30:34.123', 'b23d42fd97f14493a5cbb291268a38ea', '7ecca6bdfc874d48a2a78b1dce7862fc', 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('d0bfd7095d4742e3a9133cd72ed02635', 1, 'default_client_interventions', 'Details', '2021-09-17 12:38:26.706', '8bcbb15d59064063ac9783ef7b3fb909', NULL, 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('dc45eb5fb4a849fba6d16cdfc4a43065', 0, 'client_assessment_existing_em_client_no_reassess', 'Existing Extra-Mural Client - Need to re-assess', '2021-09-22 03:14:54.220', 'a99d47f5168d4c099dc0d5e84e9dfa85', NULL, 1, 2500);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('e01ad529ac2a4ee69f04d545c984b0b0', 0, 'client_assessment_client_status', 'Client Status', '2021-09-17 02:23:02.296', 'a99d47f5168d4c099dc0d5e84e9dfa85', 'f32412c6dd3849c0a20eba58ff810e41', 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('f2e4ce9fb4014a4fb7c802a816bcf1fc', 0, 'client_assessment_re_assessment', 'Client Re-Assessment', '2021-09-17 02:57:20.114', 'a99d47f5168d4c099dc0d5e84e9dfa85', NULL, 1, 100);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('f32412c6dd3849c0a20eba58ff810e41', 1, 'default__client_assessment', 'Details', '2021-09-13 17:13:04.633', 'a99d47f5168d4c099dc0d5e84e9dfa85', NULL, 0, NULL);
INSERT INTO providertool.entities_attributegroup
(attribute_group_id, is_default_group, attribute_group_code, attribute_group_name, created_at, attribute_set_id, parent_attribute_group_id, conditional_display, sort_order)
VALUES('f34ebd4e08894c848d147e97c6b7cf5b', 1, 'default__casemanager_daily_workload', 'Details', '2021-09-13 21:22:43.787', 'b23d42fd97f14493a5cbb291268a38ea', NULL, 0, NULL);





INSERT INTO providertool.entities_rolepermissions
(permission_id, operation_type, resource, role_id)
VALUES('10915e5fd6924d7bb7eff93937d6eee8', 'CREATE', '2e454e63aa894194a9fb507e2ff94a42', '43701c8201c7484e9aafc90901542216');
INSERT INTO providertool.entities_rolepermissions
(permission_id, operation_type, resource, role_id)
VALUES('badc0dee2c1c4e5795a7cf940a37d20f', 'CREATE', 'cbc8a7ab9e764a3eb4786fe8b419da23', '43701c8201c7484e9aafc90901542216');
INSERT INTO providertool.entities_rolepermissions
(permission_id, operation_type, resource, role_id)
VALUES('d4b84e1c2cbd40e9a424695e2ae27e60', 'CREATE', 'd90d44e8480a47489844e03ff6b03647', '43701c8201c7484e9aafc90901542216');
INSERT INTO providertool.entities_rolepermissions
(permission_id, operation_type, resource, role_id)
VALUES('aacb06f0d3034fc68162f8301d646f23', 'DELETE', '2e454e63aa894194a9fb507e2ff94a42', '43701c8201c7484e9aafc90901542216');
INSERT INTO providertool.entities_rolepermissions
(permission_id, operation_type, resource, role_id)
VALUES('e6a8ce26ce334354bf237eddb7c92451', 'EDIT', '2e454e63aa894194a9fb507e2ff94a42', '43701c8201c7484e9aafc90901542216');
INSERT INTO providertool.entities_rolepermissions
(permission_id, operation_type, resource, role_id)
VALUES('2aed8b460ea84ce483495ed0b756413a', 'EDIT', 'd90d44e8480a47489844e03ff6b03647', '43701c8201c7484e9aafc90901542216');
INSERT INTO providertool.entities_rolepermissions
(permission_id, operation_type, resource, role_id)
VALUES('ed77b855cc90481485948b304c86d2d2', 'VIEW', '2e454e63aa894194a9fb507e2ff94a42', '43701c8201c7484e9aafc90901542216');
INSERT INTO providertool.entities_rolepermissions
(permission_id, operation_type, resource, role_id)
VALUES('7664d8de737a44d5be0a91494a003c6e', 'CREATE', 'e254c5fdb0fb48528d78fd9c84a026d2', 'af80cac1389c4229aabf360f89939245');


INSERT INTO providertool.entities_roles
(role_id, role_code, role_label)
VALUES('43701c8201c7484e9aafc90901542216', 'role_casemanager', 'Case Manager');
INSERT INTO providertool.entities_roles
(role_id, role_code, role_label)
VALUES('af80cac1389c4229aabf360f89939245', 'role_casemanagement_client', 'Case Management Client');




INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('0783218ecd7b446388a68979825eeaa2', 'clinical_activities_review_board_time_spent', 'Total time spent', 'input_time', 'time', 1, 'Total time spent', 1, '2021-09-13 21:29:44.134', NULL, 'acf41cb9424044a0a251e4215d32cb8e', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('0d8998eae4ba46199dd2a9a515a0a345', 'dailyworkload_research_administration_timespent', 'Total Time Spent', 'input_time', 'time', 0, 'Total Time Spent', 1, '2021-09-17 01:39:10.552', NULL, '71d00ba5de9e444aaf199633ad9c8923', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('139d2433f7284df5ba60bd478e166c70', 'client_assessment_existing_em_select_assessment_forms_EMP_Intake', 'EMP Intake', 'input_file', 'file', 0, 'EMP Intake', 1, '2021-09-17 03:16:57.830', NULL, '5e08c7b457234153baa27f07c75984b6', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('19d3f87dd23a4aca82408560e3b83ea6', 'client_assessment_existing_em_select_assessment_forms_Safe_Use_of_Home_Oxygen_Patient', 'Safe Use of Home Oxygen Patient', 'input_file', 'file', 0, 'Safe Use of Home Oxygen Patient', 1, '2021-09-17 03:21:26.234', NULL, '5e08c7b457234153baa27f07c75984b6', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('19f8d089723c4d2a8e6022cbc98eacd3', 'client_assessment_providerspecificforms_Clinical_Nutrition_Assessment', 'Clinical Nutrition Assessment', 'input_file', 'file', 0, 'Clinical Nutrition Assessment - File', 1, '2021-09-17 03:04:19.980', NULL, '594146da66194973b1d731f151c1ce6c', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('274b0ade92954677944af065cee84201', 'dailyworkload_service_recipient_travel', 'Service Recipient Travel', 'input_time', 'time', 1, 'Service Recipient Travel', 1, '2021-09-13 21:21:55.340', NULL, 'f34ebd4e08894c848d147e97c6b7cf5b', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('2c7855fb275a471b9fed3b34bb2361e0', 'client_assessment_providerspecificforms_Nursing Assessment', 'Nursing Assessment', 'input_file', 'file', 0, 'Nursing Assessment', 1, '2021-09-17 03:04:47.744', NULL, '594146da66194973b1d731f151c1ce6c', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('3cc5d7d2c0fa481999d8dd34ac983657', 'client_assessment_providerspecificforms_', 'Social Work Assessment', 'input_file', 'file', 0, 'Social Work Assessment', 1, '2021-09-17 03:09:57.685', NULL, '594146da66194973b1d731f151c1ce6c', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('3f8edb2226824569a1d7fb67b7e69958', 'client_assessment_providerspecificforms_OccupationalTherapyAssessment', 'Occupational Therapy Assessment', 'input_file', 'file', 0, 'Occupational Therapy Assessment', 1, '2021-09-17 03:05:46.044', NULL, '594146da66194973b1d731f151c1ce6c', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('4021d3aae61d48729ee94e6ff9af1b08', 'client_assessment_existing_em_select_assessment_forms_Smoking_Cessation_Assessment', 'Smoking Cessation Assessment', 'input_file', 'file', 0, 'Smoking Cessation Assessment', 1, '2021-09-17 03:27:01.530', NULL, '5e08c7b457234153baa27f07c75984b6', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('4a2fefa75dcf43bbbf6faee896cc61dd', 'client_assessment_client_status', 'Client Status', 'input_radio', 'radio', 1, 'Client Status - New case management client or existing case management client.', 1, '2021-09-17 02:32:11.579', NULL, 'e01ad529ac2a4ee69f04d545c984b0b0', 3000);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('4d541fcb485f4c44a5f88acf779764e3', 'client_assessment_existing_em_select_assessment_forms_Safe_Workplace_Agreement', 'Safe Workplace Agreement', 'input_file', 'file', 0, 'Safe Workplace Agreement', 1, '2021-09-17 03:17:33.307', NULL, '5e08c7b457234153baa27f07c75984b6', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('5f219f4002674e2ca5500afcd7217432', 'clinical_activities_administration_time_spent', 'Total time spent', 'input_time', 'time', 1, 'Total time spent', 1, '2021-09-13 21:30:16.018', NULL, '461655a5f029451c87892409f59c712f', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('67bf97d5ae5a44778a549d1e06ac622d', 'dailyworkload_research_meetings_timespent', 'Total Time Spent', 'input_time', 'time', 0, 'Total Time Spent', 1, '2021-09-17 01:38:20.349', NULL, '4619f055a0c847cc84bbae357c17a6a4', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('79c3b348237349d894d2365c4163670d', 'client_assessment_existing_emp_client_date', 'Date', 'input_date', 'date', 1, 'Date', 1, '2021-09-17 02:59:08.496', NULL, '0fab350fcbcc4245836fb06d7c760646', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('8247ae6e5aa546c88694f1f270833283', 'client_assessment_existing_em_select_assessment_forms_EMP_Medication_Profile', 'EMP Medication Profile', 'input_file', 'file', 0, 'EMP Medication Profile', 1, '2021-09-17 03:20:43.715', NULL, '5e08c7b457234153baa27f07c75984b6', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('83a8288073ef4dcfbf7906755f30f0d4', 'dailyworkload_clinical_activities_other', 'Other', 'input_textbox', 'text', 1, 'Other', 1, '2021-09-13 21:31:31.812', NULL, '7ecca6bdfc874d48a2a78b1dce7862fc', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('843cf9e8e9b84bb9a394e30513975276', 'client_assessment_existing_em_select_assessment_forms_EMP_Progress_Notes', 'EMP Progress Notes', 'input_file', 'file', 0, 'EMP Progress Notes', 1, '2021-09-17 03:15:35.703', NULL, '5e08c7b457234153baa27f07c75984b6', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('855e1c6e018147de88827013ec451f6d', 'client_assessment_providerspecificforms_Respiratory_Assessment', 'Respiratory Assessment', 'input_file', 'file', 0, 'Respiratory Assessment', 1, '2021-09-17 03:09:01.111', NULL, '594146da66194973b1d731f151c1ce6c', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('9c5f3b0872204e25979f83bac979d4e7', 'client_assessment_existing_em_select_assessment_forms_Braden_Scale', 'Braden Scale', 'input_file', 'file', 0, 'Braden Scale', 1, '2021-09-17 03:19:12.288', NULL, '5e08c7b457234153baa27f07c75984b6', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('a5df4a90d95d4c0d97f8dc8b0754e760', 'client_assessment_existing_em_select_assessment_forms_Team_Communication', 'Team Communication', 'input_file', 'file', 0, 'Team Communication', 1, '2021-09-17 03:27:27.007', NULL, '5e08c7b457234153baa27f07c75984b6', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('b4c33d1cf9c34bdd80bdf5e90145fb8d', 'dailyworkload_date', 'Date', 'input_date', 'date', 1, 'Daily workload date', 1, '2021-09-16 00:17:22.703', NULL, 'f34ebd4e08894c848d147e97c6b7cf5b', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('c49a516384b84eaebf064f6b87a3f552', 'client_assessment_existing_em_select_assessment_forms_Risk_of_Falls_Assessment', 'Risk of Falls Assessment', 'input_file', 'file', 0, 'Risk of Falls Assessment', 1, '2021-09-17 03:20:07.752', NULL, '5e08c7b457234153baa27f07c75984b6', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('cc3e542ea482422a908c40fa8e83fcdc', 'dailyworkload_caseload_cm_number', 'Number of Case Management clients', 'input_number', 'number', 0, 'Number of case management clients', 1, '2021-09-13 17:33:23.837', NULL, '8ed9c06ca5f24c448f228e375d6aa904', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('d012fb5079cc4273955735b1069dfbe5', 'client_interventions_client_name', 'Client Name', 'input_text', 'text', 0, 'Client Name', 1, '2021-09-17 12:40:19.141', NULL, 'd0bfd7095d4742e3a9133cd72ed02635', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('ddde131197ca4af39869fcbf8f8fd260', 'dailyworkload_caseload_cm_timespent', 'Time spent for Case Management Clients', 'input_time', 'time', 0, 'Time spent for Case Management Clients', 1, '2021-09-13 17:51:50.656', NULL, '8ed9c06ca5f24c448f228e375d6aa904', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('e65400f172bc468abe2b7bb063cdaa45', 'client_assessment_providerspecificforms_Speech_Language_Pathology_Adult_Assessment', 'Speech-Language Pathology Adult Assessment', 'input_file', 'file', 0, 'Speech-Language Pathology Adult Assessment', 1, '2021-09-17 03:10:33.306', NULL, '594146da66194973b1d731f151c1ce6c', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('eeb383e196354ac4928a84b350d1ede5', 'client_interventions_date', 'Date', 'input_date', 'date', 0, 'Date', 1, '2021-09-17 12:40:59.458', NULL, 'd0bfd7095d4742e3a9133cd72ed02635', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('fab6a50ceb7541b9b790f3c7c2ae7988', 'client_assessment_providerspecificforms_Physiotherapy_Assessment', 'Physiotherapy Assessment', 'input_file', 'file', 0, 'Physiotherapy Assessment', 1, '2021-09-17 03:06:33.108', NULL, '594146da66194973b1d731f151c1ce6c', NULL);
INSERT INTO providertool.entities_userroleattribute
(attribute_id, attribute_code, frontend_label, frontend_input, attribute_type, is_required, note, is_active, created_at, updated_at, attribute_group, sort_order)
VALUES('fdac6c42b8154d1398c404f9ed7cfc2a', 'dailyworkload_functional_center', 'Functional Center', 'input_time', 'time', 1, 'Functional Center', 1, '2021-09-13 21:23:58.560', NULL, 'f34ebd4e08894c848d147e97c6b7cf5b', NULL);



INSERT INTO providertool.entities_userroleentitydata
(entity_data_id, created_at, updated_at, entity_data_type_id, user_entity_id)
VALUES('e925768da8264a61ac75667884bb1e81', '2021-09-16 00:40:22.331', NULL, '2e454e63aa894194a9fb507e2ff94a42', 'd205efca061b4e69a450c75d593d89e2');



INSERT INTO providertool.entities_userroleentitydatatypes
(entity_data_type_id, data_type_code, data_type_label, is_active, created_at, updated_at, attribute_set_id)
VALUES('2e454e63aa894194a9fb507e2ff94a42', 'casemanager_daily_workload', 'Daily Workload', 1, '2021-09-13 18:27:18.976', NULL, 'b23d42fd97f14493a5cbb291268a38ea');
INSERT INTO providertool.entities_userroleentitydatatypes
(entity_data_type_id, data_type_code, data_type_label, is_active, created_at, updated_at, attribute_set_id)
VALUES('cbc8a7ab9e764a3eb4786fe8b419da23', 'casemanager-client-interventions', 'Client Interventions', 1, '2021-09-16 16:40:13.878', NULL, '8bcbb15d59064063ac9783ef7b3fb909');
INSERT INTO providertool.entities_userroleentitydatatypes
(entity_data_type_id, data_type_code, data_type_label, is_active, created_at, updated_at, attribute_set_id)
VALUES('d90d44e8480a47489844e03ff6b03647', 'casemanager-client-assessment', 'Client Assessment', 1, '2021-09-13 17:06:45.688', NULL, 'a99d47f5168d4c099dc0d5e84e9dfa85');
INSERT INTO providertool.entities_userroleentitydatatypes
(entity_data_type_id, data_type_code, data_type_label, is_active, created_at, updated_at, attribute_set_id)
VALUES('e254c5fdb0fb48528d78fd9c84a026d2', 'client_personal_info', 'Personal Info', 1, '2021-09-14 20:44:46.527', NULL, '735f6747f5b945acbe544de20c4b2cdb');
