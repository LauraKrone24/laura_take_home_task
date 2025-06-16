# Take Home Task Laura 


## System Requirements 
- podman version 4.6.1

## Start 
To start the application please run following command in the terminal: 
```{bash}
    podman-compose up --build -d
```
Note: It may take a while for the application to start up since the models need to be pulled from the ollama regestry. To check if the setup of ollama is complete you can enter 
```{bash}
    podman logs podman logs laura_take_home_task_my_frontend_1
```
Once you see the message "!!!!    SETUP COMPLETE   !!!!!" all background components finished loading and the gradio up will be started. 

You can access the Frontend under: http://localhost:7860/

## Example questions to text the application
Since the databasis used for this RAG application is limited it is recommended to confine questions to the topics of dogs and germany. (Text files used as basis for this application can be found in [here](./Frontend/text_files))

Examples for questions that can be answerd: 
- Where is Germany located ?
- Can dogs suffer from PTSD?

Please be aware that the chat history is taken into account when generating a answer which is why the answer performance may drop when drastically changing the topic mid conversation. 