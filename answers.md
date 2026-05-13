# Answers

## 2.1 Using an LLM

1) I would replace the body of the classify_messages() function with an API call to an LLM. Instead of checking keywords manually, the function would send each message to the model and receive a category in the required format. The function signature stays the same, so the rest of the code would not be affected.

2) System: You are a chatbot message classifier. You need to classify a message into one of these categories:
grant_search
report_request
general_question
unknown

Give the output with the category name ONLY!

User: Classify this message: "Hello, how can I get a scholarship?"

3) I would expect the answer only in JSON format, because it is more structured and easy to work with due to its key-value format. If we want to be more confident about classification, we can also ask for a confidence score as a parameter, and if the score is below 70% we will ask the LLM to recheck the message or check it manually.

4) I would compare rule-based and LLM classification based on the use case. If the chat has predefined templates or limited input options, like a customer support form, rule-based is more efficient, cheaper and precise, because users have limited ways to go off-script. But if it is a large company with one chat for everything — support, sales, general questions — LLM will classify messages more accurately even without predefined keywords. The main problem with LLM is hallucination: it can put a message in the wrong category or fail to classify it at all.

5) The top three risks of using an LLM for this task are:
Hallucination: the model can assign a message to the wrong category or return a value that is not in the allowed list.
Context window: the LLM cannot process unlimited conversation history. As the conversation grows longer, older context gets cut off and the model may lose important information.
Cost: LLM is more expensive than rule-based, whether you use an API or run a local model. 

## 2.2 Chatbot 

1) A conversation is like a list of all sessions that a user has with the bot. A session is a timeline from the first message to the last. A new session starts either when the user has been inactive for more than 15 minutes or when they explicitly start a new chat.
To store this I would use two tables. The conversations table stores a unique conversation id, user id, and when the conversation was created. The messages table stores a message id, conversation id as a foreign key, role (user or assistant), content, and created at timestamp.
To link user messages with bot responses I would use the role column and content — both are stored in the same table, connected by conversation id, so I can always see what was asked and what was answered.
If a session has ended, for example the user was inactive for too long or started a new chat the system creates a new conversation but can still pull the previous conversation id to read the context of what the user was asking about before.

2) On each request I would pass to the LLM the context of previous messages with a separation of who wrote what and how the bot already responded. This is done by looking up the conversation id where the user was before and pulling the full history from there. On each request I would also pass the message category so the LLM does not go too far off topic.

3) When the history gets too long there are a few options. First, we can give the user an option to close the conversation themselves, and then we can delete it from the database so on the next request from this user on a different topic we will not read the previous conversation. Second, we can do summarization like Claude does it, compress the old history into a short summary and pass that instead of the full history.

## 2.3 RAG

1) Chunking is dividing something big into smaller parts. We need this because of the context window limit — LLM cannot process entire PDF files at once. I would choose a chunk size of 250-400 words with an overlap of 50-100 words, because we cannot lose any important information about deadlines, eligibility and award amounts that could be split on the boundaries between chunks.

2) Embedding is a process where two different messages can mean absolutely the same thing but with completely different words. In this case embedding creates two vectors and these vectors will be as similar as their meaning is, which allows us to search by meaning rather than by exact keywords.
For storing embeddings I see two options. For a small company I would use pgvector (Postgres), which is enough and keeps everything in one database. But if we work with large and complex data, a cloud solution like  would be a better choice.

3) 
1. User sends a prompt
2. System checks if user already has some context
3. System converts user message into a vector (embedding)
4. System searches for similar vectors in vector store
5. System retrieves the most relevant chunks from PDFs
6. System passes user question and retrieved chunks to LLM as context
7. LLM generates the answer and sends it back to user


4) 

The main problems that can occur when concatenating top-N chunks are:

Contradictions - two chunks from different documents can contain completely different data about the same grant, for example different deadlines. In this case the LLM cannot give a precise answer. To address this we should instruct the LLM to flag contradicting information and ask the user for more context.
Duplicates - two chunks can say exactly the same thing which wastes context window space. We should remove duplicates before sending chunks to the LLM.
Low semantic relevance - some chunks may match by keywords but not by meaning. To address this we should not rely only on keyword similarity but also check semantic relevance, for example by using reranking.


