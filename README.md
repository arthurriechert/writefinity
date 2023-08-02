# writefinity

## For those who don't like paying the ChatGPT subscription
I made this project because I was in what my opinion seemed like performance dips in the current ChatGPT models. Plus, I couldno longer justify the $20/month subscription as I do not use it that much anymore due to the loss of web browsing. My focus shifted to making it more affordable, and it is cheaper to use the OpenAI API itself.

This project is made with the goal of interfacing with multiple models sometime in the future, having integration with external APIs to automate my workflow, and improving the chat experience. In other words, this is a project that I plan on building as I get new needs. Feel free to build it on it and implement your own uses!

## Install Instructions
1. cd src/.streamlit
2. touch secrets.toml and open in an editor
3. copy & paste with your API keys 
[api_keys]
openai="api-key"
serpapi="api-key"
4. cd ../../ && source env/bin/activate
5. cd src && stream run main.py
6. Go to http://localhost:8501/chat_page
