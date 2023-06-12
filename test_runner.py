import classification.dialogflow as dialogflow

function = dialogflow.detect_intent_texts(1, "Will it rain today?").intent_function
function()