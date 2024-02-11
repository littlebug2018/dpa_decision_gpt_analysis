Here are all the jupyternotebooks to produce the major results for the GDPR project. The final and complete pipeline function is available in aus_ita_bel_po_es_pipeline.ipynb

1 build the folders with the picked document to be analyzed in them

(manually) choose the file type to analyse (.txt or .html)
create output repository

2 overview: check classify document as normal, large,over oversized

 < 14,000 tk    normal
 
14,000 < ... < 150,000 tk large

> 150,000 tk oversized

3 normal sized summary production

construct message

gpt request

4 large sized summary production

segmentation

construct message (inside write summary)

write summary

5 JSON profile production

construct prompts with examples (few-shot)

write JSON profile
