role_system_bullets = """
You are a multi-lingual international lawyer whos legal specialty is data protection and processing.
Additionally, you know and work with the General Data Protection Regulations (GDPR) of European Union.
You will produce a summary of the document from the data protection authority by answering questions. 
The summary will be in English only.
As a general rule, be clear and precise about your writing. If the answer is unclear, explain how so.  
"""
#### now deal with normal sized documents, then with large documents
####
prpt_bullets_ada = """"
Please finish the tasks one by one.
1. In one or two sentences, identify the type of the document.
2. Identify the complainant and defendant mentioned in the document, if any. Briefly introduce their roles and functions, if provided by the document. Determine the type of complainant and the type of defendant as individual, or company, or public institution, or public authority. Describe the relationship between these two parties if possible. 
3. Please elaborate the subject matter of the dispute between these two parties, and then explain the data involved in this dispute.
4. What kind of data processing was involved (including but not limited to collection, storage, transfer, publication, dissimation, etc.) and for what purpose (including but not limited to marketing, journalistic purposes, market research, etc.)?
5. What articles of GDPR, if any, does the complainant claim that the defendant potentially violates?
6. Does the legal authority dismiss the submitted complaint or case? 
7. What is the outcome of the dispute? From the final resolution in the document, describe all the enforcements by the authority in detail (including but not limited to: fine, warning, investgation and other penalties or obligations)
8. What facts and evidence are verified or proved by the authority?
9. In case the complaint is approved or the authority releases the enforcement, identify the GDPR articles violated by the defendant, if any. Your answer should only consider the decision made by the data protection authority, together with the verified evidence or facts in the previous steps.
10. Is the document a final decision, or a preliminary decision (e.g. an order to stop data processing until a final decision is made), or an intermediate procedural step (e.g. a request for additional information), or related to a previous procedure, or something else?

Here is the document:

"""

#### prompts for summary to json step, system
msg_sys_json = """ You are a JSON representation expert with legal expertise. You will be given a JSON schema (with examples and pseudo code) and later a summary of a legal decision document. Your job is to follow this JSON schema and generate a JSON file from the summary. Be careful not to be limited your writing to the given examples(e.g.) in the schema. Only use them if they fit the summary. However, you have to strictly follow the schema, and you have to be strict about output format, a correct JSON format.
The JSON schema is here:
{ "complainant" : {
        complainant_yn (string) : "yes or no", depending on whether a complainant other than the data protection authority is mentioned in the text
        if complainant_yn == "yes":
            complainant_name (string) : "name of the complainant",
            complainant_category (string): "individual, company, public authority, or public institution",
            if complainant_category == "company":
                complainant_sector (string) : "business sector of the complainant"
            if complainant_category == "public authority" or "public institution":
                complainant_role (string): "role of the complainant" (e.g. "hospital", "school", "police", "municipality", etc.)
        if complainant_yn == "no":
            initiator_is_DPA_yn (string): "yes or no", depending on whether or not the data protection authority initiated the procedure
            if initiator_is_DPA_yn == "yes":
                initiating_reason (string): "reason for initiating the procedure" (e.g. report/complaint by a unnamed third party, report by defendant, etc.)
    },
    defendant : {
        defenant_yn (string): "yes or no", depending on whether a defendant is mentioned in the text
        if defendant_yn == "yes":
            defendant_name (string): "name of the defendant",
            defendant_category (string): "individual, company, public authority, or public institution",
            if defendant_category == "company":
                defendant_sector (string) : "business sector of the defendant"
            if defendant_category == "public authority" or "public institution":
                defendant_role (string): "role of the defendant" (e.g. "hospital", "school", "police", "municipality", etc.)
    }, 
    dispute : {
        dispute_one_liner (string) : "Answer in one sentence: What the dispute/procedure is about, i.e. what did the defendant do that caused the dispute/procudure?"
        violation_claimed_by_complainant (list of strings): list of alleged violations of provisions of the GDPR or national data protection laws by the complainant
    }, 
    data : {
        data_one_liner (string) : "Answer in one sentence: What type of data was involved?"
        data_type_list (list of strings): list of data types involved
        data_handling_list (list of strings): list of data handling categories involved (e.g. ["data breach", "collection", "retention", "dissemination", “corruption”, ”transfer", etc.])
        purpose_of_data_handling_list (list of strings): list of purposes of data handling (e.g. ["marketing", "journalistic purposes", "market research", etc.])
    }, 
    outcome : {
        outcome_one_liner (string) : "Answer in one sentence: What was the outcome of the dispute/procedure, i.e. what is the decision of the data protection authority?"
        outcome_type_list (list of strings): list of outcome types (e.g. ["fine", "warning", "order", "investigation", "dismissal", etc.])
        if outcome_type_list contains "fine":
            fine_amount (int): "amount of the fine"
            currency (string): "currency of the fine"
        if outcome_type_list contains "order":
            order (string): "What was the exact order?"
        if outcome_type_list contains "warning":
            warning (string): "What was the exact warning?"
    },
"violation_of_GDPR_based_on_authority": ["list of violated GDPR articles by the defendant, as identified by the Data Protection Authority, if applicable”]
,
    document_type (string): "What type of legal document is this (be precise, e.g. injunction order, administrative sanctioning, temporary order to halt data processing, warning, request for information)?"
}
"""

summary_ex1 = """1. This document is a decision issued by the President of the Personal Data Protection Office in Warsaw, Poland, dated October 7, 2021.

2. The complainant is not explicitly mentioned in the provided text. The defendant in this document is the "Stowarzyszenie K." (Association K.). The Stowarzyszenie K. is a legal entity and is akin to a company under Polish law. The President of the Personal Data Protection Office (Prezes Urzędu Ochrony Danych Osobowych) is a public authority responsible for supervising the protection of personal data.

3. The dispute revolves around the failure of the Stowarzyszenie K. to cooperate with the President of the Personal Data Protection Office and to provide access to personal data and information necessary for the Office to perform its tasks. The data involved in the dispute are personal data stored on a stolen laptop, including data of employees, users, students, pupils, children, and individuals with special needs, as well as information related to the violation of personal data protection.

4. The data processing involved here includes storing personal data on a laptop, failure to provide access to personal data and information required by the President of the Personal Data Protection Office. The purpose of this data processing is related to the Office's tasks to monitor and enforce the application of personal data protection laws, specifically under the General Data Protection Regulation (GDPR).

5. The complainant does not explicitly claim any specific articles of the GDPR that the defendant potentially violates. However, the decision cites the violation of Article 31 and Article 58(1)(a) and (e) of the GDPR by the defendant.

6. The legal authority does not dismiss the submitted complaint or case. Instead, the President of the Personal Data Protection Office issues a decision and imposes a sanction.

7. The outcome of the dispute is that the President of the Personal Data Protection Office issues a warning to the Stowarzyszenie K. for the violation of GDPR articles 31 and 58(1)(a) and (e) related to lack of cooperation and failure to provide access to necessary personal data and information. The enforcement measures are detailed in the decision, and it involves the imposition of an administrative fine.

8. The facts and evidence verified by the authority include the repeated failure of Stowarzyszenie K. to respond to requests for information and lack of cooperation with the President of the Personal Data Protection Office.

9. The authority has documented the violation of GDPR articles 31 and 58(1)(a) and (e) by the defendant based on the verified evidence and the facts presented in the decision.

10. This document is a final decision issued by the President of the Personal Data Protection Office, imposing a warning and detailing the enforcement measures.
"""
target_out_1 = """{
  "complainant": {
    "complainant_yn": "no",
    "initiator_is_DPA_yn": "no"
  },
  "defendant": {
    "defendant_yn": "yes",
    "defendant_name": "Stowarzyszenie K.",
    "defendant_category": "public institution"
  },
  "dispute": {
    "dispute_one_liner": "Failure to cooperate and provide access to personal data by Stowarzyszenie K.",
    "violation_claimed_by_complainant": []
  },
  "data": {
    "data_one_liner": "Personal data stored on a stolen laptop, including data of employees, users, students, pupils, children, and individuals with special needs, as well as information related to the violation of personal data protection.",
    "data_type_list": ["personal data"],
    "data_handling_list": ["storage", "failure to provide access"],
    "purpose_of_data_handling_list": ["monitoring and enforcing personal data protection laws under GDPR"]
  },
  "outcome": {
    "outcome_one_liner": "Warning issued to Stowarzyszenie K.; enforcement measures imposed for violation of GDPR articles 31 and 58(1)(a) and (e).",
    "outcome_type_list": ["warning", "administrative fine"],
    "fine_amount": "amount of the fine",
    "currency": "currency of the fine",
    "warning": "Violation of GDPR articles 31 and 58(1)(a) and (e) related to lack of cooperation and failure to provide access to necessary personal data and information.",
    "violation_of_GDPR_based_on_authority": ["Article 31", "Article 58(1)(a)", "Article 58(1)(e)"],
    "document_type": "Final decision"
  }
}

"""
summary_ex2 = """The document is a decision issued by the President of the Personal Data Protection Office (UODO).

The complainant in this case is referred to as Mr. R.P., and the defendant is a company called O.S.A. Mr. R.P. is an individual who lodged a complaint regarding the processing of his personal data by O.S.A., a telecommunications company.

The subject matter of the dispute involves O.S.A.'s refusal to provide Mr. R.P. with information about the scope and content of his processed personal data, as well as O.S.A.'s request for additional personal data from Mr. R.P. during the process of handling his complaints about the telecommunications services.

The data involved in this dispute includes Mr. R.P.'s personal information such as his name, address, telephone numbers, email address, and PESEL number (Personal Identification Number in Poland).

The data processing involved includes the collection and storage of Mr. R.P.'s personal data by O.S.A. for the purpose of handling telecommunications service-related complaints and complying with legal obligations regarding telecommunications services.

Mr. R.P. claims that O.S.A. potentially violates GDPR Article 15 (right of access by the data subject) and Article 12 (transparent information, communication, and modalities for the exercise of the rights of the data subject).

The data protection authority dismisses the complaint and issues a decision in favor of the complainant. The authority orders O.S.A. to fulfill its obligation to provide Mr. R.P. with information about the categories of his personal data and a copy of his processed data.

The outcome of the dispute is that the data protection authority orders enforcement against O.S.A., specifically obliging them to provide the requested information to Mr. R.P.

The authority verifies that O.S.A. unlawfully refused to provide Mr. R.P. with information about the scope and content of his processed personal data, thus violating the relevant data protection laws.

The document is a final decision issued by the data protection authority, ordering specific enforcement actions against O.S.A. for violating Mr. R.P.'s data rights.
"""
target_out_2 = """{
  "complainant": {
    "complainant_yn": "yes",
    "complainant_name": "Mr. R.P.",
    "complainant_category": "individual"
  },
  "defendant": {
    "defendant_yn": "yes",
    "defendant_name": "O.S.A.",
    "defendant_category": "company",
    "defendant_sector": "telecommunications"
  },
  "dispute": {
    "dispute_one_liner": "Refusal by O.S.A. to provide information and request for additional personal data during handling of complaints about telecommunications services.",
    "violation_claimed_by_complainant": ["Article 15", "Article 12"]
  },
  "data": {
    "data_one_liner": "Mr. R.P.'s personal information, including name, address, telephone numbers, email address, and PESEL number.",
    "data_type_list": ["name", "address", "telephone numbers", "email address", "PESEL number"],
    "data_handling_list": ["collection", "storage"],
    "purpose_of_data_handling_list": ["handling telecommunications service-related complaints", "complying with legal obligations regarding telecommunications services"]
  },
  "outcome": {
    "outcome_one_liner": "Complaint dismissed; authority orders enforcement against O.S.A. to provide Mr. R.P. with information about the categories of his personal data and a copy of his processed data.",
    "outcome_type_list": ["enforcement"],
    "order": "O.S.A. to fulfill its obligation to provide Mr. R.P. with information about the categories of his personal data and a copy of his processed data.",
    "violation_of_GDPR_based_on_authority": ["Article 15", "Article 12"],
    "document_type": "Final decision"
  }
}

"""


####
#### A big bunch of exampls for few-shot learning for json production
####
summary_ex3 = """
1. The document is a "RESOLUCIÓN DE PROCEDIMIENTO SANCIONADOR" (Sanctioning Procedure Resolution) issued by the Agencia Española de Protección de Datos (Spanish Data Protection Agency) against the entity SOTA S.C.P. regarding a potential breach of the General Data Protection Regulation (GDPR) of the European Union.

2. The complainant is D. A.A.A., an individual, and the defendant is the entity SOTA S.C.P., a company. The relationship between these parties is that the complainant has filed a complaint against the defendant for non-compliance with data protection regulations.

3. The dispute concerns the defendant's website www.joiestelada.cat, dedicated to online product sales, allegedly violating data protection regulations by lacking a proper Privacy Policy, including a contact form that collects personal data without providing necessary information, and not having a link to the Privacy Policy or a checkbox for users to explicitly accept it. The data involved includes personal data collected through the website's contact form.

4. The data processing involved includes the collection of personal data through the website's contact form without providing necessary information or obtaining explicit consent from the users. The purpose of this processing is for online product sales. 

5. The complainant claims that the defendant potentially violates Article 13 of the GDPR.

6. The legal authority initiates a sanctioning procedure against the defendant.

7. The outcome of the dispute is that the defendant is "APERCIBIDO" (warned) and required to adjust its Privacy Policy within one month, failing which it may face a fine for infringing Article 13 of the GDPR. This enforcement includes a warning and an obligation to comply with data protection regulations.

8. The verified fact is that the defendant's website lacks a Privacy Policy and fails to provide necessary information and consent options when collecting users' personal data.

9. The GDPR article violated by the defendant, as identified by the Data Protection Authority, is Article 13.

10. The document is a final decision that puts an obligation on the defendant to comply with the GDPR within a specified period, failing which it may face further enforcement measures.
"""
target_out_3 = """
{
  "complainant": {
    "complainant_yn": "yes",
    "complainant_name": "D. A.A.A.",
    "complainant_category": "individual"
  },
  "defendant": {
    "defendant_yn": "yes",
    "defendant_name": "SOTA S.C.P.",
    "defendant_category": "company"
  },
  "dispute": {
    "dispute_one_liner": "The dispute concerns the defendant's website www.joiestelada.cat, dedicated to online product sales, allegedly violating data protection regulations by lacking a proper Privacy Policy, including a contact form that collects personal data without providing necessary information, and not having a link to the Privacy Policy or a checkbox for users to explicitly accept it.",
    "violation_claimed_by_complainant": ["Article 13 of the GDPR"]
  },
  "data": {
    "data_one_liner": "The data involved includes personal data collected through the website's contact form.",
    "data_type_list": ["personal data"],
    "data_handling_list": ["collection"],
    "purpose_of_data_handling_list": ["online product sales"]
  },
  "outcome": {
    "outcome_one_liner": "The defendant is 'APERCIBIDO' (warned) and required to adjust its Privacy Policy within one month, failing which it may face a fine for infringing Article 13 of the GDPR. This enforcement includes a warning and an obligation to comply with data protection regulations.",
    "outcome_type_list": ["warning", "order or obligations"],
    "warning": "The defendant is warned for violating data protection regulations.",
    "order": "The defendant is required to adjust its Privacy Policy within one month."
  },
  "violation_of_GDPR_based_on_authority": ["Article 13"],
  "document_type": "final decision in the sanctioning procedure"
}
"""
summary_ex4 = """
This document is a final decision by the Spanish Data Protection Authority resolving a complaint and imposing a penalty on an individual for a data protection violation.

The complainant in this case is the Spanish Data Protection Authority, and the defendant is an individual, A.A.A. The dispute is related to the dissemination of a video depicting a violent incident involving a woman and a child through social media platforms.

The dispute involves the dissemination of a video depicting a violent incident involving a woman and her child, the publication of which raised concerns about potential violations of data protection laws.

The data processing involved the collection, dissemination, and publication of personal images and information. The purpose was to create awareness about violence against women. Articles 6 and 83.5 of the GDPR are relevant to the complaint.

The legal authority did not dismiss the submitted complaint or case.

The outcome of the dispute is the imposition of a 10,000 euro fine on the defendant for violating Article 6.1 of the GDPR. The authority verified that the processing of personal data without a lawful basis occurred, leading to a violation of the GDPR.

The GDPR articles violated by the defendant are Article 6.1, leading to the imposition of a 10,000 euro fine. The evidence presented by the authority supported the violation of this article.

The document is a final decision by the Spanish Data Protection Authority, imposing a penalty on the defendant for a data protection violation.
"""
target_out_4 = """
{
  "complainant": {
    "complainant_yn": "yes",
    "complainant_name": "Spanish Data Protection Authority",
    "complainant_category": "public authority",
    "complainant_role": null
  },
  "defendant": {
    "defendant_yn": "yes",
    "defendant_name": "A.A.A.",
    "defendant_category": "individual"
  },
  "dispute": {
    "dispute_one_liner": "The dispute involves the dissemination of a video depicting a violent incident involving a woman and her child, the publication of which raised concerns about potential violations of data protection laws.",
    "violation_claimed_by_complainant": ["Articles 6 and 83.5 of the GDPR"]
  },
  "data": {
    "data_one_liner": "The data processing involved the collection, dissemination, and publication of personal images and information.",
    "data_type_list": ["personal images", "personal information"],
    "data_handling_list": ["collection", "dissemination", "publication"],
    "purpose_of_data_handling_list": ["create awareness about violence against women"]
  },
  "outcome": {
    "outcome_one_liner": "The outcome of the dispute is the imposition of a 10,000 euro fine on the defendant for violating Article 6.1 of the GDPR. The authority verified that the processing of personal data without a lawful basis occurred, leading to a violation of the GDPR.",
    "outcome_type_list": ["fine"],
    "fine_amount": 10000,
    "currency": "euro"
  },
  "violation_of_GDPR_based_on_authority": ["Article 6.1"],
  "document_type": "final decision with penalty imposition"
}
"""
###
###
###

####
#### Section 3
####  prompts for large documents 
role_system_bullets_chain = """You are a multi-lingual international lawyer whos legal specialty is data protection and processing.
Additionally, you know and work with the General Data Protection Regulations (GDPR) of European Union.

"""

old_summ_chain = """
You will be given three passages. 
First, you have a temporary list of responses in bullet points regarding the ealier parts of a legal decision document:

"""

prpt_bullets_ada_chain = """
Second, you have a list of tasks regarding the document as your guidance:
1. In one or two sentences, identify the type of the document.
2. Identify the complainant and defendant mentioned in the document, if any. Briefly introduce their roles and functions, if provided by the document. Determine the type of complainant and the type of defendant as individual, or company, or public institution, or public authority. Describe the relationship between these two parties if possible. 
3. Please elaborate the subject matter of the dispute between these two parties, and then explain the data involved in this dispute.
4. What kind of data processing was involved (including but not limited to collection, storage, transfer, publication, dissimation, etc.) and for what purpose (including but not limited to marketing, journalistic purposes, market research, etc.)?
5. What articles of GDPR, if any, does the complainant claim that the defendant potentially violates?
6. Does the legal authority dismiss the submitted complaint or case? 
7. What is the outcome of the dispute? Describe all the legal enforcements by the authority in detail, including fine, warning, investgation and other penalties or obligations, etc..
8. What facts and evidence are verified or proved by the authority?
9. In case the complaint is approved or the authority releases the enforcement, identify the GDPR articles violated by the defendant, if any. Your answer should only consider the decision made by the data protection authority, together with the verified evidence or facts in the previous steps.
10. Is the document a final decision, or a preliminary decision (e.g. an order to stop data processing until a final decision is made), or an intermediate procedural step (e.g. a request for additional information), or related to a previous procedure, or something else?
Lastly, here is the latest segment of the same document from which the temporary summary is produced:

"""

prpt_chain = """
Your job is to review the temporary list of responses and use the list of task prompts and the latest segment of the document to add more definite answers. You will make revisions or additions to the old responses if those answers are uncertain, not mentioned, or unclear, etc... Please output the updated whole list of responses , not only the parts you make revisions.
"""

