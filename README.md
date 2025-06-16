# Laura Take-Home Task
This repository contains the code for the take home task for the technical interview as a PCAI Customer Success Engineer. 

## System Requirements

- Podman version 4.6.1
- Podman compose version 1.0.6

## Getting Started

To start the application, run the following command in your terminal:

```bash
    podman-compose up --build -d
```

> **Note:** The initial startup may take some time as the required models are downloaded from the Ollama registry and the data is loaded in the vectorstore.

To monitor the setup progress, check the logs with:

```bash
podman logs laura_take_home_task_my_frontend_1
```

When you see the message:

```
!!!!    SETUP COMPLETE   !!!!!
```

all background components have finished loading.

Access to the gradio frontend will be available at: [http://localhost:7860/](http://localhost:7860/)

## Example Questions

This RAG application's database is limited. For best results, focus your questions on the topics of **dogs** and **Germany**. The text files used as the knowledge base are located in [`Frontend/text_files`](./Frontend/text_files).

Sample questions:

- Where is Germany located?
- Can dogs suffer from PTSD?

> **Note:** The chat history influences responses. Changing topics drastically mid-conversation may reduce answer quality.
