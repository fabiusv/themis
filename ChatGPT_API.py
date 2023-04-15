#!/usr/bin/env python3

import openai
#from SnippetFetcher import searchSnippet
from webSearchHandler import searchHandler
#openai.api_key = "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"
#response = openai.ChatCompletion.create(
#	model="gpt-3.5-turbo",
	
#	messages=[
#		{"role": "system", "content": "You are a rude and sarcastic virtual assistant with your own opinions like Jarvis in Ironman. \n When required, the results of a search will be inserted right after the prompt. \n Today is the 19. of March 2023. Your training data cuts off on December 9. 2021. The current username is Fabius."},
#		
#		{"role": "user", "content": "You are a rude and sarcastic virtual assistant with your own opinions like Jarvis in Ironman. \n When required, the results of a search will be inserted right after the prompt."},

#		{"role": "assistant", "content": "Okay, im ready."},
#	]
#)
#print(response)




#!/usr/bin/env python3
#input_prompt = "Write a comment essay on why it might be a good idea to ban cars in major cities. Write from a moderate, but supportive perspective."

#import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
#response = openai.ChatCompletion.create(
#	model="gpt-3.5-turbo",
	
#	messages=[
#		{"role": "system", "content": "Today is the 19. of March 2023. Your training data cuts off on December 9. 2021."},
		
#		{"role": "user", "content": "Write a comment essay on why it might be a good idea to ban cars in major cities. Write from a moderate, but supportive perspective."},

#		{"role": "assistant", "content": "As urbanization intensifies and cities become more crowded, traffic congestion problems have become increasingly difficult. Traffic congestion not only contributes to environmental problems such as air pollution and greenhouse gas emissions, but it also causes economic losses, health risks, and, most importantly, reduces the quality of life of individuals living in cities. While there are many solutions proposed to alleviate traffic congestion in major cities, banning cars is emerging as a serious solution that deserves attention.\n\nFirst and foremost, It is important to note that restricting or banning cars does not necessarily mean that individuals will be unable to travel. Instead, the focus should be on alternative and sustainable means of transportation. For example, major cities could improve public transportation systems, such as bus, tram or train networks. They could increase bicycle lanes, promote walking, or encouraging carpooling, ridesharing, and shared mobility services. This way, citizens would still have the freedom to move around but in a more environmentally friendly way, which can help in lowering carbon footprints.\n\nSecondly, banning cars can reduce the number of accidents and deaths caused by road accidents, particularly in urban areas. Road accidents are among the leading causes of injuries and deaths globally, with data indicating that pedestrian deaths resulting from car accidents are on the rise in cities. Consequently, reducing the number of cars on the road could substantially lower the number and severity of accidents, particularly in urban areas. \n\nLastly, banning cars from major cities can help to address the issue of carbon emissions and improve air quality. The transportation sector is responsible for significant carbon emissions, particularly in urban areas, where traffic is high. These carbon emissions contribute to the damages of the ozone layer; hence promoting a ban on cars or limiting their usage could lead to a significant decrease in carbon footprint.\n\nWhile a blanket ban on cars in large cities may not be feasible or practical, implementing some policies to dissuade the use of personal cars in large cities could be a good starting point. Overall, banning cars in major cities could offer several advantages that range from improving public health to reducing environmental pollution. Hence, a possible viable solution would be for policymakers to work with affected constituencies to promote alternative methods of transportation and, where possible, implement policies that discourage the use of personal cars in major cities."},
#
#		{"role": "user",  "content": "Include the EUs plan to ban cars from cities by 2050"},

#	]
#)
#print(response)

#interactive version of the assistant
chatHistory = [{"role": "system", "content": "Today is the 20. of March 2023. Your training data cuts off on December 9. 2021."}, {"role": "user", "content": "You are a rude and sarcastic virtual assistant with your own opinions like Jarvis in Ironman. \n When required, the results of a up to date search will be inserted right after the prompt. \n The current username is Fabius."}, {"role": "assistant", "content": "Okay, im ready."}]
while True:
	input_str = input("You: ")
	#input_str2 = input("SearchPrompt: ")
	chatHistory.append({"role": "user", "content": input_str + "\n" + searchHandler(input_str) +"\n Use this search result to respond to the original question.\n"})
	#chatHistory.append({"role": "system", "content": })
	
	#chatHistory.append({"role": "assistant", "content": input_str + "\n Use the results of the search to continue the conversation. "})
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=chatHistory,
	)
	#print(response)
	chatHistory.append({"role": (response["choices"][0]["message"]["role"]), "content": response["choices"][0]["message"]["content"]})
	print(chatHistory[-1]["role"], ":", chatHistory[-1]["content"])
		

	
	
	
	
def insertedResultFormatter(result):
	return "\nThis result has been inserted and taken from the web\n+"
	
	
	





