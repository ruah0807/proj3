from transformers import pipeline

classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

sentences = ["""The federal government has set out on a path to solve the housing crisis, with bold investments and ambitious targets outlined in Budget 2024 and their new housing plan. This week’s budget promised $8.5 billion in new spending on housing, complemented by as much as $55 billion in financing – these investments are promising to unlock 3.87 million new homes by 2031.  

The impact of the new housing measures should not be underestimated – this is the most ambitious housing plan by the federal government in 50 years and will set Canada up to address the housing crisis over the long-term. We are encouraged by the Government’s adoption of many of the recommendations from the National Housing Accord, which laid out a multi-sector roadmap to solve Canada’s rental housing crisis.

The housing plan takes a multi pronged approach to solving the housing crisis, with investments and policies that will incentivize and speed up the construction of both market and non-market housing. New policies such as reforms to tax measures for housing and the availability of low-cost financing were recommended by the Accord and will help put Canada on a path to reaching the 3.5 million homes needed to restore affordability.  

The advocacy work of the Canadian Alliance to End Homelessness and our supporters has kept homelessness on the Government’s agenda. CAEH notes that there are important investments in the Government’s housing plan and in the federal Budget directed at alleviating homelessness over the long-term. The $1 billion investment to stabilize Reaching Home, $250 million for housing-focused responses to encampments and unsheltered homelessness, and $50 million to support communities adopt best practices and accelerate reductions in homelessness will have a tangible impact on community efforts to prevent and end homelessness.  

But over the coming months and years, while the new affordable housing gets built, we are particularly worried about the wave of new homelessness growing across the country, and the lack of supports in place to help people experiencing and at-risk of homelessness today. For those at risk of losing their home, direct supports are the most cost-effective way to keep them in their housing and stop them from becoming homeless. A Homelessness Prevention and Housing Benefit would do just that, and is a necessary tool to stop growing homelessness until Canada has fixed the housing crisis and restores affordability for all.

Across the country, communities are seeing new homelessness, including among asylum seekers, who are finding themselves in municipal shelter systems in the absence of a comprehensive refugee and asylum seeker resettlement system. The $1.1 billion announced in Budget 2024 to extend the Interim Housing Assistance Program is a necessary measure in addressing this situation, and the federal government must continue to work with all levels of government to quickly deliver the community-driven solutions needed to support the housing needs of asylum seekers.  

The federal government has set a clear intention to solve the housing crisis and has created the conditions to address it. """]

model_outputs = classifier(sentences)
print(model_outputs[0])
# produces a list of dicts for each of the labels
