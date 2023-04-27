import re
string = """Hervorgehobenes Snippet aus dem Web The Republic of Mainz was the first democratic state in the current German territory and was centered in Mainz.
 A product of the French Revolutionary Wars French Revolutionary Wars The French Revolutionary Wars (French: Guerres de la Révolution française) were a series of sweeping military conflicts lasting from 1792 until 1802 and resulting from the French Revolution.
 They pitted France against Britain, Austria, Prussia, Russia, and several other monarchies.
https://en.
wikipedia.
org › wiki › French_Revolutionary_Wars French Revolutionary Wars - Wikipedia, it lasted from March to July 1793.
Republic of Mainz - Wikipedia Wikipediahttps://en.
wikipedia.
org › wiki › Republic_of_Mainz Wikipediahttps://en.
wikipedia.
org › wiki › Republic_of_Mainz Informationen zu hervorgehobenen Snippets•Feedback geben"""
fixed_string = re.sub(r'([a-z])([A-Z])', r'\1 \2', string)

try:
    fixed_string = fixed_string.replace("Hervorgehobenes Snippet aus dem Web", "")
    
except:
    print("failed")
    pass
try:
    fixed_string = fixed_string.split("https")[0]
except:
    pass
try:

    fixed_string = fixed_string.split("Andere suchten")[0]
except:
    pass

try:
    fixed_string = fixed_string.replace(".", ".\n")
except:
    pass

print(fixed_string)