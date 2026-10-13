I have to recieve userinput at one end point

@app.route("/first end point")

i need to also store collection as prompts
prompts:{
"\_id":"Education_Prompt",
"template":"You are an expert in education domain. Answer the following: {{userinput}}"
}

then i need to store these in another collection called history

collections
users
-id
-userinput
prompts
-id
-template
history
-request(template from prompts)
-response(imedeate response for the same)

test response in postman

another POST endpoint will send list of string in one request

@app.post("/second end point")
